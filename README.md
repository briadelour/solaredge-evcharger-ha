# SolarEdge EV Charger Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Compatible-blue.svg)](https://www.home-assistant.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/release/briadelour/solaredge-evcharger-ha.svg)](https://github.com/briadelour/solaredge-evcharger-ha/releases)

Monitor and **control** your SolarEdge EV Charger directly in Home Assistant using the private SolarEdge API.

This is a **custom component** that integrates seamlessly with Home Assistant through the UI - no YAML configuration required!

<div align="center">
<img width="512" height="512" alt="image" src="https://github.com/user-attachments/assets/af7c9dbb-fcb7-4aaf-bbae-54fb212385aa" />
</div>

## ✨ Features

### 📊 Comprehensive Monitoring
- **13 Sensors** tracking charger status, power, energy, duration, vehicle, mode, solar usage, schedules, and more
- **4 Binary Sensors** for connection status, charging status, schedule status, and solar status
- **2 Control Buttons** to manually start and stop charging

### ☀️ Solar Charging
- Track when Excess PV charging is enabled/disabled
- Monitor solar energy usage during charging sessions
- Real-time solar charging indicators

### 📅 Schedule Management
- View all active charging schedules with times and days
- See when your next scheduled charge will begin
- Schedule status integration with dashboard

### 🎮 Manual Control
- Start and stop charging directly from Home Assistant
- Smart conditional buttons that only appear when relevant
- Manual override of schedules and solar charging modes

### 🔧 Easy Configuration
- **UI-based setup** - no manual YAML editing!
- Update expired cookies through the options menu
- Adjust scan interval and timeout settings
- Automatic device discovery

## 📋 Prerequisites

- Home Assistant 2023.8.0 or newer
- HACS (Home Assistant Community Store) installed
- SolarEdge account with EV Charger (NOTE: this integration was developed and tested with the North American EV Charger model)
- SolarEdge monitoring portal access

## 🚀 Installation

### Method 1: HACS (Recommended)

1. **Add Custom Repository**
   - Open HACS in Home Assistant
   - Click the 3 dots in the top right
   - Select "Custom repositories"
   - Add repository URL: `https://github.com/briadelour/solaredge-evcharger-ha`
   - Category: `Integration`
   - Click "Add"

2. **Install Integration**
   - Search for "SolarEdge EV Charger" in HACS
   - Click "Download"
   - Restart Home Assistant

3. **Configure Integration**
   - Go to **Settings** → **Devices & Services**
   - Click **"+ Add Integration"**
   - Search for "SolarEdge EV Charger"
   - Follow the setup wizard (see Configuration section below)

### Method 2: Manual Installation

1. Download the `custom_components/solaredge_evcharger` folder
2. Copy to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Add integration through UI as described above

## ⚙️ Configuration

### Getting Your Credentials

#### Step 1: Get Site ID

1. Login to https://monitoring.solaredge.com
2. Look at the URL: `https://monitoring.solaredge.com/solaredge-web/p/site/XXXXXXX/#/dashboard`
3. The number `XXXXXXX` is your Site ID

#### Step 2: Extract Browser Cookie

**For Chrome:**
1. Press `F12` to open Developer Tools
2. Go to **Application** tab
3. Click **Cookies** → `monitoring.solaredge.com`
4. Find `SPRING_SECURITY_REMEMBER_ME_COOKIE`
5. Copy the **Value**

**For Firefox:**
1. Press `F12` to open Developer Tools
2. Go to **Storage** tab
3. Click **Cookies** → `monitoring.solaredge.com`
4. Find `SPRING_SECURITY_REMEMBER_ME_COOKIE`
5. Copy the **Value**

### Adding the Integration

1. **Go to Settings → Devices & Services**
2. **Click "+ Add Integration"**
3. **Search for "SolarEdge EV Charger"**
4. **Enter your credentials:**
   - **Site ID**: Your site ID from step 1
   - **Browser Cookie**: Your cookie from step 2
   - **Username/Password**: (Optional, reserved for future OAuth support)
   - **Scan Interval**: How often to update (default: 30 seconds)
   - **Timeout**: API request timeout (default: 30 seconds)
5. **Click Submit**

The integration will automatically discover your EV Charger and create all sensors!

## 🔄 Updating Expired Cookie

Cookies typically expire every 7-14 days. To update:

1. **Go to Settings → Devices & Services**
2. **Find "SolarEdge EV Charger"**
3. **Click "Configure"**
4. **Paste your new cookie**
5. **Click Submit**

No restart required!

## 📊 Available Entities

