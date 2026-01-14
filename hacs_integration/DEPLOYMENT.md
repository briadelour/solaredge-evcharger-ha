# HACS Integration Deployment Guide

This guide will help you deploy the complete HACS custom integration to your GitHub repository.

## 📦 What You Have

A complete HACS custom integration with:
- ✅ UI-based configuration (no YAML!)
- ✅ 19 entities (13 sensors, 4 binary sensors, 2 buttons)
- ✅ Cookie update via options menu
- ✅ Manual charging control
- ✅ Solar & schedule monitoring
- ✅ Complete documentation
- ✅ Migration guide from YAML setup

## 🗂️ Repository Structure

```
hacs_integration/
├── custom_components/
│   └── solaredge_evcharger/
│       ├── __init__.py              ✅ Main integration
│       ├── manifest.json            ✅ Metadata
│       ├── const.py                 ✅ Constants
│       ├── config_flow.py           ✅ UI configuration
│       ├── coordinator.py           ✅ API & data
│       ├── sensor.py                ✅ 13 sensors
│       ├── binary_sensor.py         ✅ 4 binary sensors
│       ├── button.py                ✅ 2 buttons
│       ├── strings.json             ✅ UI text
│       └── translations/
│           └── en.json              ✅ Translations
│
├── README.md                        ✅ Main docs
├── MIGRATION.md                     ✅ YAML→HACS guide
├── STRUCTURE.md                     ✅ Code overview
├── hacs.json                        ✅ HACS metadata
├── info.md                          ✅ HACS store display
├── LICENSE                          ⚠️ YOU NEED TO ADD
├── .gitignore                       ✅ Git ignore
└── CHANGELOG.md                     ⚠️ YOU NEED TO CREATE
```

## 🚀 Deployment Steps

### Step 1: Create GitHub Repository

```bash
# On GitHub
1. Create new repository: "solaredge-evcharger-ha"
2. Make it public
3. DO NOT initialize with README
4. Copy the repository URL
```

### Step 2: Prepare Local Files

```bash
# Create new directory
mkdir solaredge-evcharger-ha
cd solaredge-evcharger-ha

# Initialize git
git init
git branch -M main
```

### Step 3: Copy Integration Files

Copy the contents of the `hacs_integration` folder:

```bash
# Copy all files from hacs_integration/
cp -r /path/to/hacs_integration/* .

# Verify structure
ls -la
# Should show:
# - custom_components/
# - README.md
# - MIGRATION.md
# - hacs.json
# - etc.
```

### Step 4: Update Placeholder Text

**Replace `briadelour` in these files:**

1. **manifest.json** (line 3)
   ```json
   "codeowners": ["@YOUR_GITHUB_USERNAME"],
   ```

2. **manifest.json** (line 6)
   ```json
   "documentation": "https://github.com/YOUR_GITHUB_USERNAME/solaredge-evcharger-ha",
   ```

3. **manifest.json** (line 9)
   ```json
   "issue_tracker": "https://github.com/YOUR_GITHUB_USERNAME/solaredge-evcharger-ha/issues",
   ```

4. **README.md** (multiple places - search for briadelour)

5. **info.md** (search for briadelour)

6. **MIGRATION.md** (search for briadelour)

**Quick replace command:**
```bash
# Replace all at once (Mac/Linux)
find . -type f -name "*.md" -o -name "*.json" | xargs sed -i '' 's/briadelour/your_actual_username/g'

# For Linux (without empty string)
find . -type f -name "*.md" -o -name "*.json" | xargs sed -i 's/briadelour/your_actual_username/g'
```

### Step 5: Add License File

```bash
# Copy MIT License
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 YOUR NAME

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

### Step 6: Create CHANGELOG

```bash
cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-01-15

### Added
- ✨ Full HACS integration with UI configuration
- ✨ Update cookies through options menu without restart
- ✨ Automatic device discovery
- ✨ Native Home Assistant coordinator
- ✨ No YAML configuration required

