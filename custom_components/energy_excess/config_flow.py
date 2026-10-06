import asyncio
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, DEFAULT_URL

def schema(values):
    return vol.Schema({vol.Required('url',default=values.get('url',DEFAULT_URL)):str,vol.Required('poll_seconds',default=values.get('poll_seconds',60)):vol.All(vol.Coerce(int),vol.Range(min=15,max=3600))})

async def check(hass,values):
    values['url']=values['url'].rstrip('/')
    async with asyncio.timeout(15):
        async with async_get_clientsession(hass).get(values['url']+'/api/health') as response:
            response.raise_for_status()
            if (await response.json()).get('status')!='ok': raise ValueError('Unexpected app response')

class EnergyExcessConfigFlow(config_entries.ConfigFlow,domain=DOMAIN):
    VERSION=1
    async def async_step_user(self,user_input=None):
        errors={}
        if user_input:
            try:
                await check(self.hass,user_input)
                await self.async_set_unique_id(user_input['url'])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title='Evening Energy',data=user_input)
            except Exception: errors['base']='cannot_connect'
        return self.async_show_form(step_id='user',data_schema=schema(user_input or {}),errors=errors)
    @staticmethod
    @callback
    def async_get_options_flow(config_entry): return EnergyExcessOptionsFlow()

class EnergyExcessOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self,user_input=None):
        errors={}
        if user_input:
            try:
                await check(self.hass,user_input)
                return self.async_create_entry(title='',data=user_input)
            except Exception: errors['base']='cannot_connect'
        values={**self.config_entry.data,**self.config_entry.options}
        return self.async_show_form(step_id='init',data_schema=schema(values),errors=errors)