### Sensors (13)
- `sensor.ev_charger_status` - Charging/Plugged In/Not Connected
- `sensor.ev_charger_power` - Current power (kW)
- `sensor.ev_session_energy` - Energy delivered (kWh)
- `sensor.ev_session_duration` - Session duration
- `sensor.ev_connected_vehicle` - Vehicle name
- `sensor.ev_charger_mode` - Manual/Auto mode
- `sensor.ev_connection_status` - Connection details
- `sensor.ev_session_distance` - Range added (km)
- `sensor.ev_session_distance_miles` - Range added (miles)
- `sensor.ev_excess_solar_status` - Solar charging status
- `sensor.ev_session_solar_usage` - Solar energy usage
- `sensor.ev_charging_schedules` - Active schedules
- `sensor.ev_next_scheduled_charge` - Next charge time

### Binary Sensors (4)
- `binary_sensor.ev_charger_connected` - Vehicle plugged in?
- `binary_sensor.ev_charger_charging` - Currently charging?
- `binary_sensor.ev_charge_schedule_enabled` - Schedule active?
- `binary_sensor.ev_excess_solar_enabled` - Solar charging enabled?

### Buttons (2)
- `button.ev_charger_start_charging` - Start charging manually
- `button.ev_charger_stop_charging` - Stop charging manually

## 📱 Dashboard Example

```yaml
type: entities
title: EV Charger
entities:
  - sensor.ev_charger_status
  - sensor.ev_charger_power
  - sensor.ev_session_energy
  - sensor.ev_excess_solar_status
  - sensor.ev_charging_schedules
  
  # Start button (only when plugged in, not charging)
  - type: conditional
    conditions:
      - entity: binary_sensor.ev_charger_connected
        state: "on"
      - entity: binary_sensor.ev_charger_charging
        state: "off"
    row:
      type: button
      name: Start Charging
      tap_action:
        action: call-service
        service: button.press
        service_data:
          entity_id: button.ev_charger_start_charging
      icon: mdi:play-circle
  
  # Stop button (only when charging)
  - type: conditional
    conditions:
      - entity: binary_sensor.ev_charger_charging
        state: "on"
    row:
      type: button
      name: Stop Charging
      tap_action:
        action: call-service
        service: button.press
        service_data:
          entity_id: button.ev_charger_stop_charging
      icon: mdi:stop-circle
```

## 🔔 Automation Example

```yaml
automation:
  - alias: "EV Charging Started"
    trigger:
      - platform: state
        entity_id: binary_sensor.ev_charger_charging
        to: 'on'
    action:
      - service: notify.notify
        data:
          title: "⚡ EV Charging Started"
          message: >
            {{ states('sensor.ev_connected_vehicle') }} is now charging at 
            {{ states('sensor.ev_charger_power') }} kW
```

## 🔧 Troubleshooting

### Integration Won't Load

- **Check logs**: Settings → System → Logs
- **Verify cookie**: Make sure it's copied completely
- **Check Site ID**: Verify it matches your monitoring portal

### Sensors Show "Unavailable"

- **Cookie expired**: Update through options menu
- **Network issues**: Check Home Assistant can reach internet
- **API rate limit**: Increase scan interval

### Can't Find Integration

- **Restart after install**: Required for new custom components
- **Clear browser cache**: Sometimes needed after updates
- **Check HACS logs**: Settings → System → Logs, filter for HACS

### Manual Control Not Working

- **Check connection**: Vehicle must be plugged in
- **Verify mode**: Some modes may block manual control
- **Check logs**: Look for specific error messages

## 📚 Documentation

For more detailed information:
- [Complete Documentation](https://github.com/briadelour/solaredge-evcharger-ha/wiki)
- [Dashboard Examples](docs/dashboard-examples.md)
- [Automation Examples](docs/automation-examples.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 Changelog

### v1.2.2 (2026-07-31)
- BUG FIX: More stable reading for active charge session & unconfirmed support for 22kw SolarEdge ONE EV Charger (outside of North America)

### v1.2.1 (2026-07-25)
- BUG FIX: Configuration button not working

### v1.2.0 (2026-01-15)
- ✨ **NEW**: Full HACS integration with UI configuration
- ✨ **NEW**: Update cookies through options menu
- ✨ **NEW**: Automatic device discovery
- ✨ **NEW**: No YAML configuration required
- 🐛 All previous features maintained from v1.1.0

### v1.1.0 (2026-01-13)
- ✨ Added Excess Solar monitoring
- ✨ Added Schedule management
- ✨ Added Manual start/stop control
- 🐛 Fixed power display (kW instead of W)

### v1.0.0 (2026-01-10)
- Initial release with basic monitoring

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This integration uses SolarEdge's private/undocumented API. It is not officially supported by SolarEdge and may break at any time if they change their API. Use at your own risk.

This integration is not affiliated with, endorsed by, or connected to SolarEdge Technologies Ltd.

## 🙏 Acknowledgments

- Thanks to the Home Assistant community
- Thanks to HACS for making custom integrations easy
- Thanks to all contributors and testers

---

**Made with ❤️ for the Home Assistant community**

If this integration helped you, consider giving it a ⭐ on GitHub!
