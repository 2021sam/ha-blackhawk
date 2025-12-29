---

# Advanced SSH & Web Terminal – Setup & Usage

This project uses **Home Assistant OS** with the **Advanced SSH & Web Terminal** add-on for terminal access, SSH, and file transfer (SCP).

> ⚠️ Important: Add-on configuration and network settings are **NOT stored in `/config`** and therefore **NOT tracked by Git**. They must be configured manually on each device.

---

## Add-on Overview

* **Add-on name:** Advanced SSH & Web Terminal
* **Purpose:**

  * Web-based terminal inside Home Assistant
  * SSH access from remote machines
  * SCP file transfer (requires SFTP enabled)

---

## Required Configuration (Add-on → Configuration)

Use this **known-working baseline**:

```yaml
ssh:
  username: root
  password: "<SET_MANUALLY>"
  authorized_keys: []
  sftp: true
  compatibility_mode: true
  allow_agent_forwarding: false
  allow_remote_port_forwarding: false
  allow_tcp_forwarding: false
zsh: true
share_sessions: false
packages: []
init_commands: []
```

### Notes

* `password` **must not be empty**
* Quotes around the password are **safe and recommended**
* `sftp: true` is **required** for `scp`
* `compatibility_mode: true` avoids macOS/OpenSSH issues

---

## Network Settings (Add-on → Network)

These settings are **NOT part of the YAML** and must be set in the UI.

| Setting         | Value    |
| --------------- | -------- |
| SSH server port | **2222** |

> Do **NOT** use port 22 on Home Assistant OS. It is unreliable and often blocked.

---

## Start & Verify

1. **Save** configuration
2. **Restart** the add-on
3. Confirm status shows **Running**
4. Open **Terminal** from the sidebar

You should see:

```bash
root@homeassistant:~#
```

Verify identity:

```bash
whoami
# root
```

---

## SSH Access (from another machine)

```bash
ssh -p 2222 root@homeassistant.local
```

If `.local` does not resolve, use the IP:

```bash
ssh -p 2222 root@<HA_IP>
```

---

## SCP File Transfer

```bash
scp -P 2222 root@homeassistant.local:/config/automations.yaml .
scp -P 2222 root@homeassistant.local:/config/scripts.yaml .
```

---

## What IS and IS NOT in Git

### ✅ Stored in Git

* `/config/automations.yaml`
* `/config/scripts.yaml`
* `/config/configuration.yaml`
* `/config/packages/*`
* Documentation under `/docs`

### ❌ NOT stored in Git

* SSH add-on config
* SSH password
* SSH port (2222)
* Add-on install state

These are **Supervisor-managed**.

---

## Recommended Practice

* Do **NOT** commit passwords to Git
* Store a **template/example config** in `/docs`
* Keep SSH port and usage documented
* Consider switching to **SSH keys** later

---

## Common Failure Causes

| Symptom                    | Cause                       |
| -------------------------- | --------------------------- |
| Terminal won’t open        | Empty password              |
| `scp` fails                | `sftp: false`               |
| Connection refused         | Wrong port (not 2222)       |
| Worked before, broke later | Add-on restart / port reset |

---

## One-Line Rule (Remember This)

> **`/config` is Git.
> Add-ons are Supervisor.
> Supervisor must be documented, not versioned.**

---

