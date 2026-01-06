# Whole Home Audio – Home Assistant

## Purpose

This setup allows **motion alerts, TTS announcements, and sound effects** to play through:

* a **single amp**, or
* **both amps at once** (“whole home audio”)

The routing is **user-selectable** via a dropdown and does **not require editing automations**.

---

## Core Concept

Audio output is abstracted behind a **media player group** and an **input_select**:

* Automations do **not** hardcode speakers
* Users choose where audio plays
* The system stays simple and debuggable

---

## Components

### Media Players

* `media_player.amp_1` – Downstairs A30 (currently installed)
* `media_player.amp_2` – Upstairs A30 (optional / future)

---

### Media Player Group

**Whole Home Audio**

* Entity ID:
  `media_player.whole_home_audio`

**Members:**

* `media_player.amp_1`
* `media_player.amp_2` (only add when it exists)

> A one-member group is valid and safe.

---

### Audio Routing Helper

**Input Select**

* Name: `Audio Output`
* Entity ID:
  `input_select.audio_target_1`

**Options:**

* `media_player.whole_home_audio`
* `media_player.amp_1`
* `media_player.amp_2`

This dropdown controls **where all audio plays**.

---

## How Automations Use Audio

All automations reference **only**:

```
{{ states('input_select.audio_target_1') }}
```

They do **not** reference amps directly.

This allows:

* easy user control
* no YAML edits
* safe future expansion

---

## Normal Operation

* Default selection:
  **Whole Home Audio**
* Motion detected → audio plays through selected target
* Power strip and lights follow motion logic
* Cooldown timer prevents repeated announcements

---

## Known Limitation (By Design)

If **Whole Home Audio** is selected but:

* only `amp_1` exists
* or `amp_2` is offline

Audio may not play.

### Fix (intentional manual control)

Set:

```
Audio Output → media_player.amp_1
```

This restores sound immediately.

> This is preferred over complex auto-fallback logic.

---

## Why This Design Was Chosen

* Simple > clever
* Easy to debug
* Easy to explain
* Easy to extend later

Complex fallback logic was intentionally avoided.

---

## When to Revisit

Revisit this design **only if**:

* both amps are permanently installed
* you want automatic failover
* or you add more zones (patio, garage, etc.)

Until then: **this is the correct level of complexity**.

---

## Summary

* One dropdown controls all audio
* One group represents “whole home”
* Automations stay clean
* System is stable and understandable

**Ship it.**
