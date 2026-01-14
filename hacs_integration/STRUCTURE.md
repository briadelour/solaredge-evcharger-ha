# HACS Integration Repository Structure

This document outlines the complete structure of the SolarEdge EV Charger HACS integration repository.

## 📁 Repository Structure

```
solaredge-evcharger-ha/
│
├── custom_components/
│   └── solaredge_evcharger/
│       ├── __init__.py                 # Integration setup & entry management
│       ├── manifest.json              # Integration metadata
│       ├── const.py                   # Constants & configuration
│       ├── config_flow.py             # UI configuration flow
│       ├── coordinator.py             # Data update coordinator & API calls
│       ├── sensor.py                  # 13 sensor entities
│       ├── binary_sensor.py           # 4 binary sensor entities
│       ├── button.py                  # 2 button entities (start/stop)
│       ├── strings.json               # English strings for UI
│       └── translations/
│           └── en.json                # English translations
│
├── docs/                              # Documentation folder (optional)
│   ├── dashboard-examples.md
│   ├── automation-examples.md
│   └── TROUBLESHOOTING.md
│
├── .github/                           # GitHub configuration (optional)
│   └── workflows/
│       └── validate.yaml              # Validation workflow
│
├── README.md                          # Main documentation
├── MIGRATION.md                       # Migration guide from YAML
├── CHANGELOG.md                       # Version history
├── hacs.json                          # HACS metadata
├── info.md                            # HACS store display
├── LICENSE                            # MIT License
└── .gitignore                         # Git ignore rules
```

## 📄 File Descriptions

### Core Integration Files

#### `custom_components/solaredge_evcharger/__init__.py`
- Integration entry point
- Handles setup and unload
- Manages coordinator lifecycle
- Registers platforms (sensor, binary_sensor, button)

**Key Functions:**
- `async_setup_entry()` - Initialize integration
- `async_unload_entry()` - Clean shutdown
- `async_reload_entry()` - Reload on options change

#### `custom_components/solaredge_evcharger/manifest.json`
```json
{
  "domain": "solaredge_evcharger",
  "name": "SolarEdge EV Charger",
  "config_flow": true,
  "dependencies": [],
  "documentation": "https://github.com/...",
  "integration_type": "device",
  "iot_class": "cloud_polling",
  "requirements": [],
  "version": "1.2.0"
}
```

#### `custom_components/solaredge_evcharger/const.py`
- Domain and platform definitions
- Configuration keys
- Default values
- API endpoints and constants
- Charger status enums
- Icons for entities

#### `custom_components/solaredge_evcharger/config_flow.py`
- UI configuration wizard
- Input validation
- Cookie authentication testing
- Options flow for updates
- Error handling

**Features:**
- Validates cookie on setup
- Auto-discovers device ID
- Allows cookie updates without restart
- Configurable scan interval and timeout

#### `custom_components/solaredge_evcharger/coordinator.py`
- Data update coordination
- API communication layer
- Session management
- Start/stop charging methods
- Error handling and retry logic

**Key Methods:**
- `_async_update_data()` - Fetch fresh data
- `async_start_charging()` - Start charging
- `async_stop_charging()` - Stop charging
- `_set_charging_state()` - Send control commands

#### `custom_components/solaredge_evcharger/sensor.py`
13 sensor entities:
1. EV Charger Status
2. EV Charger Power (kW)
3. EV Session Energy (kWh)
4. EV Session Duration
5. EV Connected Vehicle
6. EV Charger Mode
7. EV Connection Status
8. EV Session Distance (km)
9. EV Session Distance (miles)
10. EV Excess Solar Status
11. EV Session Solar Usage
12. EV Charging Schedules
13. EV Next Scheduled Charge

#### `custom_components/solaredge_evcharger/binary_sensor.py`
4 binary sensor entities:
1. EV Charger Connected
2. EV Charger Charging
3. EV Charge Schedule Enabled
4. EV Excess Solar Enabled

#### `custom_components/solaredge_evcharger/button.py`
2 button entities:
1. EV Charger Start Charging
2. EV Charger Stop Charging

#### `custom_components/solaredge_evcharger/strings.json`
UI text for:
- Configuration wizard
- Options flow
- Error messages
- Descriptions and help text

#### `custom_components/solaredge_evcharger/translations/en.json`
Same as strings.json, for UI translation system.

### Documentation Files

#### `README.md`
Main repository documentation:
- Features overview
- Installation instructions
- Configuration guide
- Quick start examples
- Troubleshooting basics

#### `MIGRATION.md`
Complete guide for migrating from YAML setup:
- Benefits of migration
- Step-by-step instructions
- Troubleshooting migration issues
- Rollback procedures
- Entity ID mapping

#### `CHANGELOG.md`
Version history and changes:
- v1.2.0 - HACS integration
- v1.1.0 - Solar/schedule monitoring
- v1.0.0 - Initial release

### HACS Files

#### `hacs.json`
HACS repository metadata:
```json
{
  "name": "SolarEdge EV Charger",
  "render_readme": true,
  "content_in_root": false,
  "homeassistant": "2023.8.0"
}
```

#### `info.md`
Displayed in HACS store:
- Brief feature overview
- Installation summary
- Requirements
- Quick links

### Configuration Files

#### `.gitignore`
Excludes:
- Python cache files
- Virtual environments
- IDE files
- Secrets and databases
- Test artifacts