### Changed
- 🔄 Migrated from YAML-based setup to custom integration
- 🔄 Improved error handling and logging
- 🔄 Better session management

### Maintained
- ✅ All 13 sensors from v1.1.0
- ✅ All 4 binary sensors
- ✅ Manual start/stop control
- ✅ Solar monitoring
- ✅ Schedule management

## [1.1.0] - 2026-01-13

### Added
- ✨ Excess Solar monitoring (status & usage)
- ✨ Schedule management (active schedules & next charge)
- ✨ Manual start/stop charging control
- ✨ 4 new sensors for enhanced monitoring

### Fixed
- 🐛 Power sensor displaying W instead of kW

## [1.0.0] - 2026-01-10

### Added
- Initial release
- Basic sensor monitoring via SolarEdge API
- Template sensors for charger states
- Binary sensors for status tracking
- Shell script-based API access
EOF
```

### Step 7: Commit and Push

```bash
# Stage all files
git add .

# Create first commit
git commit -m "Initial commit: HACS custom integration v1.2.0

- Full UI configuration
- 19 entities (13 sensors, 4 binary sensors, 2 buttons)
- Solar and schedule monitoring
- Manual charging control
- Cookie update via options
- Complete documentation"

# Add remote
git remote add origin https://github.com/briadelour/solaredge-evcharger-ha.git

# Push to GitHub
git push -u origin main

# Create version tag
git tag -a v1.2.0 -m "Version 1.2.0 - HACS Integration"
git push origin v1.2.0
```

### Step 8: Create GitHub Release

1. Go to your repository on GitHub
2. Click **"Releases"** → **"Create a new release"**
3. **Tag**: `v1.2.0`
4. **Title**: `Version 1.2.0 - HACS Custom Integration`
5. **Description**:

```markdown
## 🎉 Initial HACS Release - v1.2.0

This is the first release of the SolarEdge EV Charger as a full HACS custom integration!

### ✨ What's New

**HACS Integration**
- 🔧 UI-based configuration (no YAML required!)
- ⚙️ Update cookies through options menu
- 🔄 Automatic device discovery
- 📦 One-click installation via HACS

**Features**
- 📊 13 Sensors (power, energy, status, solar, schedules, etc.)
- 🔘 4 Binary Sensors (connected, charging, schedule, solar)
- 🎮 2 Control Buttons (start/stop charging)
- ☀️ Solar charging monitoring
- 📅 Schedule management
- 🎯 Manual charging control

### 📦 Installation

1. Add custom repository to HACS:
   - Repository: `briadelour/solaredge-evcharger-ha`
   - Category: Integration

2. Search for "SolarEdge EV Charger" in HACS

3. Install and restart Home Assistant

4. Add via Settings → Devices & Services

### 📚 Documentation

- [Installation Guide](README.md)
- [Migration from YAML](MIGRATION.md)
- [Code Structure](STRUCTURE.md)

### 🔧 Requirements

- Home Assistant 2023.8.0+
- SolarEdge monitoring portal access
- EV Charger connected to SolarEdge

### ⚠️ Migration from v1.1.0

If you're using the YAML-based setup, see [MIGRATION.md](MIGRATION.md) for complete upgrade instructions.

---

