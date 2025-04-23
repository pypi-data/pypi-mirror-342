# SPDX-License-Identifier: MIT
# Copyright (C) 2024 Avnet
# Authors: Nikola Markovic <nikola.markovic@avnet.com> et al.

import random
import time
from datetime import datetime, timezone
from ssl import SSLError
from typing import Callable, Optional

from avnet.iotconnect.sdk.sdklib.dra import DeviceRestApi
from avnet.iotconnect.sdk.sdklib.error import C2DDecodeError
from avnet.iotconnect.sdk.sdklib.mqtt import C2dOta, C2dMessage, C2dCommand, C2dAck, TelemetryRecord, TelemetryValueType, encode_telemetry_records, encode_c2d_ack, decode_c2d_message
from avnet.iotconnect.sdk.sdklib.util import Timing
from paho.mqtt.client import CallbackAPIVersion, MQTTErrorCode, DisconnectFlags, MQTTMessageInfo
from paho.mqtt.client import Client as PahoClient
from paho.mqtt.reasoncodes import ReasonCode

from .config import DeviceConfig


class Callbacks:
    def __init__(
            self,
            command_cb: Optional[Callable[[C2dCommand], None]] = None,
            ota_cb: Optional[Callable[[C2dOta], None]] = None,
            disconnected_cb: Optional[Callable[[str, bool], None]] = None,
            generic_message_callbacks: dict [int, Callable[[C2dMessage, dict], None]]= None
    ):
        """
        Specify callbacks for C2D command, OTA (not implemented yet) or MQTT disconnection.

        :param command_cb: Callback function with first parameter being C2dCommand object.
            Use this callback to process commands sent by the back end.

        :param ota_cb: Callback function with first parameter being C2dOta object.
            Use this callback to process OTA updates sent by the back end.

        :param disconnected_cb: Callback function with first parameter being string with reason for disconnect
            and second a boolean indicating whether a disconnect request was received from the server.
            Use this callback to asynchronously react to the back end disconnection event rather than polling Client.is_connected.

        :param generic_message_callbacks: A dictionary of callbacks indexed by the message type.
        """

        self.disconnected_cb = disconnected_cb
        self.command_cb = command_cb
        self.ota_cb = ota_cb
        self.generic_message_callbacks = generic_message_callbacks or dict[int, C2dMessage]() # empty dict otherwise


class ClientSettings:
    """ Optional settings that the user can use to control the client MQTT connection behavior"""

    def __init__(
            self,
            verbose: bool = True,
            connect_timeout_secs: int = 30,
            connect_tries: int = 100,
            connect_backoff_max_secs: int = 15
    ):
        if verbose:
            from . import __version__ as SDK_VERSION
            from avnet.iotconnect.sdk.sdklib import __version__ as LIB_VERSION
            print(f"/IOTCONNENCT Lite Client started with version {SDK_VERSION} and Lib version {LIB_VERSION}")
        self.verbose = verbose
        self.connect_timeout_secs = connect_timeout_secs
        self.connect_tries = connect_tries
        self.connect_backoff_max_secs = connect_backoff_max_secs
        if connect_timeout_secs < 1:
            raise ValueError("connect_timeout_secs must be greater than 1")
        if connect_tries < 1:
            raise ValueError("connect_tries must be greater than 1")


