"""Read-only excess-energy sensors from Evening Energy."""
import asyncio, logging
from datetime import timedelta
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
from .const import DOMAIN

PLATFORMS=[Platform.SENSOR]

async def async_setup_entry(hass,entry):
    options={**entry.data,**entry.options}; session=async_get_clientsession(hass)
    async def update():
        try:
            async with asyncio.timeout(20):
                async with session.get(options['url'].rstrip('/')+'/api/excess') as response:
                    response.raise_for_status(); data=await response.json()
            if not data.get('valid_until'): raise UpdateFailed('Forecast is not available yet')
            return data
        except (ValueError,KeyError) as exc: raise UpdateFailed(str(exc)) from exc
    coordinator=DataUpdateCoordinator(hass,logging.getLogger(__name__),name='Energy Excess',config_entry=entry,update_method=update,update_interval=timedelta(seconds=options.get('poll_seconds',60)))
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data=coordinator
    await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload))
    return True

async def async_reload(hass,entry): await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass,entry): return await hass.config_entries.async_unload_platforms(entry,PLATFORMS)
