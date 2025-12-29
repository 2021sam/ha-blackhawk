## 🔧 Home Assistant Entity Naming Convention (Portable)

This repository uses a **location-agnostic, numbered entity naming convention** so the **same automations and scripts can run unchanged** across multiple Home Assistant installations (different houses, rooms, or hardware).

### 🎯 Design goals

* No location names in entity IDs (`atrium`, `family_room`, etc.)
* Identical automations work everywhere
* Only entity mapping changes per installation
* UI-only metadata (Categories, Areas) is not versioned

---

## 📌 Standard Entity IDs

### Motion / Occupancy

```yaml
binary_sensor.sonoff_1_occupancy
```

---

### Lights

```yaml
light.wall_dimmer_1
light.wall_dimmer_2
light.light_1
```

---

### Media / Audio

```yaml
media_player.amp_1
```

> **Note:**
> Any powered speaker, AVR, receiver, or amp (Denon, Yamaha, WiiM, A30, etc.) is treated as an **amp**.

---

### Power Strips / Switches

Power strips may expose **multiple switch entities**.
We use a **two-level numbering scheme** to avoid collisions across locations and devices.

```yaml
switch.power_switch_1_1
switch.power_switch_1_2
switch.power_switch_1_3
switch.power_switch_1_4
switch.power_switch_1_5
```

**Meaning:**

* First number → logical device group (strip #1)
* Second number → outlet number on that device

This allows:

* Multiple power strips
* Multiple locations
* Zero renaming of automations

---

## 🧪 TEST Automations

Automations prefixed with `TEST –` are **intentionally transient** and used for:

* Verifying audio
* Testing motion sensors
* Validating entity mappings

### Categories

* TEST automations may be placed into a **UI Category** named `TEST`
* Categories are **UI-only metadata**
* Categories live in `.storage/core.category_registry`
* Categories **do NOT appear in Git**

➡️ **This is expected and correct behavior**

---

## ⚠️ Why `.storage/` Is Not in Git

The `.storage/` directory contains **runtime state**, not configuration:

| File                     | Purpose                      |
| ------------------------ | ---------------------------- |
| `core.entity_registry`   | Entity IDs ↔ device mappings |
| `core.device_registry`   | Physical devices             |
| `core.category_registry` | UI Categories                |
| `core.area_registry`     | Rooms / Areas                |
| `auth`, `http.auth`      | Credentials                  |
| `core.restore_state`     | Last known states            |

🚫 These files are:

* Installation-specific
* Hardware-specific
* Not portable
* Not safe to version

✔️ Therefore `.storage/` is intentionally **excluded from Git**

---

## 🧠 How Portability Works (Mental Model)

1. **Git tracks logic**

   * `automations.yaml`
   * `scripts.yaml`
   * `configuration.yaml`
   * README

2. **Home Assistant tracks environment**

   * Entity registry
   * Categories
   * Areas
   * Devices

3. **To deploy to a new location**

   * Clone repo
   * Map physical devices → standard entity IDs
   * Reload automations
   * Done

No branching required for locations.

---

## ✅ Recommended Repo Strategy

* **One canonical repo** (`ha-blackhawk`)
* **One master branch** for shared logic
* Optional feature branches for experimentation
* No per-location repos
* No per-location branches unless actively testing

---

If you want next, I can:

* Normalize the **Atrium PIR → Power Strip** automation to this convention (zero structure changes)
* Add a **“New Location Setup Checklist”** to the README
* Help you decide when (and when *not*) to branch

You’ve landed on a **very solid architecture** here.
