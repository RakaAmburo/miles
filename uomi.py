import asyncio
import aiohttp
from imouapi.api import ImouAPIClient
from imouapi.device import ImouDiscoverService
import os
from tools import get_logger

logger = get_logger(__name__)

APP_ID = os.getenv("IMOU_APP_ID")
APP_SECRET = os.getenv("IMOU_APP_SECRET")

async def enable_camera(sensor):
    await sensor.async_turn_off()  # closeCamera=OFF means camera ON

async def disable_camera(sensor):
    await sensor.async_turn_on()  # closeCamera=ON means camera OFF

async def control_cameras(enable: bool):
    async with aiohttp.ClientSession() as session:
        api_client = ImouAPIClient(APP_ID, APP_SECRET, session)
        devices = await ImouDiscoverService(api_client).async_discover_devices()
        logger.info(f"Devices found: {len(devices)}")

        for name, device in devices.items():
            await device.async_wakeup()
            await device.async_refresh_status()

            for sensor in device.get_all_sensors():
                sensor_name = sensor.get_name().lower()
                if "close" in sensor_name or "privacy" in sensor_name:
                    if enable:
                        await enable_camera(sensor)
                    else:
                        await disable_camera(sensor)
                    logger.info(f"Camera {name}: {'ON' if enable else 'OFF'}")

def uomis_on():
    asyncio.run(control_cameras(enable=True))

def uomis_off():
    asyncio.run(control_cameras(enable=False))