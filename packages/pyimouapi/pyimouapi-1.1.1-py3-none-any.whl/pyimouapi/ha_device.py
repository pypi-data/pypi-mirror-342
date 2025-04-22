import asyncio
import logging
from enum import Enum

import aiohttp

from .const import (
    BUTTON_TYPE_PARAM_VALUE,
    SWITCH_TYPE_ENABLE,
    PARAM_MOTION_DETECT,
    PARAM_STATUS,
    PARAM_STORAGE_USED,
    PARAM_NIGHT_VISION_MODE,
    PARAM_MODE,
    PARAM_CURRENT_OPTION,
    PARAM_MODES,
    PARAM_OPTIONS,
    PARAM_CHANNELS,
    PARAM_CHANNEL_ID,
    PARAM_USED_BYTES,
    PARAM_TOTAL_BYTES,
    PARAM_STREAMS,
    PARAM_HLS,
    PARAM_RESTART_DEVICE,
    PARAM_URL,
    PARAM_STREAM_ID,
    SWITCH_TYPE_ABILITY,
    ABILITY_LEVEL_TYPE,
    BUTTON_TYPE_ABILITY,
    PARAM_DEFAULT,
    PARAM_PROPERTIES,
    PARAM_REF,
    PARAM_ON,
    ERROR_CODE_LIVE_NOT_EXIST,
    ERROR_CODE_LIVE_ALREADY_EXIST,
    PARAM_PTZ,
    PARAM_ONLINE,
    PARAM_HD,
    SELECT_TYPE_ABILITY,
    SENSOR_TYPE_ABILITY,
    PARAM_TEMPERATURE_CURRENT,
    PARAM_HUMIDITY_CURRENT,
    PARAM_BATTERY,
    PARAM_ELECTRICITYS,
    PARAM_LITELEC,
    PARAM_ELECTRIC,
    PARAM_ALKELEC,
    ERROR_CODE_NO_STORAGE_MEDIUM,
    BINARY_SENSOR_TYPE_ABILITY,
    SWITCH_TYPE_REF,
    PARAM_STATE,
    PARAM_TYPE,
    PARAM_SERVICES,
    BUTTON_TYPE_REF,
    SELECT_TYPE_REF,
    PARAM_EXCEPTS,
)
from .device import ImouDeviceManager, ImouDevice
from .exceptions import RequestFailedException

_LOGGER: logging.Logger = logging.getLogger(__package__)

NUMBER_TYPE = [
    PARAM_STORAGE_USED,
    PARAM_TEMPERATURE_CURRENT,
    PARAM_HUMIDITY_CURRENT,
    PARAM_BATTERY,
]


class ImouHaDevice(object):
    def __init__(
        self,
        device_id: str,
        device_name: str,
        manufacturer: str,
        model: str,
        swversion: str,
    ):
        self._device_id = device_id
        self._device_name = device_name
        self._manufacturer = manufacturer
        self._model = model
        self._swversion = swversion
        self._switches = {}
        self._sensors = {
            PARAM_STATUS: {PARAM_STATE: DeviceStatus.OFFLINE.value},
        }
        self._binary_sensors = {}
        self._selects = {}
        self._buttons = {}
        self._channel_id = None
        self._channel_name = None
        self._product_id = None
        self._parent_product_id = None
        self._parent_device_id = None

    @property
    def device_id(self):
        return self._device_id

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def channel_name(self):
        return self._channel_name

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def model(self):
        return self._model

    @property
    def swversion(self):
        return self._swversion

    @property
    def switches(self):
        return self._switches

    @property
    def sensors(self):
        return self._sensors

    @property
    def binary_sensors(self):
        return self._binary_sensors

    @property
    def selects(self):
        return self._selects

    @property
    def buttons(self):
        return self._buttons

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def parent_product_id(self) -> str:
        return self._parent_product_id

    @property
    def parent_device_id(self) -> str:
        return self._parent_device_id

    @property
    def device_name(self) -> str:
        return self._device_name

    def set_product_id(self, product_id: str) -> None:
        self._product_id = product_id

    def set_parent_product_id(self, parent_product_id: str) -> None:
        self._parent_product_id = parent_product_id

    def set_parent_device_id(self, parent_device_id: str) -> None:
        self._parent_device_id = parent_device_id

    def __str__(self):
        return (
            f"device_id: {self._device_id}, product_id:{self._product_id},parent_device_id:{self._parent_product_id},device_name: {self._device_name}, manufacturer: {self._manufacturer}, "
            f"model: {self._model}, swversion: {self._swversion},selects:{self._selects},sensors:{self._sensors},"
            f"switches:{self._switches},binary_sensors:{self.binary_sensors},buttons:{self._buttons}"
        )

    def set_channel_id(self, channel_id):
        self._channel_id = channel_id

    def set_channel_name(self, channel_name):
        self._channel_name = channel_name


