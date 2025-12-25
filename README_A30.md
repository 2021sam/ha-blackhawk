# A30 Audio Controller – Home Assistant Setup

This document describes how the **A30 audio controller** is wired, configured, and used with Home Assistant in this repo.

The A30 acts as the **physical audio output layer**, while Home Assistant controls *when* and *what* audio is played.

---

## Hardware Overview

- **Device:** A30 Audio Controller (Nexus Rave A30)
- **Purpose:** Route audio to ceiling / wired speakers
- **Inputs used:**
  - AUX / Line-In (from HA-controlled source)
- **Outputs used:**
  - Speaker terminals → in-ceiling speakers
- **Control method:**
  - Physical remote for input selection
  - Home Assistant controls the *source*, not the A30 itself

> The A30 is treated as a **dumb amplifier / switcher**.  
> Home Assistant owns logic and automation.

---

## Physical Wiring

### Speaker Wiring
- Ceiling speakers wired directly to A30 speaker terminals
- Polarity observed (+ / –)

### Audio Input
One of the following feeds the A30:

- **3.5mm AUX from media device** (TV, streamer, receiver)
- **HDMI / Optical via TV** (TV outputs audio → A30 AUX)

The A30 **does not need network access**.

---

## A30 Configuration (Device Side)

Using the A30 remote:

1. Power on A30
2. Select **AUX IN** (or the wired input used)
3. Set volume to a reasonable baseline (≈ 40–60%)
4. Leave A30 powered on (recommended)

> Home Assistant handles volume changes upstream via the media player.

---

## Home Assistant Audio Model

Home Assistant does **not** talk to the A30 directly.

Instead:

```

Home Assistant
↓
media_player (TV / receiver / streamer)
↓
Audio out (3.5mm / HDMI / optical)
↓
A30 AUX IN
↓
Ceiling speakers

```

### Why this model
- Stable
- No custom integration required
- A30 never blocks automations
- Easy to replace hardware later

---

## Media Player Used

Example entity:
```

media_player.family_room

```

This media player:
- Supports `media_player.play_media`
- Supports TTS
- Outputs audio to the A30 input path

---

## Playing Soundscapes (Test)

Sound files live in:
```

/config/www/soundscapes/

```

Access path:
```

/local/soundscapes/<file>.wav

````

### Manual Test Script (UI YAML editor)

```yaml
alias: TEST – A30 Sound Output
mode: single
sequence:
  - action: media_player.play_media
    target:
      entity_id: media_player.family_room
    data:
      media:
        media_content_id: /local/soundscapes/1.wav
        media_content_type: music
````

If you hear sound:

* HA → media player → A30 path is correct
* Wiring and input selection are correct

---

## Volume Strategy

* **A30:** fixed baseline volume
* **Home Assistant:** dynamic control

Example:

```yaml
- action: media_player.volume_set
  target:
    entity_id: media_player.family_room
  data:
    volume_level: 0.45
```

This avoids sudden loud playback.

---

## Common Issues

### No sound

* Verify A30 input is set to AUX
* Verify browser test works:

  ```
  http://<HA_HOST>:8123/local/soundscapes/1.wav
  ```
* Confirm media player entity actually outputs to A30

### 404 on sound file

* Files must exist in:

  ```
  /config/www/soundscapes/
  ```
* Restart HA after adding new files:

  ```bash
  ha core restart
  ```

### TTS works but WAV does not

* Use the `media:` block schema (required for this setup)
* Ensure `media_content_type` is set

---

## Design Principle

> The A30 is **replaceable hardware**.
> Home Assistant owns logic, timing, zones, and intent.

This keeps the system flexible and future-proof.

---

## Related Docs

* Main setup: `README.md`
* Soundscapes: `/www/soundscapes`
* Scripts: `scripts.yaml`

```

---