#### `LICENSE`
MIT License for the project.

## 🔧 How It Works

### Data Flow

```
┌─────────────┐
│   User UI   │
└──────┬──────┘
       │ Configure
       ▼
┌─────────────────┐
│  config_flow.py │ ◄─── Validates credentials
└────────┬────────┘      Tests API connection
         │
         ▼
┌──────────────┐
│  __init__.py │ ◄─── Sets up integration
└──────┬───────┘       Creates coordinator
       │
       ▼
┌───────────────────┐
│  coordinator.py   │ ◄─── Manages API calls
└────────┬──────────┘      Updates data
         │
         ├─────────────┐
         ▼             ▼
┌──────────────┐  ┌──────────────┐
│  sensor.py   │  │button.py     │
└──────┬───────┘  └──────┬───────┘
       │                 │
       ▼                 ▼
┌─────────────────────────┐
│    Home Assistant       │
│    (Entities & States)  │
└─────────────────────────┘
```

### API Communication

```
Home Assistant
     │
     ▼
coordinator.py
     │
     ├─► GET /sites/{site_id}/devices
     │   (Fetch charger data)
     │
     └─► PUT /sites/{site_id}/devices/{device_id}/activationState
         (Start/stop charging)
```

### Cookie Management

```
Browser
   │ Extract cookie
   ▼
User Input (UI)
   │
   ▼
config_flow.py (Validate)
   │
   ▼
coordinator.py (Store & Use)
   │
   ▼
API Requests (Authenticated)
   │
   ▼
[Cookie Expires]
   │
   ▼
Options Flow (Update)
```

## 📦 Installation Process

### User Perspective

1. **Add to HACS** → Custom repository
2. **Download** → HACS installs files
3. **Restart HA** → Integration loads
4. **Add Integration** → UI configuration
5. **Done** → Entities created automatically

### Technical Process

1. **HACS copies** `custom_components/` to Home Assistant
2. **HA discovers** integration via `manifest.json`
3. **config_flow** validates credentials
4. **coordinator** fetches initial data
5. **Platforms** create entities
6. **Entities** populate with data

## 🔄 Update Process

### User Perspective

1. **HACS shows update** → Click update
2. **Restart HA** → New version loads
3. **Done** → Entities updated

### Technical Process

1. **Git pull** new code
2. **Replace files** in `custom_components/`
3. **Restart** reloads integration
4. **Coordinator** uses new code
5. **Entities** updated automatically

## 🛠️ Development Setup

### Local Testing

```bash
# Clone repository
git clone https://github.com/briadelour/solaredge-evcharger-ha
cd solaredge-evcharger-ha

# Create symlink to HA
ln -s $(pwd)/custom_components/solaredge_evcharger \
      /config/custom_components/solaredge_evcharger

# Restart HA
ha core restart
```

### File Watching

For development, create a script to sync changes:

```bash
#!/bin/bash
# sync-to-ha.sh

rsync -av --delete \
  custom_components/solaredge_evcharger/ \
  /config/custom_components/solaredge_evcharger/
```

## 📝 Creating a Release

### Version Checklist

- [ ] Update version in `manifest.json`
- [ ] Update version in `CHANGELOG.md`
- [ ] Update version in `README.md`
- [ ] Test all functionality
- [ ] Commit changes
- [ ] Create Git tag: `git tag -a v1.2.0 -m "Release 1.2.0"`
- [ ] Push: `git push origin v1.2.0`
- [ ] Create GitHub release
- [ ] Announce in Home Assistant community

## 🎯 Key Differences from YAML Setup

| Aspect | YAML Setup | HACS Integration |
|--------|------------|------------------|
| Installation | Manual file copying | HACS one-click |
| Configuration | Edit YAML files | UI wizard |
| Cookie Updates | Edit files + restart | UI + no restart |
| Entity Creation | Template sensors | Native platform |
| API Calls | Shell scripts + curl | Python aiohttp |
| Error Handling | Limited | Comprehensive |
| Updates | Manual git pull | HACS automatic |
| Debugging | Check logs manually | Native HA logging |

## 📚 Additional Resources

- [Home Assistant Integration Development](https://developers.home-assistant.io/)
- [HACS Documentation](https://hacs.xyz/)
- [Config Flow Documentation](https://developers.home-assistant.io/docs/config_entries_config_flow_handler/)
- [Data Update Coordinator](https://developers.home-assistant.io/docs/integration_fetching_data/)

## ✅ Integration Quality Checklist

Essential requirements:
- [x] Unique domain name
- [x] Config flow for UI setup
- [x] Data update coordinator
- [x] Proper device info
- [x] Unique IDs for entities
- [x] Translation strings
- [x] Error handling
- [x] Documentation
- [x] HACS compatibility
- [x] Version info in manifest

## 🎓 Understanding the Code

### For Developers

Each Python file is well-commented and follows Home Assistant conventions:
- **Type hints** for all function arguments
- **Async/await** for all I/O operations
- **Logging** at appropriate levels
- **Error handling** with try/except
- **Constants** for magic numbers/strings

### For Contributors

See each file's docstrings for detailed explanations of:
- Class purposes
- Method behaviors
- Parameter meanings
- Return values
- Exceptions raised

---

**Need help understanding the code?** Open an issue with questions!

**Found an issue?** Submit a PR with the fix!

**Have improvements?** Share them in Discussions!
