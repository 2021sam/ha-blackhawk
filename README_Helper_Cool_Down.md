Below is a **copy/paste-ready** `README_Helper.md` you can drop into your repo. It documents the **exact helpers you’re using**, how to create them in the **new HA UI (Actions, not Services)**, and where they live on disk / Git.

---

# README_Helper.md

## Purpose

This repo uses a small set of **Home Assistant Helpers** to make automations reliable and reusable.

Helpers are created in the HA UI and are **not stored as YAML files** like `automations.yaml`. Most helper definitions live in Home Assistant internal storage (`/config/.storage/`), which is **not recommended to commit to Git**.

---

## Helpers Used

### 1) Timer — Audio Cooldown

**Entity ID:** `timer.audio_cooldown`
**Name:** Audio Cooldown
**Duration:** `00:05:00` (5 minutes)
**Restore state:** OFF (unchecked) *(recommended)*

**What it does**

* Used to rate-limit audio events (TTS / WAV).
* Logic: “Only play audio when timer is `idle`.”
* Timer is started by automation at the correct time (typically at end of the OFF sequence).

**Create it**

1. Home Assistant → **Settings**
2. **Devices & services**
3. **Helpers**
4. **Create helper**
5. Choose **Timer**
6. Set:

   * Name: `Audio Cooldown`
   * Duration: `00:05:00`
   * Entity ID: `timer.audio_cooldown`
   * (Optional) Icon: `mdi:motion-sensor`
   * Leave **Restore state and time when Home Assistant starts** unchecked
7. Save

**Verify**

* Go to **Developer Tools → States**
* Search `timer.audio_cooldown`
* Confirm state shows `idle`
* Tap **Start** and confirm it counts down (state becomes `active`)

---

### 2) Input Text — Last Google Voice Post Time Spoken

**Entity ID:** `input_text.last_google_voice_post_time_spoken`

**What it does**

* Stores the last notification `post_time` we already announced.
* Prevents duplicate TTS for repeated notifications.

**Create it**

1. Home Assistant → **Settings**
2. **Devices & services**
3. **Helpers**
4. **Create helper**
5. Choose **Text**
6. Set:

   * Name: `Last Google Voice Post Time Spoken`
   * Entity ID: `input_text.last_google_voice_post_time_spoken`
   * Max length: `50` (or anything >= 20)
7. Save

**Verify**

* Developer Tools → States → `input_text.last_google_voice_post_time_spoken`
* You should be able to set a value and see it persist.

---

## Where Helpers Are Stored (Git note)

Helpers created in the UI are stored in Home Assistant’s internal storage:

* `/config/.storage/`

Common files involved:

* `core.entity_registry`
* `core.device_registry`
* `core.restore_state`

**Recommendation**

* ✅ Commit: `automations.yaml`, `scripts.yaml`, `configuration.yaml`, `packages/`, README files
* ❌ Do NOT commit: `.storage/` (it changes often and contains instance-specific IDs)

---

## Quick Troubleshooting

### Timer never becomes `idle`

* Make sure your automation is not repeatedly starting it.
* Check **Traces** on the automation to confirm when `timer.start` is called.

### TTS/WAV never plays even when timer is idle

* Confirm your condition checks exactly `state: "idle"` on `timer.audio_cooldown`
* Verify the media player is available: `media_player.amp_1`

### Duplicate Google Voice TTS

* Confirm the automation updates `input_text.last_google_voice_post_time_spoken`
* Confirm the condition compares against the input_text value (not an attribute that doesn’t exist)

---

## Optional: Documenting Old/Previous Entity IDs (without comments)

Home Assistant often strips YAML comments in the UI editor.
To preserve notes, use **description** or a **doc variable**.

Example:

```yaml
description: >
  Previous phone sensor: sensor.lm_q710_fgn_last_notification
variables:
  _doc_previous_phone_sensor: sensor.lm_q710_fgn_last_notification
```

---

If you want, I can also generate:

* `README_Entities.md` (all your standardized entity_id naming conventions)
* A “portable” approach that avoids timers by using timestamps (fully Git-defined)
