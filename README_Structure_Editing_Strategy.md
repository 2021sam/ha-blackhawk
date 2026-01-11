Below is a **drop-in README.md** you can commit at the repo root (or `/config/README.md`).
It documents **folder structure, naming conventions, reload strategy, and VS Code / SSH workflow** exactly as you’re using it.

---

# Home Assistant Architecture & Workflow

This repo uses a **file-first, modular architecture** for Home Assistant that supports:

* location-based segregation
* safe refactors
* rapid iteration without constant reboots
* clean migration between sites

---

## 1. Folder Structure

### Automations

```
automations/
  guard/
    pir_1_on.yaml
    pir_1_off.yaml
  patio/
  deercreek/
  self_trigger/
```

**Rules**

* One folder = one logical module or location
* One file = one automation (preferred)
* Automations are **list items** (`- id: ...`)
* Automations **must have an `id:`**

Included via:

```yaml
automation: !include_dir_merge_list automations
```

---

### Scripts

```
scripts/
  atrium/
    lights_reasoned.yaml
  phone/
    google_voice_tts.yaml
  tests/
    audio.yaml
    tts.yaml
  dev/
    reload_all.yaml
```

**Rules**

* Scripts are **named mappings** (not list items)
* Group scripts by purpose or location
* No `id:` required for scripts

Included via:

```yaml
script: !include_dir_merge_named scripts
```

⚠️ Do **not** also include `scripts.yaml`.

---

### Helpers

```
helpers/
  input_select.yaml
  input_boolean.yaml
  input_datetime.yaml
  timer.yaml
  group.yaml
```

Helpers are defined in YAML **only to create entities**.
Once created, Home Assistant tracks them in `.storage`.

---

## 2. Naming Conventions

### Automations

**Format**

```
Guard <N> — <Signal> — <Transition>
```

**Examples**

```
Guard 1 — PIR — Trigger
Guard 1 — PIR — Clear
```

**Notes**

* Use **Trigger / Clear** instead of ON / OFF
* No leading zero in names (`Guard 1`, not `Guard 01`)
* Entity IDs remain stable and machine-friendly

---

### Helpers

**Format**

```
Guard <N> — <Category> — <Purpose>
```

**Categories**

* `Condition`
* `Target`
* `State`

**Examples**

```
Guard 1 — Condition — Daylight
Guard 1 — Condition — Audio Cooldown
Guard 1 — Target — Light
Guard 1 — Target — Audio
Guard 1 — State — Last Motion
```

This guarantees helpers group correctly when sorted by **Name**.

---

### Scripts

Scripts use descriptive aliases:

```
Atrium Lights ON (reasoned)
Reload Core Configs (Automations · Scripts · Helpers)
TEST – Play Soundscape – amp 1
```

Script entity_ids are **never renamed** after creation.

---

## 3. Reload vs Restart (Critical)

### Partial Reload (No Reboot)

Use when changing **logic only**.

Reloadable domains:

* automations
* scripts
* helpers (existing entities only)
* timers
* groups

Example script:

```yaml
reload_all_core_configs:
  alias: Reload Core Configs (Automations · Scripts · Helpers)
  icon: mdi:reload
  sequence:
    - action: automation.reload
    - action: script.reload
    - action: input_boolean.reload
    - action: input_select.reload
    - action: input_number.reload
    - action: input_datetime.reload
    - action: input_text.reload
    - action: timer.reload
    - action: group.reload
```

---

### Restart Required

A **full restart** is required if you:

* add or delete helpers
* add new automation files
* change `id:`
* change `configuration.yaml` includes
* remove entities
* restructure folders

**Rule of thumb**

> Reload = behavior
> Restart = existence

---

## 4. VS Code / SSH Workflow

### Recommended Workflow

1. Edit YAML in VS Code (local or Remote SSH)
2. Save files
3. Run **Reload Core Configs**
4. Test
5. Restart HA **only if entities changed**

### Configuration Validation

Always run before restart:

```
Settings → Developer Tools → YAML → Check configuration
```

CLI alternative:

```bash
python3 -m homeassistant --script check_config -c /config
```

---

## 5. Git Workflow

### Typical Status Output

```text
deleted:    automations/guard/pir_01.yaml
modified:   helpers/input_select.yaml
untracked:  automations/guard/pir_1_on.yaml
untracked:  scripts/
```

This is expected during refactors.

### Commit Guidance

Use **descriptive, architectural messages**:

```bash
git commit -m "Refactor Guard 1: split PIR trigger/clear, modular helpers, foldered scripts"
```

---

## 6. Zombie Helpers (Important)

Helpers can “come back” if:

* they are referenced by automations/scripts
* they are defined in YAML
* HA sees their entity_id during startup

**Rule**

> Remove references first.
> Then delete helpers.
> Never delete `.storage` wholesale.

---

## 7. Design Principles (Lock These In)

* Entity IDs are **machine contracts**
* Names are **human UX**
* YAML is **additive**
* Home Assistant never garbage-collects entities
* Folder structure is for **humans**, not HA

---

## 8. Recommended Extensions

* One folder per location
* One automation per file
* One reload script
* One naming grammar

This repo is now **portable, debuggable, and scalable**.

---

If you want, next I can:

* add a **Guard template folder**
* create a **site switchboard README**
* or produce a **cleanup checklist for legacy helpers**
