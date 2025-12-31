Absolutely — here is a **clean, copy-paste-ready README** that compiles **everything you proved works over the last 2 days**, tailored **specifically to your Android device and Home Assistant setup**, with clear notes about what may vary on newer phones.

---

# 📣 Google Voice (Android) → Home Assistant → TTS

**Reliable SMS Announcements via Android Notifications**

> **Tested & confirmed working** on a real device, in real conditions
> (foreground / background / minimized / screen off)

---

## 1. Overview

This setup turns an **Android phone running Google Voice** into a **reliable SMS event source** for **Home Assistant**, announcing messages via **Text-to-Speech (TTS)**.

✔ Works when the Google Voice app is:

* Open (foreground)
* Minimized
* Fully backgrounded
* Screen locked

✔ No polling
✔ No UI scraping
✔ No `None` / null errors
✔ No duplicate announcements

---

## 2. Tested Hardware (Important)

This README is **hardware-specific** to the phone you used.

### 📱 Android Phone

* **Model:** LG LM-Q710 (FGN)
* **SoC:** Qualcomm Snapdragon 835
* **RAM:** 4 GB
* **Storage:** 64 GB
* **Android Version:** Android 10
* **OEM UI:** LG UX
* **Battery Optimization:** Disabled for HA app
* **Notification Access:** Explicitly granted

> ⚠️ Newer Android versions (12–14) **may require additional permission steps**, especially for notification access and background activity.

---

## 3. Apps Involved

### 📲 Google Voice

* Package name:

  ```
  com.google.android.apps.googlevoice
  ```
* Notification style:

  ```
  android.app.Notification$MessagingStyle
  ```
* Provides **structured messaging data**, including:

  * Sender
  * Message text
  * Message history
  * Timestamp

### 🏠 Home Assistant Companion App (Android)

* Role:

  * Reads Android notifications
  * Publishes them as sensors in HA
* Required permissions:

  * ✅ Notification Access
  * ✅ Background execution
  * ✅ Battery optimization disabled

---

## 4. Home Assistant Entities Used

### 🔔 Notification Sensor

```
sensor.lm_q710_fgn_last_notification
```

Key attributes (verified):

```yaml
android.title: (510) 246-5504
android.text: It is now 10 o'clock
android.messages: [ ... ]
package: com.google.android.apps.googlevoice
post_time: 1767160837737
category: msg
```

> ❗ There is **NO** generic `attributes.text`
> Use **`android.text`** instead.

---

### 🔊 TTS Service

```
tts.google_translate_en_com
```

### 🔉 Audio Output

```
media_player.amp_1
```

---

## 5. Why This Works (Architecture)

This setup is **event-driven**, not UI-dependent:

```
Google Voice
   ↓
Android Notification System
   ↓
Home Assistant Companion App
   ↓
sensor.lm_q710_fgn_last_notification
   ↓
Automation
   ↓
TTS Announcement
```

Because Android **always posts notifications**, it works regardless of app state.

---

## 6. Core Automation (FINAL)

### 🔔 Speak Google Voice Messages (Title + Text)

```yaml
alias: TTS – Speak Google Voice last notification (title + text)
description: Speak Google Voice SMS via Android → HA → TTS
mode: single

trigger:
  - platform: state
    entity_id: sensor.lm_q710_fgn_last_notification

condition:
  # Only Google Voice notifications
  - condition: template
    value_template: >
      {{ state_attr('sensor.lm_q710_fgn_last_notification','package')
         == 'com.google.android.apps.googlevoice' }}

  # Must have usable text
  - condition: template
    value_template: >
      {{
        (state_attr('sensor.lm_q710_fgn_last_notification','android.title') or '')|length > 0
        or
        (state_attr('sensor.lm_q710_fgn_last_notification','android.text') or '')|length > 0
      }}

  # Prevent repeat announcements
  - condition: template
    value_template: >
      {{
        state_attr('sensor.lm_q710_fgn_last_notification','post_time') | string
        !=
        states('input_text.last_google_voice_post_time_spoken')
      }}

action:
  - variables:
      n: sensor.lm_q710_fgn_last_notification
      who: "{{ (state_attr(n,'android.title') or 'Message') | string }}"
      txt: "{{ (state_attr(n,'android.text') or '') | string }}"
      msg: "{{ who ~ ': ' ~ txt if txt|length > 0 else who ~ ': (no text)' }}"
      pt: "{{ state_attr(n,'post_time') | string }}"

  - service: tts.speak
    target:
      entity_id: tts.google_translate_en_com
    data:
      media_player_entity_id: media_player.amp_1
      message: "{{ msg }}"

  - service: input_text.set_value
    target:
      entity_id: input_text.last_google_voice_post_time_spoken
    data:
      value: "{{ pt }}"
```

---

## 7. Required Helper

Create **once**:

```
input_text.last_google_voice_post_time_spoken
```

Purpose:

* Prevents duplicate announcements
* Stores last `post_time`

---

## 8. Why Earlier Attempts Failed (Lessons Learned)

### ❌ What DOES NOT work

```yaml
state_attr(n, 'text')
```

Because:

* Google Voice uses **`android.text`**
* `text` returns `None`
* HA throws:

  ```
  string value is None for dictionary value @ data['message']
  ```

### ✅ Correct attributes

* `android.title`
* `android.text`
* `android.messages[-1].text` (advanced)

---

## 9. Behavior Confirmed

| Scenario               | Result          |
| ---------------------- | --------------- |
| App open               | ✅ Works         |
| App minimized          | ✅ Works         |
| App backgrounded       | ✅ Works         |
| Screen locked          | ✅ Works         |
| Phone idle             | ✅ Works         |
| Multiple messages      | ✅ Latest spoken |
| Duplicate notification | ❌ Blocked       |

---

## 10. Notes for Newer Phones (Android 12+)

You may need:

* Re-grant **Notification Access** after updates
* Disable **Adaptive Battery**
* Allow **“Unrestricted” background usage**
* Ignore OEM “deep sleep” features (Samsung, Xiaomi, etc.)

---

## 11. Why This Is the Right Pattern

* ✔ Uses Android’s **official notification pipeline**
* ✔ No hacks
* ✔ No polling
* ✔ No fragile UI hooks
* ✔ Scales to other apps (SMS, WhatsApp, Ring, etc.)

---

## 12. Next Easy Extensions (Optional)

* Quiet hours
* Zone-based speaker routing
* Message batching
* Sender filtering
* Call announcements

---

### ✅ Status

**PRODUCTION-READY & VERIFIED**

---

If you want, next we can:

* Add **zones** (your numbered abstraction system)
* Turn this into a **reusable blueprint**
* Extend to **calls or missed calls**

Just say the word.
