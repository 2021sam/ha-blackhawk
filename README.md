## 🏡 **ha-blackhawk — Home Assistant Configuration**

**Location-independent Home Assistant setup using numbered zones to decouple rooms from automations and devices.**

This repo contains a **live, Git-managed Home Assistant configuration** running on a Raspberry Pi. It includes YAML automations, scenes, scripts, and web assets (e.g., soundscapes) used to control lights, play audio cues, and more.

---

## 🌟 Features

* **Numeric zone abstraction** — devices & rooms referenced by numbers instead of literal names
* **Automations & scripts** for common behaviors (lights on/off, PIR triggers, sound cues)
* **Soundscape support** — versioned audio assets in the `www/` directory
* **Git tracking without sensitive data** (see `.gitignore`)
* **SSH-based remote Git integration for seamless pushes/pulls**
* Designed to be **deployable and understandable** by collaborators or future you

---

## 📁 Repository Structure

```
ha-blackhawk/
├── .git/                    # Git metadata
├── .gitignore               # Ignore runtime/state
├── README.md                # This file
├── blueprints/              # YAML automation & script blueprints
├── configuration.yaml       # Core HA config
├── automations.yaml         # Automation definitions
├── scripts.yaml             # Script definitions
├── scenes.yaml              # Scene definitions
├── www/                     # Static assets served as /local/
│   └── soundscapes/         # Versioned audio files
├── secrets.yaml             # *Not* committed — excluded by .gitignore
```

> YAML files like `configuration.yaml`, `automations.yaml`, and `scripts.yaml` form the core of how Home Assistant behaves.

---

## 🚀 Quick Start

### Prerequisites

* Home Assistant OS running on a Raspberry Pi
* SSH access to the Pi
* A machine where you edit config (e.g., Mac, PC)
* An SSH key added to your GitHub account

---

## 📦 Clone the Repo

### On your local machine (Mac/PC)

```bash
cd ~/apps
git clone git@github.com:2021sam/ha-blackhawk.git
cd ha-blackhawk
git checkout master
```

---

## 📡 Install on Raspberry Pi (Home Assistant OS)

```bash
cd /homeassistant
git clone git@github.com:2021sam/ha-blackhawk.git .
git checkout master
ha core restart
```

---

## 🧰 Git Identity (optional, recommended)

To make commits show your real name/email:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## 📤 Updating the Repository

### On your editor machine:

```bash
git add -A
git commit -m "Describe what changed"
git push
```

### On the Raspberry Pi (pull latest):

```bash
cd /homeassistant
git pull
ha core restart   # refresh HA if needed
```

---

## 🎧 Soundscapes — Static Media

Place audio in:

```
/homeassistant/www/soundscapes/
```

They serve at:

```
/local/soundscapes/<filename>.wav
```

### Example (browser test):

```
http://<YOUR_HA_HOST>:8123/local/soundscapes/1.wav
```

If you add new files to `www/`, HA sometimes needs a core restart so the webserver recognizes them.

---

## 📜 Example Usage in Scripts

Sound playback snippet:

```yaml
- action: media_player.play_media
  target:
    entity_id: media_player.family_room
  data:
    media:
      media_content_id: /local/soundscapes/1.wav
      media_content_type: music
```

---

## 📌 Best Practices

### 🔐 Secrets & Security

Sensitive information is excluded by `.gitignore`. Use `!secret` in YAML and store values in `secrets.yaml` which is not committed.

### 📦 `.gitignore` Rules

The `.gitignore` excludes:

* runtime state dirs like `.storage/`, `.cloud/`, `tts/`, etc.
* databases (`home-assistant_v2.db*`, `zigbee.db*`)
* logs and locks
* secrets and keys

This keeps the repo **clean and shareable**, while preserving core configs.

### 🔁 Commit Often

Commit changes after each meaningful tweak. This makes rollbacks and understanding history easy.

---

## 🧪 Quick Tests

### 1. Static file test

Open in browser:

```
http://<HA_HOST>:8123/local/soundscapes/1.wav
```

Should play/download.

### 2. Script test

Create a test script in HA UI using the example above and run it manually.

### 3. Developer Tools Action

Paste:

```yaml
action:
  - service: media_player.play_media
    target:
      entity_id: media_player.family_room
    data:
      media:
        media_content_id: /local/soundscapes/1.wav
        media_content_type: music
```

Run — media should play.

---

## 🧠 Zone Abstraction

This repo uses **zone numbers** (e.g., `1`, `2`, etc.) instead of literal room names. This allows:

* easier reuse
* less accidental exposure of locations
* consistent automation logic across spaces

---

## 🧩 Common Commands

Listing remotes:

```bash
git remote -v
```

Pulling latest:

```bash
git pull
```

Checking status:

```bash
git status
```

Setting ssh remote:

```bash
git remote set-url origin git@github.com:2021sam/ha-blackhawk.git
```

---

## 📬 Contributions

This is your own config; but if you share examples, improvements welcome. The clearer we document Home Assistant configs, the easier it is to onboard others. Many in the community recommend using `!secret` for private values and scrubbing sensitive info before pushing public repos. ([community.home-assistant.io][1])

---

## 📄 License

**MIT License**
Use, share, and adapt as you see fit.

---

<!-- JARVIS_PRODUCT_STATUS_2026 -->
## Jarvis Home Hub integration: phases and status

This Home Assistant configuration is the **home-automation side of the Jarvis Home Hub prototype**. The Mac-side AI/API service is documented in the companion `anythingllm-wake` repository. **Phase 1 is a working demonstration, not a customer-ready installation package.**

### Phase 1 — Working in the demonstration home

- Custom `jarvis_conversation` integration forwards Assist requests and device identifiers to the Jarvis API.
- Pixel 6 Pro acts as an always-listening “Hey Jarvis” voice entry point.
- Home Assistant performs configured device actions; device commands are routed separately from free-form LLM answers.
- Per-device speaker preferences support voice-selectable destinations, including Family Room audio; Pixel plus external audio output has been tested.
- Guardian/motion lighting automation with an adjustable audio cooldown; motion retriggers reset the cooldown interval.
- Existing helper, script, and automation directories support lighting, audio, notifications, and other house-specific workflows.

### Phase 2 — Experimental / incomplete

| Capability | Status | Next milestone |
| --- | --- | --- |
| Appliance operating instructions | Experimental, handled through Mac-side AnythingLLM | Verified manufacturer-specific step-by-step guidance |
| Guided cooking conversations | Experimental | Reliable multi-turn state and safety checks |
| Wake acknowledgment tone | Incomplete | Confirm tone reliably plays when wake word activates microphone |
| Continuous follow-up voice interaction | Partially implemented across components | Test end-to-end hands-free task continuation |
| Multi-room voice routing | Manual speaker selection works | More automatic and context-aware room selection |

### Phase 3 — Planned for customer installations

- Portable configuration and setup wizard; avoid hard-coded entity IDs, rooms, and IP addresses.
- Repeatable deployment, backup, update, rollback, and diagnostics procedures.
- Customer-safe onboarding, secrets management, and documented supported devices.
- Acceptance testing for voice control, audio, privacy, and safety.

### Example user experience

1. Say “Hey Jarvis” near the Pixel voice satellite.
2. Ask Jarvis to control a configured Home Assistant light or answer a question from household documents.
3. Choose a response speaker by voice, e.g. “change speaker to Family Room.”
4. For appliance guidance, treat responses as **experimental** until verified against the manufacturer's manual.

### Security and publication

Do not publish tokens, passwords, service-account JSON, personal addresses, internal endpoints, or identifiable household data. Review Git diffs before pushing this repository publicly.
