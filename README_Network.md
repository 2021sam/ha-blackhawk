Perfect — this is exactly the right moment to **codify the decision** so Future-You (and Laurie-You) don’t re-debug this.

Below is a **clean, production-grade README section** you can drop directly into your repo.

---

# 📡 Home Assistant Network Architecture

## Overview

This Home Assistant deployment **requires a wired (Ethernet) network connection** for the Home Assistant host (Raspberry Pi).

This is a **deliberate architectural decision** based on real-world testing with consumer ISPs, managed Wi-Fi, and multicast-dependent devices (audio, discovery, TTS).

---

## ✅ Supported & Recommended Configuration

### Home Assistant Host

* **Connection:** Ethernet (wired)
* **Reason:** Stable routing, multicast reliability, deterministic behavior

### Audio / IoT Devices

* **Connection:** Wi-Fi
* Examples:

  * LinkPlay / A30 audio devices
  * Chromecast-like speakers
  * Zigbee / Thread coordinators (via USB)

This topology is **stable, repeatable, and production-safe**.

---

## ❌ Unsupported / Experimental Configuration

### Home Assistant Host over Wi-Fi

Running the Home Assistant host on Wi-Fi is **not supported** in this environment.

Reasons include:

* Client isolation / AP isolation
* Multicast (mDNS / SSDP) suppression
* Consumer router “security” features
* ISP apps (e.g. Xfinity) modifying network behavior automatically
* Dual-interface routing ambiguity (Ethernet + Wi-Fi)

This configuration may:

* Appear connected but be unreachable
* Break audio/TTS silently
* Go “offline” after router or app changes
* Require frequent manual recovery

---

## 🧠 Key Design Rule

> **Home Assistant must be Ethernet-connected.**
> Audio and IoT devices may be Wi-Fi.

This rule eliminates:

* mDNS discovery failures
* UDP audio dropouts
* Xfinity / ISP interference
* Linux routing edge cases

---

## 🔊 Audio & Multicast Notes

Audio devices (e.g. LinkPlay / A30) rely on:

* mDNS
* SSDP / UPnP
* UDP streaming

These protocols are **extremely sensitive** to:

* Wi-Fi client isolation
* Guest networks
* Band steering
* “Optimize device” features
* Multicast filtering

Wiring the Home Assistant host avoids all of these failure modes.

---

## 🛜 Known Network Constraints

### Xfinity / ISP-Managed Networks

* May silently pause or restrict headless Linux devices
* May re-enable isolation after updates
* May change DHCP or routing without notice

### Managed Wi-Fi / Guest Networks (e.g. Laurie’s)

* Client-to-client traffic often blocked
* Multicast commonly disabled
* Unsuitable for Home Assistant controllers

---

## 🔁 Recovery Procedure (If Network Issues Occur)

Home Assistant OS is resilient and **cannot be bricked by network settings**.

If Home Assistant becomes unreachable:

1. Power off the Raspberry Pi
2. Plug in Ethernet
3. Power on
4. Access via:

   ```
   http://<wired-ip>:8123
   ```

Service will be restored immediately.

---

## 🧾 Summary

| Component           | Network  | Status          |
| ------------------- | -------- | --------------- |
| Home Assistant host | Ethernet | ✅ Required      |
| Audio devices (A30) | Wi-Fi    | ✅ Supported     |
| Zigbee / Thread     | USB      | ✅ Supported     |
| HA over Wi-Fi       | Wi-Fi    | ❌ Not supported |

---

## 📌 Final Note

This network design is **intentional**, not a workaround.

It prioritizes:

* Stability
* Predictability
* Low maintenance
* Zero surprise outages

Future changes to Wi-Fi infrastructure **do not require reconfiguration** of Home Assistant as long as Ethernet is maintained.

---

If you want, next we can:

* Add a **network diagram**
* Create a **“Laurie deployment checklist”**
* Add a **static IP / DHCP reservation appendix**

Just say the word.