class Client:
    """
    This is an Avnet /IOTCONNECT MQTT client that provides an easy way for the user to
    connect to /IOTCONNECT, send and receive data.

    :param config: Required device configuration. See the examples or DeviceConfig class description for more details.
    :param callbacks: Optional callbacks that can be provided for the following events:
        - /IOTCONNECT C2D (Cloud To Device) commands that you can send to your device using the /IOTCONNECT
        - /IOTCONNECT OTA update events.
        - Device MQTT disconnection.
    :param settings: Tune the client behavior by providing your preferences regarding connection timeouts and logging.

    Usage (see basic-example.py or minimal.py examples at https://github.com/avnet-iotconnect/iotc-python-lite-sdk for more details):

    - Construct this client class:
        - Provide your device information and x509 credentials (certificate and private key)
            Either provide the path the downloaded iotcDeviceConfig.json and use the DeviceConfig.from_iotc_device_config_json_file()
            class method. You can download the iotcDeviceConfig.json by clicking the cog icon in the upper right of your device's info panel.

            Or you can also provide the device parameters directly:

            device_config = DeviceConfig(
                platform="aws",                             # The IoTconnect IoT platform - Either "aws" for AWS IoTCore or "az" for Azure IoTHub
                env="your-environment",                     # Your account environment. You can locate this in you /IOTCONNECT web UI at Settings -> Key Value
                cpid="ABCDEFG123456",                       # Your account CPID (Company ID). You can locate this in you /IOTCONNECT web UI at Settings -> Key Value
                duid="my-device",                           # Your device unique ID
                device_cert_path="path/to/device-cert.pem", # Path to the device certificate file
                device_pkey_path="path/to/device-pkey.pem"  # Path to the device private key file
            )
            NOTE: If you do not pass the server certificate, we will use the system's trusted certificate store, if available.
            For example, the trusted Root CA certificates from the in /etc/ssl/certs will be used on Linux.
            However, it is more secure to pass the actual server CA Root certificate in order to avoid potential MITM attacks.
            On Linux, you can use server_ca_cert_path="/etc/ssl/certs/DigiCert_Global_Root_CA.pem" for Azure
            or server_ca_cert_path="/etc/ssl/certs/Amazon_Root_CA_1.pem" for AWS

        - (Optional) provide callbacks for C2D Commands or device disconnect.
            See the basic-example.py at https://github.com/avnet-iotconnect/iotc-python-lite-sdk example for details.

        - (Optional) provide ClientSettings to tune the client behavior.

        It is recommended to surround the DeviceConfig constructor and the Client constructor
        with a try/except block catching DeviceConfigError and printing it to get more information
        to be able to troubleshoot configuration errors.


    - Call Client.connect(). The call will block until successfully connected or timed out. For example:

    - Ensure that the Client.is_connected() periodically or react to a disconnect event callback
        and attempt to reconnect or perform a different action appropriate to your application. For example:
        if not client.is_connected:
            client.connect()

    - Send messages with Client.send_telemetry() or send_telemetry_records().
        See basic-example.py example at https://github.com/avnet-iotconnect/iotc-python-lite-sdk for more info.
        For example:
            c.send_telemetry({
                'temperature': get_sensor_temperature()
            })

    """

    def __init__(
            self,
            config: DeviceConfig,
            callbacks: Callbacks = None,
            settings: ClientSettings = None
    ):
        self.user_callbacks = callbacks or Callbacks()
        self.settings = settings or ClientSettings()

        self.mqtt_config = DeviceRestApi(config.to_properties(), verbose=self.settings.verbose).get_identity_data()  # can raise DeviceConfigError

        self.mqtt = PahoClient(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=self.mqtt_config.client_id
        )
        # TODO: User configurable with defaults
        self.mqtt.reconnect_delay_set(min_delay=1, max_delay=int(self.settings.connect_timeout_secs / 2 + 1))
        self.mqtt.tls_set(certfile=config.device_cert_path, keyfile=config.device_pkey_path, ca_certs=config.server_ca_cert_path)
        self.mqtt.username = self.mqtt_config.username

        self.mqtt.on_message = self._on_mqtt_message
        self.mqtt.on_connect = self._on_mqtt_connect
        self.mqtt.on_disconnect = self._on_mqtt_disconnect
        self.mqtt.on_publish = self._on_mqtt_publish

        self.user_callbacks = callbacks or Callbacks()

    @classmethod
    def timestamp_now(cls) -> datetime:
        """ Returns the UTC timestamp that can be used to stamp telemetry records """
        return datetime.now(timezone.utc)

    def is_connected(self):
        return self.mqtt.is_connected()

    def connect(self):
        def wait_for_connection() -> bool:
            connect_timer = Timing()
            if self.settings.verbose:
                print("waiting to connect...")
            while True:
                if self.is_connected():
                    if self.settings.verbose:
                        print("MQTT connected")
                    return True
                time.sleep(0.5)
                if connect_timer.diff_now().seconds > self.settings.connect_timeout_secs:
                    print("Timed out.")
                    self.disconnect()
                    return False

        if self.is_connected():
            return

        for i in range(1, self.settings.connect_tries):
            try:
                t = Timing()
                mqtt_error = self.mqtt.connect(
                    host=self.mqtt_config.host,
                    port=8883
                )
                if mqtt_error != MQTTErrorCode.MQTT_ERR_SUCCESS:
                    print("TLS connection to the endpoint failed")
                else:
                    print("Awaiting MQTT connection establishment...")
                    self.mqtt.loop_start()
                    if wait_for_connection():
                        if self.settings.verbose:
                            print("Connected in %dms" % (t.diff_now().microseconds / 1000))
                        break
                    else:
                        continue

            except (SSLError, TimeoutError, OSError) as ex:
                # OSError includes socket.gaierror when host could not be resolved
                # This could also be temporary, so keep trying
                print("Failed to connect to host %s. Exception: %s" % (self.mqtt_config.host, str(ex)))

            backoff_ms = random.randrange(1000, self.settings.connect_backoff_max_secs * 1000)
            print("Retrying connection... Backing off for %d ms." % backoff_ms)
            # Jitter back off a random number of milliseconds between 1 and 10 seconds.
            time.sleep(backoff_ms / 1000)

        self.mqtt.subscribe(self.mqtt_config.topics.c2d, qos=1)

    def disconnect(self) -> MQTTErrorCode:
        ret = self.mqtt.disconnect()
        if self.settings.verbose:
            print("Disconnected.")
        return ret

    def send_telemetry(self, values: dict[str, TelemetryValueType], timestamp: datetime = None):
        """ Sends a single telemetry dataset. 
        If you need gateway/child functionality or need to send multiple value sets in one packet, 
        use the send_telemetry_records() method.
         
        :param TelemetryValues values:
            The name-value telemetry pairs to send. Each value can be
                - a primitive value: Maps directly to a JSON string, number or boolean
                - None: Maps to JSON null,
                - Tuple[float, float]: Used to send a lat/long geographic coordinate as decimal degrees as an
                    array of two (positive or negative) floats.
                    For example, [44.787197, 20.457273] is the geo coordinate Belgrade in Serbia,
                    where latitude 44.787197 is a positive number indicating degrees north,
                    and longitude a positive number as well, indicating degrees east.
                    Maps to JSON array of two elements.
                - Another hash with possible values above when sending an object. Maps to JSON object.
            in case when an object needs to be sent.
        :param datetime timestamp: (Optional) The timestamp corresponding to this dataset.
            If not provided, this will save bandwidth, as no timestamp will not be sent over MQTT.
             The server receipt timestamp will be applied to the telemetry values in this telemetry record.
             Supply this value (using Client.timestamp()) if you need more control over timestamps.
        """
        self.send_telemetry_records([TelemetryRecord(
            values=values,
            timestamp=timestamp
        )])

    def send_telemetry_records(self, records: list[TelemetryRecord]) -> Optional[MQTTMessageInfo]:
        """
        A complex, but more powerful way to send telemetry.
        It allows the user to send multiple sets of telemetry values
        and control the timestamp of each telemetry value set.
        Supports gateway devices with gateway-child relationship by allowing
        the user to set the parent/child unique_id ("id" in JSON)
        and tag of respective parent./child ("tg" in JSON)

        See https://docs.iotconnect.io/iotconnect/sdk/message-protocol/device-message-2-1/d2c-messages/#Device for more information.
        """

        if not self.is_connected():
            print('Message NOT sent. Not connected!')
            return None
        else:
            packet = encode_telemetry_records(records)
            ret = self.mqtt.publish(
                topic=self.mqtt_config.topics.rpt,
                qos=1,
                payload=packet
            )
            if self.settings.verbose:
                print(">", packet)
            return ret


    def send_command_ack(self, original_message: C2dCommand, status: int, message_str = None):
        """
        Send Command acknowledgement.

        :param original_message: The original message that was received in the callback.
        :param status: C2dAck.CMD_FAILED or C2dAck.CMD_SUCCESS_WITH_ACK.
        :param message_str: (Optional) For example: 'LED color now "blue"', or 'LED color "red" not supported'
        """

        if original_message.type != C2dMessage.COMMAND:
            print('Error: Called send_command_ack(), but message is not a command!')
            return
        self.send_ack(
            ack_id=original_message.ack_id,
            message_type=original_message.type,
            status=status,
            message_str=message_str,
            original_command=original_message.command_name
        )

    def send_ota_ack(self, original_message: C2dOta, status: int, message_str = None):
        """
        Send OTA acknowledgement.
        See the C2dAck comments for best practices with OTA download ACks.

        :param original_message: The original message that was received in the callback.
        :param status: For example: C2dAck.OTA_DOWNLOAD_FAILED.
        :param message_str: (Optional) For example: "Failed to unzip the OTA package".
        :param message_str: (Optional) For example: "Failed to unzip the OTA package".
        """
        if original_message.type != C2dMessage.OTA:
            print('Error: Called send_ota_ack(), but message is not an OTA request!')
            return
        self.send_ack(
            ack_id=original_message.ack_id,
            message_type=original_message.type,
            status=status,
            message_str=message_str
        )

    def send_ack(self, ack_id: str, message_type: int, status: int, message_str: str = None, original_command: str = None):
        """
        Send Command or OTA ack while having only ACK ID

        :param ack_id: Recorded ack_id from the original message.
        :param message_type: For example: C2dMessage.COMMAND or C2dMessage.OTA, .
        :param status: For example: C2dAck.CMD_FAILED or C2dAck.OTA_DOWNLOAD_DONE for command/OTA respectively.
        :param message_str: (Optional) For example: "Failed to unzip the OTA package", or 'LED color "red" not supported'
        :param original_command: (Optional) If this argument is passed,
            this command name will be printed along with any potential error messages.

        While the client should generally use send_ota_ack or send_command_ack, this method can be used in cases
        where the context of the original received message is not available (after OTA restart for example)
        """
        if not self.is_connected():
            print('Message NOT sent. Not connected!')
        elif ack_id is None or len(ack_id) == 0:
            if original_command is not None:
                print('Error: Message ACK ID missing. Ensure to set "Acknowledgement Required" in the template for command %s!' % original_command)
            else:
                print('Error: Message ACK ID missing. Ensure to set "Acknowledgement Required" in the template the command!' % original_command)
            return
        elif message_type not in (C2dMessage.COMMAND, C2dMessage.OTA):
            print('Warning: Message type %d does not appear to be a valid message type!' % message_type)  # let it pass, just in case we can still somehow send different kind of ack
        elif message_type == C2dMessage.COMMAND and not C2dAck.is_valid_cmd_status(status):
            print('Warning: Status %d does not appear to be a valid command ACK status!' % status) # let it pass, just in case there is a new status
        elif message_type == C2dMessage.OTA and not C2dAck.is_valid_ota_status(status):
            print('Warning: Status %d does not appear to be a valid OTA ACK status!' % status) # let it pass, just in case there is a new status

        packet = encode_c2d_ack(ack_id, message_type, status, message_str)
        ret = self.mqtt.publish(
            topic=self.mqtt_config.topics.ack,
            qos=1,
            payload=packet
        )
        if self.settings.verbose:
            print(">", packet)
        return ret

    def _process_c2d_message(self, topic: str, payload: str) -> bool:
        # topic is ignored for now as we only subscribe to one
        # we ought to change this once we start supporting Properties (Twin/Shadow)
        try:
            # use the simplest form of ProtocolC2dMessageJson when deserializing first and
            # convert message to appropriate json later

            decoding_result = decode_c2d_message(payload)
            generic_message = decoding_result.generic_message
            # if the user wants to handle this message type, stop processing further
            generic_cb = self.user_callbacks.generic_message_callbacks.get(generic_message.type)
            if generic_cb is not None:
                generic_cb(generic_message, decoding_result.raw_message)
                return True

            if decoding_result.command is not None:
