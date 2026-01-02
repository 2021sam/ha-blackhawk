Here’s a **README_Helper.md** you can drop into your repo to document setting up the **Last Motion Time** helper (the `input_datetime.last_motion_time` you created).

---

# README_Helper.md — Last Motion Time Helper (input_datetime)

## Purpose

This helper stores the **timestamp of the most recent motion event** so automations can speak the **previous motion time** (ex: “Last motion was detected at 9:48 PM.”).

This is useful for reassurance:

* “Nothing happened while I was asleep.”
* “No one entered my space since I left.”

---

## Helper Created

* **Name:** `Last Motion Time`
* **Entity ID:** `input_datetime.last_motion_time`
* **Type:** Date and time

---

## Setup Steps (UI)

### 1) Create the helper

1. Go to **Settings → Devices & services → Helpers**
2. Click **Create helper**
3. Choose **Date and/or time**
4. Configure:

   * **Name:** `Last Motion Time`
   * Select **Date and time**
   * **Entity ID:** `input_datetime.last_motion_time`
   * (Optional) Icon: `mdi:motion-sensor`
5. Click **Create**

---

### 2) Confirm it exists

Go to **Developer Tools → States** and search:

* `input_datetime.last_motion_time`

You should see it listed with a date/time value.

---

## How it’s used (logic)

On **motion ON**:

1. Read the helper’s current value → that is the **previous motion time**
2. Update the helper to `now()` (so next motion has a “previous” to speak)

So the helper always represents:

* **“Most recent motion time recorded.”**

---

## Notes

* If you manually change the helper value in the UI, the automations will speak that value.
* If you ever delete/recreate it, keep the **Entity ID** the same (`input_datetime.last_motion_time`) so automations don’t break.

---

If you paste your current automation YAML that updates/reads this helper, I’ll format a matching README section for that exact automation name + entities (`binary_sensor.sonoff_1_occupancy`, `tts.google_translate_en_com`, `media_player.amp_1`, etc.).
