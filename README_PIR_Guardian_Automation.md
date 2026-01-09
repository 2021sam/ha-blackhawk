That’s a **very good instinct** — this is exactly when a README is warranted.

Below is a **single-automation README** written for **two audiences at once**:

* **Users** (what it does, how to use helpers)
* **Future us (you + me)** when modifying it without breaking invariants

You can paste this into:

* a note
* a GitHub repo
* or even as a comment block stored alongside the automation (recommended)

---

# 📘 PIR Motion Automation – README

## Name

**PIR → Light (daylight blocks) + Power Strip + Audio + Cooldown**

---

## Purpose

This automation provides **reliable, human-friendly motion handling** with:

* Context-aware lighting
* Audible feedback with memory (“previous motion”)
* Cooldown protection
* Manual runtime overrides
* UI-safe Home Assistant design

It is intentionally conservative and **optimized for stability**, not cleverness.

---

## High-Level Behavior

### Motion ON

When motion is detected:

1. **Light**

   * Turns ON *only if*:

     * Target light helper is set
     * AND daylight blocking is OFF *or* it is nighttime
2. **Power Strip**

   * Always turns ON
3. **Audio (TTS)**

   * Speaks the **PREVIOUS motion time**
   * Only if the cooldown timer is **idle**
4. **State Tracking**

   * Updates `input_datetime.last_motion_time_1`
5. **IMPORTANT**

   * ❌ Cooldown does **NOT** start here

---

### Motion OFF (Clear)

When motion clears:

1. Waits **1 minute**
2. Confirms PIR is **still OFF**
3. **Audio (WAV)**

   * Plays soundscape
   * Only if cooldown is **idle**
4. **Shutdown**

   * Light OFF
   * Power strip OFF
5. **Cooldown**

   * ✅ Starts **ONLY HERE**
   * ✅ Starts **ONLY AT THE END**

---

## Cooldown Rules (Critical Invariant)

> **The cooldown timer must NEVER start on motion ON.**

It **must only start after PIR clears**, and **after audio/shutdown completes**.

Why:

* Prevents suppressing legitimate first motion audio
* Avoids race conditions
* Preserves psychological “confidence feedback” use-case

🚫 **Never move `timer.start` into the ON branch**

---

## Previous Motion Speech Logic

* `< 24 hours ago`

  * Speaks **time only**
  * Example:

    > “Previous motion was at 9:42 PM.”
* `≥ 24 hours ago`

  * Speaks **date + time**
  * Example:

    > “Previous motion was on March 6 at 9:42 PM.”

This is intentional and correct.

---

## Helpers Used

### Required

| Helper                              | Purpose                        |
| ----------------------------------- | ------------------------------ |
| `input_select.target_light_1`       | Selects which light to control |
| `input_select.audio_target_1`       | Selects amp or `amp_all`       |
| `input_datetime.last_motion_time_1` | Stores last motion timestamp   |
| `timer.audio_cooldown_1`            | Audio cooldown gate            |

### Optional

| Helper                                | Purpose                           |
| ------------------------------------- | --------------------------------- |
| `input_boolean.block_light_daytime_1` | Blocks light during daylight only |

---

## Audio Target Rules

`input_select.audio_target_1` supports:

* `off` → no audio
* `media_player.amp_1` → single amp
* `media_player.amp_2` → single amp
* `amp_all` / `All` / `*` → broadcast (explicit fan-out)

⚠️ **No templated lists are used**
This is required for UI-only compatibility.

---

## Daylight Behavior

* Daylight blocking applies to **light only**
* Audio and power strip are **never suppressed** by daylight
* Uses:

  ```yaml
  sun.sun == below_horizon
  ```

---

## Design Constraints (DO NOT VIOLATE)

### Editing

* ✅ **UI editor only**
* ❌ Never edit `automations.yaml` directly

### YAML / Jinja

* ❌ No list-returning variables
* ❌ No templated entity lists
* ✅ Explicit fan-out via `choose`

### Architecture

* Cooldown = **gate**, not trigger
* Light / audio / power logic are **decoupled**
* Fail-safe defaults preferred over errors

---

## Known-Good Patterns Used

* Event-driven state machine
* Debounced clear confirmation
* Post-event cooldown gate
* Context-aware actuation
* Human-confidence feedback
* Platform-aware UI design

---

## Safe Future Enhancements

(These will NOT break existing behavior)

* Night / quiet hours (audio suppression only)
* Volume normalize → speak → restore
* Zone cloning (same pattern, new helpers)
* Alternate WAV for long absence

---

## One-Sentence Summary

> **A stable, context-aware PIR automation with human-meaningful audio feedback and strictly correct cooldown semantics.**

---

If you want, next I can:

* condense this to a **1-page “operator card”**, or
* add a **CHANGELOG section** so future edits are auditable

Just say which.