#               TODO: Deal with runtime qualification
#               if msg.command_name == 'aws-qualification-start':
#                    self._aws_qualification_start(msg.command_args)
#                elif self.user_callbacks.command_cb is not None:
                if self.user_callbacks.command_cb is not None:
                    self.user_callbacks.command_cb(decoding_result.command)
                else:
                    if self.settings.verbose:
                        print("WARN: Unhandled command %s received!" % decoding_result.command.command_name)
            elif decoding_result.ota is not None:
                if self.user_callbacks.ota_cb is not None:
                    self.user_callbacks.ota_cb(decoding_result.ota)
                else:
                    if self.settings.verbose:
                        print("WARN: Unhandled OTA request received!")
            elif generic_message.is_fatal:
                print("Received C2D message %s from backend. Device should stop operation." % generic_message.type_description)
            elif generic_message.needs_refresh:
                print("Received C2D message %s from backend. Device should re-initialize the application." % generic_message.type_description)
            elif generic_message.heartbeat_operation is not None:
                operation_str = "start" if generic_message.heartbeat_operation == True else "stop"
                print("Received C2D message %s from backend. Device should %s heartbeat messages." % (generic_message.type_description, operation_str))
            else:
                print("C2D Message parsing for message type %d is not supported by this client. Message was: %s" % (generic_message.ct, payload))
            return True

        except C2DDecodeError:
            print('C2D Parsing Error: "%s"' % payload)
            return False

    def _on_mqtt_connect(self, mqttc: PahoClient, obj, flags, reason_code, properties):
        if self.settings.verbose:
            print("Connected. Reason Code: " + str(reason_code))

    def _on_mqtt_disconnect(self, mqttc: PahoClient, obj, flags: DisconnectFlags, reason_code: ReasonCode, properties):
        if self.user_callbacks.disconnected_cb is not None:
            # cannot send raw reason code from paho. We could technically change the backend.
            self.user_callbacks.disconnected_cb(str(reason_code), flags.is_disconnect_packet_from_server)
        else:
            print("Disconnected. Reason: %s. Flags: %s" % (str(reason_code), str(flags)))

    def _on_mqtt_message(self, mqttc: PahoClient, obj, msg):
        if self.settings.verbose:
            print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        self._process_c2d_message(msg.topic, msg.payload)

    def _on_mqtt_publish(self, mqttc: PahoClient, obj, mid, reason_code, properties):
        # print("mid: " + str(mid))
        pass

    def _aws_qualification_start(self, command_args: list[str]):
        t = Timing()

        def log_callback(client, userdata, level, buf):
            print("%d [%s]: %s" % (t.diff_now().microseconds / 1000, str(level), buf))
            t.reset(False)

        if len(command_args) >= 1:
            host = command_args[0]
            print("Starting AWS Device Qualification for", host)
            self.mqtt_config.topics.rpt = 'qualification'
            self.mqtt_config.topics.c2d = 'qualification'
            self.mqtt_config.topics.ack = 'qualification'
            self.mqtt_config.host = host
            self.mqtt.on_log = log_callback
            self.disconnect()
            while True:
                connected_time = Timing()
                if not self.is_connected():
                    print('(re)connecting to', self.mqtt_config.host)
                    self.connect()
                    connected_time.reset(False)  # reset the timer
                else:
                    if connected_time.diff_now().seconds > 60:
                        print("Stayed connected for too long. resetting the connection")
                        self.disconnect()
                        continue
                    self.send_telemetry({
                        'qualification': 'true'
                    })
                time.sleep(5)

        else:
            print("Malformed AWS qualification command. Missing command argument!")