**Full Changelog**: Initial release
```

6. Click **"Publish release"**

## ✅ Post-Deployment Checklist

After pushing to GitHub:

- [ ] Repository is public
- [ ] All files uploaded correctly
- [ ] briadelour replaced everywhere
- [ ] LICENSE file present
- [ ] CHANGELOG.md created
- [ ] README.md renders correctly
- [ ] v1.2.0 tag created
- [ ] GitHub release published
- [ ] Repository description set
- [ ] Topics added (home-assistant, hacs, solaredge, ev-charger)

### Add Repository Topics

On GitHub repository page:
1. Click ⚙️ next to "About"
2. Add topics:
   - `home-assistant`
   - `hacs`
   - `custom-component`
   - `solaredge`
   - `ev-charger`
   - `home-automation`

### Update Repository Description

Set description to:
```
Monitor and control your SolarEdge EV Charger in Home Assistant. UI configuration, solar tracking, schedule management, and manual control.
```

## 🧪 Testing Your HACS Integration

### Test Installation

1. **Add to HACS**
   - HACS → ⋮ → Custom repositories
   - Add your repository URL
   - Category: Integration

2. **Install**
   - Search for "SolarEdge EV Charger"
   - Click Download
   - Restart Home Assistant

3. **Configure**
   - Settings → Devices & Services
   - Add Integration
   - Enter credentials
   - Verify entities created

4. **Test Functions**
   - Check all sensors update
   - Test start button
   - Test stop button
   - Update cookie via options

## 📣 Announcing Your Integration

### Home Assistant Community

Post in [Share Your Projects](https://community.home-assistant.io/c/projects/31):

```markdown
**SolarEdge EV Charger - Now Available as HACS Integration! 🎉**

I've converted my SolarEdge EV Charger integration into a full HACS custom component!

✨ Features:
- UI configuration (no YAML!)
- 19 entities for complete monitoring
- Solar charging tracking
- Schedule management
- Manual start/stop control
- Easy cookie updates

🔗 GitHub: [your-link]
📦 Installation: HACS → Custom Repositories

Feedback welcome! 🙏
```

### Reddit r/homeassistant

```markdown
[PROJECT] SolarEdge EV Charger - HACS Integration

I've released a HACS custom integration for SolarEdge EV Chargers!

Features:
- UI-based setup
- 19 monitoring entities
- Solar tracking
- Manual control
- Easy cookie management

GitHub: [link]

Open to feedback and contributions!
```

## 🐛 Handling Issues

### Expected First Issues

Users will likely report:
1. Cookie extraction confusion
2. Site ID not found
3. Multiple chargers
4. API rate limits

**Be prepared with:**
- Clear cookie extraction guide
- Screenshots for different browsers
- Multi-charger documentation
- Rate limit recommendations

### Issue Templates

Create `.github/ISSUE_TEMPLATE/` with:
- `bug_report.md`
- `feature_request.md`

## 📊 Repository Stats

After launch, monitor:
- ⭐ Stars
- 👁️ Watchers
- 🍴 Forks
- 📊 HACS installs (HACS analytics)

## 🎯 Next Steps

After successful deployment:

1. **Monitor Issues** - Respond to user questions
2. **Gather Feedback** - Improve based on usage
3. **Plan Updates** - Track feature requests
4. **Community Engagement** - Help users succeed

## 🔄 Future Updates

To release updates:

```bash
# Make changes
git add .
git commit -m "Description of changes"

# Update version in manifest.json
# Update CHANGELOG.md

# Tag new version
git tag -a v1.2.1 -m "Version 1.2.1"
git push origin main --tags

# Create GitHub release
```

HACS will automatically detect new releases!

## 💡 Tips for Success

1. **Respond quickly** to initial issues
2. **Document everything** users ask about
3. **Test thoroughly** before releasing
4. **Version carefully** - follow semver
5. **Engage community** - be welcoming

## 🆘 Help Resources

- [HACS Documentation](https://hacs.xyz/)
- [HA Integration Docs](https://developers.home-assistant.io/)
- [Discord: Home Assistant](https://discord.gg/home-assistant)
- [Community Forum](https://community.home-assistant.io/)

---

## ✅ Final Verification

Before announcing:

```bash
# Check repository
- [ ] All files present
- [ ] No broken links
- [ ] README clear
- [ ] Examples work
- [ ] License correct

# Test installation
- [ ] HACS finds it
- [ ] Downloads correctly
- [ ] Integration loads
- [ ] Entities created
- [ ] Functions work

# Documentation
- [ ] Installation clear
- [ ] Configuration explained
- [ ] Troubleshooting present
- [ ] Examples provided
```

---

**Ready to deploy? Follow these steps and you'll have a professional HACS integration!**

**Questions?** Review the documentation or open an issue!

**Success?** Don't forget to announce it to the community! 🎉
