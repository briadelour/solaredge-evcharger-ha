# Migration Guide: YAML to HACS Integration

This guide will help you migrate from the YAML-based setup to the new HACS custom integration.

## 🎯 Why Migrate?

### Benefits of HACS Integration

✅ **UI Configuration** - No more YAML editing  
✅ **Easy Cookie Updates** - Update through options menu  
✅ **Automatic Updates** - HACS handles updates  
✅ **Better Reliability** - Native Home Assistant integration  
✅ **Same Entities** - All sensors work the same way  
✅ **Manual Control** - Built-in start/stop buttons  

## 📋 Before You Start

### What You'll Need

1. Your **Site ID** (same as before)
2. A fresh **browser cookie** (extract new one)
3. HACS installed in Home Assistant
4. 10-15 minutes for migration

### Backup Your Current Setup

```bash
# SSH into Home Assistant
cd /config

# Backup your files
tar -czf solaredge_backup_$(date +%Y%m%d).tar.gz \
  shell/solaredge*.sh \
  command_line.yaml \
  templates.yaml \
  shell_command.yaml
```

## 🔄 Migration Steps

### Step 1: Install HACS Integration

1. **Add Repository to HACS**
   - Open HACS
   - Click 3 dots → Custom repositories
   - Add: `https://github.com/briadelour/solaredge-evcharger-ha`
   - Category: Integration
   - Click "Add"

2. **Install Integration**
   - Search for "SolarEdge EV Charger"
   - Click "Download"
   - **Don't restart yet!**

### Step 2: Remove YAML Configuration

**Edit `configuration.yaml`:**

Remove or comment out:
```yaml
# command_line: !include command_line.yaml  # REMOVE
# template: !include templates.yaml          # REMOVE (if only used for EV charger)
# shell_command: !include shell_command.yaml # REMOVE (if only used for EV charger)
```

**Note**: If you use `templates.yaml` or `shell_command.yaml` for other integrations, only remove the EV Charger sections from those files instead.

### Step 3: Restart Home Assistant

```bash
ha core restart
```

Wait 2-3 minutes for restart.

### Step 4: Add Integration via UI

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"SolarEdge EV Charger"**
4. Enter configuration:
   - **Site ID**: Your site ID
   - **Cookie**: Fresh cookie from browser
   - **Scan Interval**: 30 (default)
   - **Timeout**: 30 (default)
5. Click **Submit**

Integration will auto-discover your charger!

### Step 5: Verify Entities

Check that entities are created:
- Go to **Developer Tools** → **States**
- Search for `ev_charger`
- Should see 19 entities

### Step 6: Update Dashboards (Optional)

Your dashboard cards should work without changes! The entity IDs are identical.

However, you can now simplify manual control buttons since they're built-in:

**Old way (YAML):**
```yaml
- type: button
  tap_action:
    action: call-service
    service: shell_command.ev_charger_start
```

**New way (built-in):**
```yaml
- type: button
  tap_action:
    action: call-service
    service: button.press
    service_data:
      entity_id: button.ev_charger_start_charging
```

### Step 7: Clean Up Old Files (Optional)

Once everything works:

```bash
cd /config

# Remove old scripts
rm shell/solaredge*.sh

# Remove YAML configs (if only used for EV charger)
# rm command_line.yaml
# rm templates.yaml  
# rm shell_command.yaml

# Remove backup after confirming everything works
# rm solaredge_backup_*.tar.gz
```

## 🔍 Verification Checklist

After migration, verify:

- [ ] All 13 sensors showing correct data
- [ ] All 4 binary sensors working
- [ ] Both control buttons present
- [ ] Dashboard cards displaying correctly
- [ ] Automations still functioning
- [ ] Can update cookie via options

## 🆘 Troubleshooting Migration Issues

### Entities Not Appearing

**Solution:**
1. Check logs: Settings → System → Logs
2. Verify cookie is valid (extract fresh one)
3. Restart Home Assistant again
4. Try removing and re-adding integration

### Old Entities Still Showing

**Solution:**
1. Go to Settings → Devices & Services → Entities
2. Filter for "unavailable" entities
3. Delete old command_line and template entities
4. Restart Home Assistant

### Duplicate Entities

**Solution:**
1. Remove YAML configuration completely
2. Restart Home Assistant
3. Old entities should become unavailable
4. Delete unavailable entities
5. Keep only the new integration entities

### Dashboard Cards Broken

**Solution:**
1. Check entity IDs match (they should be identical)
2. Update any custom entity names in lovelace
3. Clear browser cache
4. Reload dashboard

### Automations Not Triggering

**Solution:**
1. Edit automation YAML
2. Verify entity IDs match new integration
3. Test automation manually
4. Check automation logs

## 📊 Entity ID Mapping

The entity IDs remain the same:

| Entity Type | Old | New | Status |
|-------------|-----|-----|--------|
| Sensors | `sensor.ev_charger_*` | `sensor.ev_charger_*` | ✅ Same |
| Binary | `binary_sensor.ev_charger_*` | `binary_sensor.ev_charger_*` | ✅ Same |
| Buttons | `button.ev_charger_*` | `button.ev_charger_*` | ✅ Same |

**No dashboard or automation changes needed!**

## 🔄 Updating Expired Cookie

### Old Way (YAML)
```bash
nano /config/shell/solaredge_login.sh
# Edit COOKIE_VALUE="..."
# Save and restart HA
```

### New Way (HACS)
1. Settings → Devices & Services
2. SolarEdge EV Charger → Configure
3. Paste new cookie
4. Submit (no restart needed!)

## 🎯 Migration Benefits Summary

| Feature | YAML Setup | HACS Integration |
|---------|------------|------------------|
| Initial Setup | Complex (YAML + scripts) | Simple (UI wizard) |
| Cookie Update | Edit files + restart | UI + no restart |
| Updates | Manual git pull | Automatic via HACS |
| Configuration | Manual YAML | UI options |
| Reliability | Command line calls | Native coordinator |
| Error Handling | Limited | Better logging |

## 💡 Tips for Success

1. **Extract fresh cookie** before migration
2. **Keep backup** until verified working
3. **Test on non-production HA** if possible
4. **Update one dashboard** at a time
5. **Monitor logs** during migration
6. **Don't delete backups** immediately

## 🆘 Rollback Instructions

If you need to rollback:

1. **Remove HACS Integration**
   - Settings → Devices & Services
   - SolarEdge EV Charger → Delete

2. **Restore Backup**
   ```bash
   cd /config
   tar -xzf solaredge_backup_YYYYMMDD.tar.gz
   ```

3. **Restore configuration.yaml**
   ```yaml
   command_line: !include command_line.yaml
   template: !include templates.yaml
   shell_command: !include shell_command.yaml
   ```

4. **Restart Home Assistant**
   ```bash
   ha core restart
   ```

## 📚 Additional Resources

- [HACS Documentation](https://hacs.xyz/)
- [Integration README](README.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [GitHub Issues](https://github.com/briadelour/solaredge-evcharger-ha/issues)

## ✅ Post-Migration

Once migrated successfully:

- ⭐ Star the repository on GitHub
- 💬 Share feedback in Discussions
- 🐛 Report any issues
- 📝 Update documentation if needed

---

**Need Help?** Open an issue on GitHub or ask in the Discussions section!

**Migration successful?** Don't forget to delete your backup files after confirming everything works!
