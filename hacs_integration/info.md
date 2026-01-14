# SolarEdge EV Charger

Monitor and control your SolarEdge EV Charger directly in Home Assistant!

## Features

✨ **19 Entities Total**
- 13 Sensors (power, energy, status, solar, schedules, etc.)
- 4 Binary Sensors (connected, charging, schedule, solar)
- 2 Control Buttons (start/stop charging)

☀️ **Solar Monitoring**
- Track excess solar charging status
- Monitor solar energy usage
- Real-time solar indicators

📅 **Schedule Management**
- View active charging schedules
- See next scheduled charge time
- Complete schedule integration

🎮 **Manual Control**
- Start/stop charging from HA
- Smart conditional buttons
- Override schedules

🔧 **Easy Setup**
- UI-based configuration
- No YAML required
- Update cookies via options menu

## Installation

1. Add this repository as a custom repository in HACS
2. Search for "SolarEdge EV Charger"
3. Install and restart Home Assistant
4. Add via Settings → Devices & Services
5. Enter your Site ID and browser cookie

## Requirements

- Home Assistant 2023.8.0+
- SolarEdge monitoring portal access
- EV Charger connected to SolarEdge system

## Configuration

You'll need:
1. **Site ID** - From your SolarEdge monitoring URL
2. **Browser Cookie** - Extract from Developer Tools (F12)

Cookie expires every 7-14 days and can be updated through the options menu!

## Support

- [Full Documentation](https://github.com/briadelour/solaredge-evcharger-ha)
- [Report Issues](https://github.com/briadelour/solaredge-evcharger-ha/issues)
- [Discussions](https://github.com/briadelour/solaredge-evcharger-ha/discussions)
