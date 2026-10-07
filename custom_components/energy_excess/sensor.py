from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy, PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.util import dt as dt_util
from .const import DOMAIN

async def async_setup_entry(hass,entry,async_add_entities):
    async_add_entities(EnergySensor(entry,scenario,percent,metric) for metric in ('excess','achievable_export') for scenario in ('low','middle','high') for percent in (False,True))

class EnergySensor(CoordinatorEntity,SensorEntity):
    _attr_has_entity_name=True
    _attr_state_class=SensorStateClass.MEASUREMENT
    _attr_icon='mdi:battery-arrow-up-outline'
    def __init__(self,entry,scenario,percent,metric='excess'):
        super().__init__(entry.runtime_data)
        self.scenario=scenario; self.percent=percent; self.metric=metric
        # Existing excess entity identities remain stable for automations.
        prefix='' if metric=='excess' else 'achievable_export_'
        self._attr_unique_id=f'{entry.entry_id}_{prefix}{scenario}_{"percent" if percent else "kwh"}'
        label='Excess' if metric=='excess' else 'Achievable export'
        self._attr_name=f'{label} {scenario} {"battery percent" if percent else "energy"}'
        self._attr_native_unit_of_measurement=PERCENTAGE if percent else UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class=None if percent else SensorDeviceClass.ENERGY
        self._attr_suggested_display_precision=2
        self._attr_device_info=DeviceInfo(identifiers={(DOMAIN,entry.entry_id)},name='Evening Energy',manufacturer='Home experiment',model='Energy excess and peak export forecast',configuration_url=entry.data['url'])
    @property
    def available(self):
        data=self.coordinator.data or {}
        expiry=dt_util.parse_datetime(data.get('valid_until',''))
        return super().available and expiry is not None and expiry>dt_util.utcnow()
    @property
    def native_value(self):
        data=self.coordinator.data or {}
        if not data.get('ready'):return 0
        return round(data.get(self.metric+('_percent' if self.percent else '_kwh'),{}).get(self.scenario,0),2)
    @property
    def extra_state_attributes(self):
        d=self.coordinator.data or {}
        return {'forecast_ready':d.get('ready',False),'peak_active':d.get('peak_active',False),'energy_basis':'Stored battery energy' if self.metric=='excess' else 'AC grid export energy','excess_kwh':d.get('excess_kwh',{}).get(self.scenario,0),'achievable_export_kwh':d.get('achievable_export_kwh',{}).get(self.scenario,0),'forecast_updated_at':d.get('updated_at'),'valid_until':d.get('valid_until'),'horizon_hours':d.get('horizon_hours'),'confidence':d.get('confidence'),'warnings':d.get('warnings',[])}
