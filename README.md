# Energy Excess for Home Assistant

A small, read-only integration for [Evening Energy](https://github.com/funkmaster-dan/evening-energy). It reports forecast excess energy for your battery. It does not collect training data, configure forecasting models, or control your battery.

## Installation

1. In HACS, open **Custom repositories**, add `https://github.com/funkmaster-dan/ha-energy-excess`, and choose **Integration**.
2. Download Energy Excess and restart Home Assistant.
3. Under **Settings → Devices & services → Add integration**, select **Energy Excess**.
4. Enter your app URL, for example `http://192.168.1.204:8099`. Update the URL or polling interval later using **Configure**.

## Sensors

Six sensors provide low (conservative), middle, and high (optimistic) excess estimates in **kWh** and **battery percentage**. Energy is measured at the AC export side; percentage is the battery SoC consumed including calibrated discharge losses. `planned_peak_excess` attributes show the next modeled evening-window allowance. Live sensor values are zero outside the configured peak period.

Use the **low energy** sensor for a cautious automation allowance. Untrained models and stale inputs produce zero; an unreachable app or expired forecast makes sensors unavailable. Your automations should require an available numeric state and check `forecast_ready` and `peak_active`.

All forecasting settings and training live in the app's ordinary configuration panels. This integration has no control actions, services, or switches.

Uses Home Assistant's [DataUpdateCoordinator](https://developers.home-assistant.io/docs/integration_fetching_data/) and the [HACS integration repository layout](https://www.hacs.dev/docs/publish/integration/).
