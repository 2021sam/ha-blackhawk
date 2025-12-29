## Why the Home Assistant Terminal add-on is painful (scroll vs copy)

The built-in HA Terminal (and some embedded terminals) can behave like this:

* If you can **scroll**, you often **can’t easily select/copy**.
* If you can **select/copy**, scrolling/history is limited or awkward.

### tmux mouse mode (helps scroll, can still be awkward for copy)

If you use tmux inside the HA terminal:

```sh
tmux set -g mouse on
```

This usually improves scrolling, but **copy/select behavior may still be clunky** depending on the client terminal.

✅ Best fix: **SSH from a real computer (Mac/Linux/Windows)**. You get proper scrollback, copy/paste, search, and `less`.

---

## SSH from a Mac (recommended workflow)

### Connect

Home Assistant OS commonly exposes SSH via the **SSH add-on** on port **2222**:

```sh
ssh root@10.0.0.126 -p 2222
```

First time, you’ll be prompted to trust the host key.

* Type `yes` (pressing Enter alone = no)

### Host key mismatch (homeassistant.local vs IP)

If you previously connected via `homeassistant.local`, SSH might complain when connecting via IP+port. Fix:

```sh
ssh-keygen -R homeassistant.local
```

Then connect again and type `yes`.

### After login

```sh
cd /homeassistant
```

Optional: keep sessions alive through disconnects:

```sh
tmux new -s ha
# later:
tmux attach -t ha
```

---

## Git branch switching + why automations “don’t load”

When you run `git checkout <branch>`, Git changes files on disk immediately, but **Home Assistant does not automatically reload automations into memory**.

So you can see “ghost” behavior like:

* old automations still showing
* duplicates temporarily
* UI not matching the active branch

**Browser refresh does not fix this.**
You must reload automations (fast) or restart HA Core (slower but thorough).

---

## Fast reload (1 second): Reload Automations action

In the HA UI:

**Developer tools → Actions → search `automation.reload` → Perform action**

This is the fastest way to make HA re-read `automations.yaml`.

---

## Make reload one click: Script + Dashboard Button

Add this to `scripts.yaml`:

```yaml
reload_automations:
  alias: Reload Automations
  icon: mdi:reload
  sequence:
    - action: automation.reload
```

Then reload scripts (Developer tools → Actions → search `script.reload`), or restart core once.

### Add a dashboard button

Dashboard → Edit → Add card → **Button**

* Entity: `script.reload_automations`
* Name: Reload Automations

Now you’ve got a **single click reload**.

---

## When to use `ha core restart`

If anything looks “cached”, weird, or duplicated after switching branches:

```sh
ha core restart
```

This takes ~1 minute and is normal. It’s the “clean slate” reload.

---

## Git branch strategy (simple + safe)

Recommended structure:

* `master` → stable baseline (shared config)
* `tests` → experiments / temporary automation tests
* `loc_<name>` → location-specific automations (optional, later)

Example:

* `master`
* `tests`
* `loc_blackhawk`
* `loc_laurie`

### Rules

* Do experiments on `tests`.
* Keep `master` clean/stable.
* Don’t assume HA will instantly reflect a branch switch.
* After switching branches, always run **Reload Automations** (or restart core if needed).

---

## Branch switching workflow (do this every time)

From SSH:

```sh
cd /homeassistant
git checkout <branch>
git pull --rebase origin <branch>
```

Then in HA:

* click your **Reload Automations** button (preferred), or
* run `ha core restart` if you want the “full reset”.

---

## Troubleshooting: “Why did master show my tests changes?”

If it ever *looks* like changes “followed you” to another branch, it’s usually one of these:

* HA didn’t reload yet (UI still showing previous in-memory state)
* You had uncommitted local edits when switching branches
* The same file content exists in both branches (not actually new)

Quick checks from SSH:

```sh
git status
git diff master..tests -- automations.yaml
git branch --contains <commit_hash>
```

---

## Nice-to-have (optional): Keep a “Tools” dashboard

Create a dashboard named **Tools** and pin buttons:

* Reload Automations (`script.reload_automations`)
* Reload Scripts (`script.reload` via another script if desired)
* Restart Core (`ha core restart` via SSH, or UI restart)

This keeps your “dev workflow” one click away.

---

If you want, paste your current `README.md` (or tell me which README you want to update: `README.md` vs `README_Terminal.md`), and I’ll rewrite it cleanly with headings + a tight “Quick Start” block at the top.




---
Perfect — that’s the right model.

You want:

* **Laurie’s Pi** → push **only** to her own branch
* You → keep control of `master`
* New branch: **`deercreek`**

Here’s the **clean, correct, no-surprises sequence**.

---

## Part 1 — You create the `deercreek` branch (once)

Do this from **your machine** (or any machine where you manage the repo).

### 1) Start from a clean `master`

```bash
git checkout master
git pull --rebase origin master
```

### 2) Create the new branch

```bash
git checkout -b deercreek
```

At this point:

* `deercreek` = exact copy of `master`

### 3) Push it to GitHub

```bash
git push -u origin deercreek
```

That’s it. The branch now exists remotely.

---

## Part 2 — Point Laurie’s Pi at `deercreek`

On **Laurie’s Pi**:

### 1) Fetch new branches

```bash
cd /homeassistant
git fetch origin
```

### 2) Switch to the `deercreek` branch

```bash
git checkout deercreek
```

If Git says the branch doesn’t exist locally yet, use:

```bash
git checkout -b deercreek origin/deercreek
```

### 3) Set upstream tracking (important)

```bash
git branch --set-upstream-to=origin/deercreek
```

Verify:

```bash
git status
```

You should see:

```
On branch deercreek
Your branch is up to date with 'origin/deercreek'.
```

---

## Part 3 — Laurie’s normal workflow (simple)

From now on, **on Laurie’s Pi**:

### Pull updates

```bash
git pull --rebase
```

### Make changes (YAML edits, tests, etc.)

```bash
git add automations.yaml
git commit -m "deercreek: adjust patio light timing"
git push
```

She will:

* ✅ push only to `deercreek`
* ❌ never touch `master`
* ❌ never affect other locations

---

## Part 4 — Your workflow (promote changes safely)

When you want to bring something from `deercreek` → `master`:

```bash
git checkout master
git pull --rebase origin master
git cherry-pick <commit_hash_from_deercreek>
git push
```

No merges, no pollution, no surprises.

---

## One critical rule (write this in the README)

> **Never commit directly to `master`.**
> Location machines commit only to their own branch (`deercreek`, `blackhawk`, etc.).

---

## After branch switches on Laurie’s Pi

Always:

* Click **Reload Automations** (`automation.reload`)
* Or if anything looks off: `ha core restart`

---

## Final sanity check (optional)

On Laurie’s Pi:

```bash
git branch -vv
```

You should see:

```
* deercreek  abc1234 [origin/deercreek]
  master     xyz5678 [origin/master]
```

---

If you want, next I can:

* add a **branch policy section** to your README
* give Laurie a **“safe daily checklist”**
* or lock `master` against accidental pushes

You’re setting this up the *right* way.