class ImouHaDeviceManager(object):
    def __init__(self, device_manager: ImouDeviceManager):
        self._delegate = device_manager

    @property
    def delegate(self):
        return self._delegate

    async def async_update_device_status(self, device: ImouHaDevice):
        """Update device status, with the updater calling every time the coordinator is updated"""
        # The device status is updated first, and if it's not online, the other entity status isn't updated
        await self._async_update_device_status(device)
        if device.sensors[PARAM_STATUS] == DeviceStatus.OFFLINE.value:
            _LOGGER.info(f"device {device.device_name} is offline,stop updating")
            return
        await asyncio.gather(
            self._async_update_device_switch_status(device),
            self._async_update_device_select_status(device),
            self._async_update_device_sensor_status(device),
            self._async_update_device_binary_sensor_status(device),
            return_exceptions=True,
        )
        _LOGGER.debug(f"update_device_status finish: {device.__str__()}")

    async def _async_update_device_switch_status(self, device: ImouHaDevice):
        """UPDATE SWITCH STATUS"""
        for switch_type, value in device.switches.items():
            if PARAM_REF in value:
                await self._async_update_device_switch_status_by_ref(
                    device, switch_type, value[PARAM_REF]
                )
            else:
                device.switches[switch_type] = any(
                    await asyncio.gather(
                        *[
                            self._async_get_device_switch_status_by_ability(
                                device, ability_type
                            )
                            for ability_type in SWITCH_TYPE_ENABLE[switch_type]
                        ],
                        return_exceptions=True,
                    )
                )

    async def _async_update_device_select_status(self, device: ImouHaDevice):
        """UPDATE SELECT STATUS"""
        for select_type, value in device.selects.items():
            if PARAM_REF in value:
                await self._async_update_device_select_status_by_ref(
                    device, select_type, value[PARAM_REF]
                )
            else:
                await self._async_update_device_select_status_by_type(
                    device, select_type
                )

    async def _async_update_device_sensor_status(self, device: ImouHaDevice):
        """UPDATE SENSOR STATUS"""
        for sensor_type, value in device.sensors.items():
            if PARAM_REF in value:
                await self._async_update_device_sensor_status_by_ref(
                    device, sensor_type, value[PARAM_REF]
                )
            elif sensor_type == PARAM_STORAGE_USED:
                await self._async_update_device_storage(device)
            elif sensor_type == PARAM_BATTERY:
                await self._async_update_device_battery(device)

    async def _async_update_device_status(self, device: ImouHaDevice):
        try:
            device_id = device.device_id
            if device.parent_device_id is not None:
                device_id = (
                    f"{device_id}_{device.parent_device_id}_{device.parent_product_id}"
                )
            data = await self.delegate.async_get_device_online_status(device_id)
            if device.channel_id is None and device.product_id is not None:
                device.sensors[PARAM_STATUS][PARAM_STATE] = self.get_device_status(
                    data[PARAM_ONLINE]
                )
            else:
                for channel in data[PARAM_CHANNELS]:
                    if channel[PARAM_CHANNEL_ID] == device.channel_id:
                        device.sensors[PARAM_STATUS][PARAM_STATE] = (
                            self.get_device_status(channel[PARAM_ONLINE])
                        )
                        break
        except Exception as e:
            _LOGGER.error(f"_async_update_device_status error:  {e}")

    async def _async_update_device_storage(self, device: ImouHaDevice):
        try:
            data = await self.delegate.async_get_device_storage(device.device_id)
            if data[PARAM_TOTAL_BYTES] != 0:
                percentage_used = int(
                    data[PARAM_USED_BYTES] * 100 / data[PARAM_TOTAL_BYTES]
                )
                device.sensors[PARAM_STORAGE_USED][PARAM_STATE] = str(percentage_used)
            else:
                device.sensors[PARAM_STORAGE_USED][PARAM_STATE] = "-2"
        except RequestFailedException as exception:
            _LOGGER.error(f"_async_update_device_storage error:  {exception}")
            if ERROR_CODE_NO_STORAGE_MEDIUM in exception.message:
                device.sensors[PARAM_STORAGE_USED][PARAM_STATE] = "-1"
            else:
                device.sensors[PARAM_STORAGE_USED][PARAM_STATE] = "-2"

    async def async_get_device_stream(
        self, device: ImouHaDevice, live_resolution: str, live_protocol: str
    ):
        try:
            return await self._async_get_device_exist_stream(
                device, live_resolution, live_protocol
            )
        except RequestFailedException as exception:
            if ERROR_CODE_LIVE_NOT_EXIST in exception.message:
                try:
                    return await self._async_create_device_stream(
                        device, live_resolution, live_protocol
                    )
                except RequestFailedException as ex:
                    if ERROR_CODE_LIVE_ALREADY_EXIST in ex.message:
                        return await self._async_get_device_exist_stream(
                            device, live_resolution, live_protocol
                        )
                    else:
                        raise exception
            else:
                raise exception

    async def _async_get_device_exist_stream(
        self, device: ImouHaDevice, resolution: str, protocol: str
    ):
        data = await self.delegate.async_get_stream_url(
            device.device_id, device.channel_id
        )
        return await self.async_get_stream_url(data, resolution, protocol)

    async def _async_create_device_stream(
        self, device: ImouHaDevice, resolution: str, protocol: str
    ):
        data = await self.delegate.async_create_stream_url(
            device.device_id, device.channel_id
        )
        return await self.async_get_stream_url(data, resolution, protocol)

    async def async_get_device_image(self, device: ImouHaDevice, wait_seconds: int):
        data = await self.delegate.async_get_device_snap(
            device.device_id, device.channel_id
        )
        if PARAM_URL in data:
            _LOGGER.debug(f"wait {wait_seconds} seconds to download a picture")
            await asyncio.sleep(wait_seconds)
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.request("GET", data[PARAM_URL])
                if response.status != 200:
                    raise RequestFailedException(
                        f"request failed,status code {response.status}"
                    )
                return await response.read()
        except Exception as exception:
            _LOGGER.error("error get_device_image %s", exception)
            return None

    async def async_get_devices(self) -> list[ImouHaDevice]:
        """
        GET A LIST OF ALL DEVICES。
        """
        devices = []
        for device in await self.delegate.async_get_devices():
            # Prioritize whether it's a video device.
            if device.channels is not None and len(device.channels) > 0:
                for channel in device.channels:
                    imou_ha_device = await self.async_build_device(device)
                    if device.product_id is not None:
                        _LOGGER.debug(
                            f"channels and product_id is not none, device_id:{device.device_id},product_id:{device.product_id}"
                        )
                        await self._async_configure_device_by_ref(imou_ha_device)
                    else:
                        _LOGGER.debug(
                            f"channels is not none, device_id:{device.device_id}"
                        )
                        self.configure_device_by_ability(
                            channel.channel_ability.split(","),
                            device.is_ipc,
                            device.device_ability.split(","),
                            imou_ha_device,
                            channel.channel_id,
                        )
                    imou_ha_device.set_channel_id(channel.channel_id)
                    imou_ha_device.set_channel_name(channel.channel_name)
                    devices.append(imou_ha_device)
            elif device.product_id is not None:
                _LOGGER.debug(
                    f"channels is none, device_id:{device.device_id},product_id:{device.product_id}"
                )
                imou_ha_device = await self.async_build_device(device)
                await self._async_configure_device_by_ref(imou_ha_device)
                devices.append(imou_ha_device)
        for device in devices:
            _LOGGER.debug(f"device is  {device.__str__()}")
        return devices

    @staticmethod
    async def async_build_device(device: ImouDevice) -> ImouHaDevice:
        imou_ha_device = ImouHaDevice(
            device.device_id,
            device.device_name,
            device.brand,
            device.device_model,
            device.device_version,
        )
        if device.product_id is not None:
            imou_ha_device.set_product_id(device.product_id)
        if device.parent_product_id is not None:
            imou_ha_device.set_parent_product_id(device.parent_product_id)
        if device.parent_device_id is not None:
            imou_ha_device.set_parent_device_id(device.parent_device_id)
        return imou_ha_device

    async def async_press_button(
        self, device: ImouHaDevice, button_type: str, duration: int, ref: str = None
    ):
        if PARAM_RESTART_DEVICE == button_type:
            await self.delegate.async_restart_device(device.device_id)
        elif PARAM_PTZ in button_type:
            await self.delegate.async_control_device_ptz(
                device.device_id,
                device.channel_id,
                BUTTON_TYPE_PARAM_VALUE[button_type],
                duration,
            )
        elif ref is not None:
            await self._async_press_button_by_ref(device, ref)

    async def async_switch_operation(
        self, device: ImouHaDevice, switch_type: str, enable: bool, ref: str = None
    ):
        if ref is not None:
            await self._async_switch_operation_by_ref(device, switch_type, enable, ref)
        elif PARAM_MOTION_DETECT == switch_type:
            await self.delegate.async_modify_device_alarm_status(
                device.device_id, device.channel_id, enable
            )
        else:
            result = await asyncio.gather(
                *[
                    self._async_set_device_switch_status_by_ability(
                        device, ability_type, enable
                    )
                    for ability_type in SWITCH_TYPE_ENABLE[switch_type]
                ],
                return_exceptions=True,
            )
            # Request all failed, consider this operation a failure
            if all(isinstance(result_item, Exception) for result_item in result):
                raise result[0]

    async def async_select_option(
        self, device: ImouHaDevice, select_type: str, option: str, ref: str = None
    ):
        if ref is not None:
            await self._async_select_option_by_ref(device, option, ref)
        if PARAM_NIGHT_VISION_MODE == select_type:
            await self.delegate.async_set_device_night_vision_mode(
                device.device_id, device.channel_id, option
            )

    async def _async_get_device_switch_status_by_ability(
        self, device: ImouHaDevice, ability_type: str
    ) -> bool:
        # Updating the interface requires capturing exceptions for two main purposes:
        # 1. To prevent the updater from failing to load due to exceptions;
        # 2. To set default values
        try:
            data = await self.delegate.async_get_device_status(
                device.device_id, device.channel_id, ability_type
            )
            return data[PARAM_STATUS] == PARAM_ON
        except Exception as e:
            _LOGGER.warning(f"_async_get_device_switch_status_by_ability fail:{e}")
            return False

    async def _async_set_device_switch_status_by_ability(
        self, device: ImouHaDevice, ability_type: str, enable: bool
    ) -> None:
        await self.delegate.async_set_device_status(
            device.device_id, device.channel_id, ability_type, enable
        )

    async def _async_update_device_select_status_by_type(
        self, device: ImouHaDevice, select_type: str
    ):
        if select_type == PARAM_NIGHT_VISION_MODE:
            try:
                await self._async_update_device_night_vision_mode(device)
            except Exception as e:
                _LOGGER.warning(f"_async_update_device_select_status_by_type fail:{e}")
                device.selects[PARAM_NIGHT_VISION_MODE] = {
                    PARAM_CURRENT_OPTION: "",
                    PARAM_OPTIONS: [],
                }

    async def _async_update_device_night_vision_mode(self, device: ImouHaDevice):
        data = await self.delegate.async_get_device_night_vision_mode(
            device.device_id, device.channel_id
        )
        if PARAM_MODE not in data or PARAM_MODES not in data:
            raise RequestFailedException("get_device_night_vision fail")
        if data[PARAM_MODE] is not None:
            device.selects[PARAM_NIGHT_VISION_MODE][PARAM_CURRENT_OPTION] = data[
                PARAM_MODE
            ]
        if data[PARAM_MODES] is not None:
            device.selects[PARAM_NIGHT_VISION_MODE][PARAM_OPTIONS] = data[PARAM_MODES]

    @staticmethod
    def configure_device_by_ability(
        channel_abilities: list[str],
        is_ipc: bool,
        device_abilities: list[str],
        imou_ha_device: ImouHaDevice,
        channel_id: str,
    ):
        # Determine which platform  entity should be added, based on the ability
        ImouHaDeviceManager.configure_switch_by_ability(
            channel_abilities, is_ipc, device_abilities, imou_ha_device, channel_id
        )
        ImouHaDeviceManager.configure_button_by_ability(
            channel_abilities, is_ipc, device_abilities, imou_ha_device, channel_id
        )
        ImouHaDeviceManager.configure_select_by_ability(
            channel_abilities, is_ipc, device_abilities, imou_ha_device, channel_id
        )
        ImouHaDeviceManager.configure_sensor_by_ability(
            channel_abilities, is_ipc, device_abilities, imou_ha_device, channel_id
        )
        ImouHaDeviceManager.configure_binary_sensor_by_ability(
            channel_abilities, is_ipc, device_abilities, imou_ha_device, channel_id
        )

    @staticmethod
    def get_device_status(origin_value: str) -> str:
        match origin_value:
            case "1":
                return DeviceStatus.ONLINE.value
            case "0":
                return DeviceStatus.OFFLINE.value
            case "4":
                return DeviceStatus.SLEEP.value
            case "3":
                return DeviceStatus.UPGRADING.value
            case _:
                _LOGGER.warning(f"Unknown device status: {origin_value}")
                return DeviceStatus.OFFLINE.value

    @staticmethod
    def configure_sensor_by_ability(
        channel_abilities: list[str],
        is_ipc: bool,
        device_abilities: list[str],
        imou_ha_device: ImouHaDevice,
        channel_id: str,
    ):
        for sensor_type, ability_list in SENSOR_TYPE_ABILITY.items():
            for ability in ability_list:
                if not ABILITY_LEVEL_TYPE.get(ability):
                    _LOGGER.warning(f"Unknown ability: {ability}, skipping...")
                    continue
                ability_level = ABILITY_LEVEL_TYPE[ability]
                match ability_level:
                    case 1:
                        # One level capability requires the device capability set to be verified
                        # and displayed only if it is a single-channel device
                        if (
                            ability in device_abilities
                            and is_ipc
                            and channel_id == "0"
                            and sensor_type not in imou_ha_device.sensors
                        ):
                            imou_ha_device.sensors[sensor_type] = {
                                PARAM_STATE: "unknown"
                                if sensor_type not in NUMBER_TYPE
                                else "0"
                            }
                    case 2:
                        if (
                            is_ipc
                            and channel_id == "0"
                            and ability in device_abilities
                            or (not is_ipc and ability in channel_abilities)
                        ) and sensor_type not in imou_ha_device.sensors:
                            imou_ha_device.sensors[sensor_type] = {
                                PARAM_STATE: "unknown"
                                if sensor_type not in NUMBER_TYPE
                                else "0"
                            }
                    case 3:
                        if (
                            (
                                is_ipc
                                and channel_id == "0"
                                and ability in device_abilities
                            )
                            or ability in channel_abilities
                        ) and sensor_type not in imou_ha_device.sensors:
                            imou_ha_device.sensors[sensor_type] = {
                                PARAM_STATE: "unknown"
                                if sensor_type not in NUMBER_TYPE
                                else "0"
                            }

    @staticmethod
    def configure_select_by_ability(
        channel_abilities: list[str],
        is_ipc: bool,
        device_abilities: list[str],
        imou_ha_device: ImouHaDevice,
        channel_id: str,
    ):
        for select_type, ability_list in SELECT_TYPE_ABILITY.items():
            for ability in ability_list:
                if not ABILITY_LEVEL_TYPE.get(ability):
                    _LOGGER.warning(f"Unknown ability: {ability}, skipping...")
                    continue
                ability_level = ABILITY_LEVEL_TYPE[ability]
                match ability_level:
                    case 1:
                        # One level capability requires the device capability set to be verified
                        # and displayed only if it is a single-channel device
                        if (
                            ability in device_abilities
                            and is_ipc
                            and channel_id == "0"
                            and select_type not in imou_ha_device.selects
                        ):
                            imou_ha_device.selects[select_type] = {
                                PARAM_CURRENT_OPTION: "",
                                PARAM_OPTIONS: [],
                            }
                    case 2:
                        if (
                            is_ipc
                            and channel_id == "0"
                            and ability in device_abilities
                            or (not is_ipc and ability in channel_abilities)
                        ) and select_type not in imou_ha_device.selects:
                            imou_ha_device.selects[select_type] = {
                                PARAM_CURRENT_OPTION: "",
                                PARAM_OPTIONS: [],
                            }
                    case 3:
                        if (
                            (
                                is_ipc
                                and channel_id == "0"
                                and ability in device_abilities
                            )
                            or ability in channel_abilities
                        ) and select_type not in imou_ha_device.selects:
                            imou_ha_device.selects[select_type] = {
                                PARAM_CURRENT_OPTION: "",
                                PARAM_OPTIONS: [],
                            }

    @staticmethod
    def configure_button_by_ability(
        channel_abilities: list[str],
        is_ipc: bool,
        device_abilities: list[str],
        imou_ha_device: ImouHaDevice,
        channel_id: str,
    ):
        for button_type, ability_list in BUTTON_TYPE_ABILITY.items():
            for ability in ability_list:
                if not ABILITY_LEVEL_TYPE.get(ability):
                    _LOGGER.warning(f"Unknown ability: {ability}, skipping...")
                    continue
                ability_level = ABILITY_LEVEL_TYPE[ability]
                match ability_level:
                    case 1:
                        # One level capability requires the device capability set to be verified
                        # and displayed only if it is a single-channel device
                        if (
                            ability in device_abilities
                            and is_ipc
                            and channel_id == "0"
                            and button_type not in imou_ha_device.buttons
                        ):
                            imou_ha_device.buttons[button_type] = {}
                    case 2:
                        if (
                            is_ipc
                            and channel_id == "0"
                            and ability in device_abilities
                            or (not is_ipc and ability in channel_abilities)
                        ) and button_type not in imou_ha_device.buttons:
                            imou_ha_device.buttons[button_type] = {}
                    case 3:
                        if (
                            (
                                is_ipc
                                and channel_id == "0"
                                and ability in device_abilities
                            )
                            or ability in channel_abilities
                        ) and button_type not in imou_ha_device.buttons:
                            imou_ha_device.buttons[button_type] = {}

    @staticmethod
    def configure_switch_by_ability(
        channel_abilities: list[str],
        is_ipc: bool,
        device_abilities: list[str],
        imou_ha_device: ImouHaDevice,
        channel_id: str,
    ):
        for switch_type, ability_list in SWITCH_TYPE_ABILITY.items():
            for ability in ability_list:
                if not ABILITY_LEVEL_TYPE.get(ability):
                    _LOGGER.warning(f"Unknown ability: {ability}, skipping...")
                    continue
                ability_level = ABILITY_LEVEL_TYPE[ability]
                match ability_level:
                    case 1:
                        # One level capability requires the device capability set to be verified
                        # and displayed only if it is a single-channel device
                        if (
                            ability in device_abilities
                            and is_ipc
                            and channel_id == "0"
                            and switch_type not in imou_ha_device.switches
                        ):
                            imou_ha_device.switches[switch_type] = {PARAM_STATE: False}
                    case 2:
                        if (
                            is_ipc
                            and channel_id == "0"
                            and ability in device_abilities
                            or (not is_ipc and ability in channel_abilities)
                        ) and switch_type not in imou_ha_device.switches:
                            imou_ha_device.switches[switch_type] = {PARAM_STATE: False}
                    case 3:
                        if (
                            (
                                is_ipc
                                and channel_id == "0"
                                and ability in device_abilities
                            )
                            or ability in channel_abilities
                        ) and switch_type not in imou_ha_device.switches:
                            imou_ha_device.switches[switch_type] = {PARAM_STATE: False}

    @staticmethod
    async def async_get_stream_url(data: dict, resolution: str, protocol: str) -> str:
        if PARAM_STREAMS in data and len(data[PARAM_STREAMS]) > 0:
            for stream in data[PARAM_STREAMS]:
                if (
                    stream[PARAM_HLS].startswith(protocol + ":")
                    and (0 if resolution == PARAM_HD else 1) == stream[PARAM_STREAM_ID]
                ):
                    _LOGGER.debug(f"get_device_stream {stream[PARAM_HLS]}")
                    return stream[PARAM_HLS]
            return data[PARAM_STREAMS][0][PARAM_HLS]
        return ""

    async def _async_configure_device_by_ref(
        self,
        imou_ha_device: ImouHaDevice,
    ):
        # query product model by product id
        product_model = await self.delegate.async_get_product_model(
            imou_ha_device.product_id
        )
        support_properties = [
            item[PARAM_REF] for item in product_model[PARAM_PROPERTIES]
        ]
        support_services = [item[PARAM_REF] for item in product_model[PARAM_SERVICES]]
        self.configure_switch_by_ref(
            support_properties, support_services, imou_ha_device
        )
        self.configure_button_by_ref(
            support_properties, support_services, imou_ha_device
        )
        self.configure_select_by_ref(
            support_properties, support_services, imou_ha_device
        )
        self.configure_sensor_by_ref(
            support_properties, support_services, imou_ha_device
        )
        self.configure_binary_sensor_by_ref(
            support_properties, support_services, imou_ha_device
        )

    @staticmethod
    def entity_need_add_to_device(
        ref: dict[any, any], properties: list[str], services: list[str], product_id: str
    ) -> bool:
        return (
            ref[PARAM_TYPE] == PARAM_PROPERTIES
            and ref[PARAM_REF] in properties
            or ref[PARAM_TYPE] == PARAM_SERVICES
            and ref[PARAM_REF] in services
        ) and (PARAM_EXCEPTS not in ref or product_id not in ref[PARAM_EXCEPTS])

    @staticmethod
    def configure_switch_by_ref(
        properties: list[str], services: list[str], imou_ha_device: ImouHaDevice
    ):
        for switch_type, ref_list in SWITCH_TYPE_REF.items():
            for ref in ref_list:
                if ImouHaDeviceManager.entity_need_add_to_device(
                    ref, properties, services, imou_ha_device.product_id
                ):
                    imou_ha_device.switches[switch_type] = {
                        PARAM_STATE: ref[PARAM_DEFAULT] == 1,
                        PARAM_REF: ref[PARAM_REF],
                    }
                    break

    @staticmethod
    def configure_button_by_ref(
        properties: list[str], services: list[str], imou_ha_device: ImouHaDevice
    ):
        for button_type, ref_list in BUTTON_TYPE_REF.items():
            for ref in ref_list:
                if ImouHaDeviceManager.entity_need_add_to_device(
                    ref, properties, services, imou_ha_device.product_id
                ):
                    imou_ha_device.buttons[button_type] = {
                        PARAM_REF: ref[PARAM_REF],
                    }
                    break

    @staticmethod
    def configure_select_by_ref(
        properties: list[str], services: list[str], imou_ha_device: ImouHaDevice
    ):
        for select_type, ref_list in SELECT_TYPE_REF.items():
            for ref in ref_list:
                if ImouHaDeviceManager.entity_need_add_to_device(
                    ref, properties, services, imou_ha_device.product_id
                ):
                    imou_ha_device.selects[select_type] = {
                        PARAM_REF: ref[PARAM_REF],
                        PARAM_OPTIONS: ref[PARAM_OPTIONS],
                        PARAM_CURRENT_OPTION: ref[PARAM_DEFAULT],
                    }
                    break

    @staticmethod
    def configure_sensor_by_ref(
        properties: list[str], services: list[str], imou_ha_device: ImouHaDevice
    ):
        for sensor_type, ref_list in SELECT_TYPE_REF.items():
            for ref in ref_list:
                if ImouHaDeviceManager.entity_need_add_to_device(
                    ref, properties, services, imou_ha_device.product_id
                ):
                    imou_ha_device.sensors[sensor_type] = {
                        PARAM_REF: ref[PARAM_REF],
                        PARAM_STATE: ref[PARAM_DEFAULT],
                    }
                    break

    @staticmethod
    def configure_binary_sensor_by_ref(
        properties: list[str], services: list[str], imou_ha_device: ImouHaDevice
    ):
        for binary_sensor_type, ref_list in SELECT_TYPE_REF.items():
            for ref in ref_list:
                if ImouHaDeviceManager.entity_need_add_to_device(
                    ref, properties, services, imou_ha_device.product_id
                ):
                    imou_ha_device.binary_sensors[binary_sensor_type] = {
                        PARAM_REF: ref[PARAM_REF],
                        PARAM_STATE: ref[PARAM_DEFAULT],
                    }
                    break

    async def _async_update_device_switch_status_by_ref(
        self, device: ImouHaDevice, switch_type: str, ref: str
    ):
        try:
            device_id = device.device_id
            # 如果是配件，需要拼接设备id
            if device.parent_product_id is not None:
                device_id = (
                    device_id
                    + "_"
                    + device.parent_device_id
                    + "_"
                    + device.parent_product_id
                )
            data = await self.delegate.async_get_iot_device_properties(
                device_id, device.product_id, [ref]
            )
            if ref in data[PARAM_PROPERTIES]:
                device.switches[switch_type][PARAM_STATE] = (
                    data[PARAM_PROPERTIES][ref] == 1
                )
        except Exception as e:
            _LOGGER.error(f"_async_update_device_switch_status_by_ref fail:{e}")

    async def _async_update_device_select_status_by_ref(
        self, device: ImouHaDevice, select_type: str, ref: str
    ):
        try:
            device_id = device.device_id
            if device.parent_product_id is not None:
                device_id = (
                    device_id
                    + "_"
                    + device.parent_device_id
                    + "_"
                    + device.parent_product_id
                )
            data = await self.delegate.async_get_iot_device_properties(
                device_id, device.product_id, [ref]
            )
            if ref in data[PARAM_PROPERTIES]:
                device.selects[select_type][PARAM_CURRENT_OPTION] = (
                    str(data[PARAM_PROPERTIES][ref])
                    if isinstance(data[PARAM_PROPERTIES][ref], int)
                    else data[PARAM_PROPERTIES][ref]
                )
        except Exception as e:
            _LOGGER.error(f"Error while updating device select status: {e}")

    async def _async_update_device_sensor_status_by_ref(
        self, device: ImouHaDevice, sensor_type: str, ref: str
    ):
        try:
            device_id = device.device_id
            # 如果是配件，需要拼接设备id
            if device.parent_product_id is not None:
                device_id = (
                    device_id
                    + "_"
                    + device.parent_device_id
                    + "_"
                    + device.parent_product_id
                )
            data = await self.delegate.async_get_iot_device_properties(
                device_id, device.product_id, [ref]
            )
            if ref in data[PARAM_PROPERTIES]:
                device.sensors[sensor_type][PARAM_STATE] = (
                    str(data[PARAM_PROPERTIES][ref])
                    if isinstance(data[PARAM_PROPERTIES][ref], int)
                    else data[PARAM_PROPERTIES][ref]
                )
        except Exception as e:
            _LOGGER.error(f"_async_update_device_sensor_status_by_ref fail:{e}")

    async def _async_press_button_by_ref(self, device: ImouHaDevice, ref: str):
        device_id = device.device_id
        if device.parent_product_id is not None:
            device_id = (
                device_id
                + "_"
                + device.parent_device_id
                + "_"
                + device.parent_product_id
            )
        await self.delegate.async_iot_device_control(
            device_id, device.product_id, ref, {}
        )

    async def _async_select_option_by_ref(
        self, device: ImouHaDevice, option: str, ref: str
    ):
        device_id = device.device_id
        # 如果是配件，需要拼接设备id
        if device.parent_product_id is not None:
            device_id = (
                device_id
                + "_"
                + device.parent_device_id
                + "_"
                + device.parent_product_id
            )
        value = (
            option
            if ref == "15400"
            and device.product_id
            in ["z76s20l415gnhhl1", "o8828zgeg1g9cfuz", "Q3YSZ54R", "BDHCWWPX"]
            else int(option)
        )
        await self.delegate.async_set_iot_device_properties(
            device_id, device.product_id, {ref: value}
        )

    async def _async_switch_operation_by_ref(
        self, device: ImouHaDevice, switch_type: str, enable: bool, ref: str
    ):
        device_id = device.device_id
        if device.parent_product_id is not None:
            device_id = (
                device_id
                + "_"
                + device.parent_device_id
                + "_"
                + device.parent_product_id
            )
        await self.delegate.async_set_iot_device_properties(
            device_id, device.product_id, {ref: 1 if enable else 0}
        )
        await asyncio.sleep(3)
        await self._async_update_device_switch_status_by_ref(device, switch_type, ref)

    @staticmethod
    def configure_binary_sensor_by_ability(
        channel_abilities: list[str],
        is_ipc: bool,
        device_abilities: list[str],
        imou_ha_device: ImouHaDevice,
        channel_id: str,
    ):
        for binary_sensor_type, ability_list in BINARY_SENSOR_TYPE_ABILITY.items():
            for ability in ability_list:
                if not ABILITY_LEVEL_TYPE.get(ability):
                    _LOGGER.warning(f"Unknown ability: {ability}, skipping...")
                    continue
                ability_level = ABILITY_LEVEL_TYPE[ability]
                match ability_level:
                    case 1:
                        # One level capability requires the device capability set to be verified
                        # and displayed only if it is a single-channel device
                        if (
                            ability in device_abilities
                            and is_ipc
                            and channel_id == "0"
                            and binary_sensor_type not in imou_ha_device.binary_sensors
                        ):
                            imou_ha_device.binary_sensors[binary_sensor_type] = {
                                PARAM_STATE: False
                            }
                    case 2:
                        if (
                            is_ipc
                            and channel_id == "0"
                            and ability in device_abilities
                            or (not is_ipc and ability in channel_abilities)
                        ) and binary_sensor_type not in imou_ha_device.binary_sensors:
                            imou_ha_device.binary_sensors[binary_sensor_type] = {
                                PARAM_STATE: False
                            }
                    case 3:
                        if (
                            (
                                is_ipc
                                and channel_id == "0"
                                and ability in device_abilities
                            )
                            or ability in channel_abilities
                        ) and binary_sensor_type not in imou_ha_device.binary_sensors:
                            imou_ha_device.binary_sensors[binary_sensor_type] = {
                                PARAM_STATE: False
                            }

    async def _async_update_device_binary_sensor_status(self, device: ImouHaDevice):
        """UPDATE SENSOR STATUS"""
        for binary_sensor_type, value in device.binary_sensors.items():
            if PARAM_REF in value:
                await self._async_update_device_binary_sensor_status_by_ref(
                    device, binary_sensor_type, value[PARAM_REF]
                )

    async def _async_update_device_binary_sensor_status_by_ref(
        self, device: ImouHaDevice, binary_sensor_type: str, ref: str
    ):
        try:
            device_id = device.device_id
            # 如果是配件，需要拼接设备id
            if device.parent_product_id is not None:
                device_id = (
                    device_id
                    + "_"
                    + device.parent_device_id
                    + "_"
                    + device.parent_product_id
                )
            data = await self.delegate.async_get_iot_device_properties(
                device_id, device.product_id, [ref]
            )
            if ref in data[PARAM_PROPERTIES]:
                device.binary_sensors[binary_sensor_type][PARAM_STATE] = (
                    data[PARAM_PROPERTIES][ref] == 1
                )
        except Exception as e:
            _LOGGER.warning(f"_async_update_device_sensor_status_by_ref fail:{e}")

    async def _async_update_device_battery(self, device):
        try:
            data = await self.delegate.async_get_device_power_info(device.device_id)
            if len(data[PARAM_ELECTRICITYS]) > 0:
                electricity = data[PARAM_ELECTRICITYS][0]
                if PARAM_LITELEC in electricity:
                    device.sensors[PARAM_BATTERY] = str(electricity[PARAM_LITELEC])
                elif PARAM_ALKELEC in electricity:
                    device.sensors[PARAM_BATTERY] = str(electricity[PARAM_ALKELEC])
                elif PARAM_ELECTRIC in electricity:
                    device.sensors[PARAM_BATTERY] = str(electricity[PARAM_ELECTRIC])
            else:
                device.sensors[PARAM_BATTERY] = "0"
        except RequestFailedException as exception:
            _LOGGER.error(f"_async_update_device_battery error:  {exception}")
            device.sensors[PARAM_BATTERY] = "0"


class DeviceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    SLEEP = "sleep"
    UPGRADING = "upgrading"
