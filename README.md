# Energy Excess for Home Assistant

A small, read-only integration for [Evening Energy](https://github.com/funkmaster-dan/evening-energy). It reports forecast excess energy for your battery. It does not collect training data, configure forecasting models, or control your battery.

## Installation

1. In HACS, open **Custom repositories**, add `https://github.com/funkmaster-dan/ha-energy-excess`, and choose **Integration**.
2. Download Energy Excess and restart Home Assistant.
3. Under **Settings → Devices & services → Add integration**, select **Energy Excess**.
4. Enter your app URL, for example `http://your-server:8099`. Update the URL or polling interval later using **Configure**.

## Sensors

Twelve sensors provide low (conservative), middle and high (optimistic) estimates in kWh and battery percentage:

- **Excess energy**: stored battery kWh above forecast household needs and minimum/reserve, without a peak-window export power/time cap. Battery % is its share of capacity. Existing excess sensor IDs are preserved; their values now mean actual stored excess rather than the former peak export allowance.
- **Achievable export energy**: AC energy deliverable to the grid during the remaining/current or next peak, after losses and inverter/time limits. Its battery % is the SoC consumed including discharge losses.

Both kWh quantities are also exposed as sensor attributes (`excess_kwh`, `achievable_export_kwh`). `energy_basis` labels the units' meaning. `peak_active` independently indicates tariff timing. Update the Evening Energy app before upgrading this integration; v0.2.0 requires its separated API fields.

Untrained/incompatible models or unavailable HA inputs produce zero; an unreachable app or expired forecast makes sensors unavailable. Your existing automation remains attached to the middle excess sensor and therefore follows stored-energy excess. For an automation deliberately based on what can be exported within a peak window, use the distinct achievable-export sensor instead.

All forecasting settings and training live in the app's ordinary configuration panels. This integration has no control actions, services, or switches.

Uses Home Assistant's [DataUpdateCoordinator](https://developers.home-assistant.io/docs/integration_fetching_data/) and the [HACS integration repository layout](https://www.hacs.dev/docs/publish/integration/).
