# Google Assistant — Customer Setup

## Purpose

This procedure connects a customer's Google Home / Nest speakers to their Home Assistant system.

Once configured, the customer can use normal Google Assistant commands such as:

"Hey Google, turn on Wall Dimmer One."

The customer does NOT create a Google Cloud project, service account, HomeGraph configuration, OAuth application, or Google Home Developer project.

Those are part of the central integration and should be configured once by the system administrator.

---

## What the Customer Needs

- A Google account
- Google Home app installed on their phone
- Their Google Nest / Google Home speaker already added to their Google Home
- Their Home Assistant username and password
- Internet access

The Google account used in the Google Home app should be the account associated with the customer's Google Home/Nest devices.

---

# Customer Installation Procedure

## 1. Open Google Home

Open the Google Home app on the customer's phone.

From the Home screen, tap:

+ → Link app or service → Works with Google

---

## 2. Find the Home Assistant Integration

Use the search box.

During development/testing, search for:

Home Assistant

and select:

[test] Home Assistant

For a production integration, select the published integration name instead.

---

## 3. Sign Into Home Assistant

Google will open the customer's Home Assistant login page.

Enter:

- Home Assistant username
- Home Assistant password

Tap:

Log in

Home Assistant will display a message explaining that the Google integration is requesting access to the Home Assistant instance.

Continue with authorization.

---

## 4. Approve Google Access

Google displays:

"When you link your Google Account and Home Assistant account"

Tap:

Agree and continue

Google will complete the account-linking process.

---

## 5. Synchronize Devices

After returning to Google Home, tell the Google speaker:

"Hey Google, sync my devices."

Google should respond that it is syncing devices for Home Assistant.

---

## 6. Test a Device

Test one of the devices exposed by Home Assistant.

Example:

"Hey Google, turn on Wall Dimmer One."

Then:

"Hey Google, turn off Wall Dimmer One."

If both commands work, customer setup is complete.

---

# How Multiple Customers Work

Customers do NOT share one Google account.

Each customer uses their own Google account and their own Google Home.

Architecture:

                    CENTRAL GOOGLE INTEGRATION
                              |
                              |
                 Home Assistant / Google
                       Cloud-to-Cloud
                              |
              +---------------+---------------+
              |               |               |
          Customer A      Customer B      Customer C
          Google acct     Google acct     Google acct
              |               |               |
          Google Home     Google Home     Google Home
              |               |               |
          HA Account      HA Account      HA Account
              |               |               |
          Customer A      Customer B      Customer C
          HA instance     HA instance     HA instance

The customer's Google account identifies which linked Home Assistant account belongs to that Google user.

Therefore, a command such as:

"Hey Google, turn on Light One."

does not require the customer to say their customer number, Home Assistant hostname, or other identifier.

Google already knows which smart-home account is associated with that Google user.

---

# What Is Done Once vs. Per Customer

| Setup | Once Centrally | Each Customer |
|---|---|---|
| Google Developer project | YES | |
| Cloud-to-cloud integration | YES | |
| HomeGraph API | YES | |
| OAuth configuration | YES | |
| Service-account infrastructure | YES | |
| Google Home app | | YES |
| Customer Google account | | YES |
| Link Home Assistant account | | YES |
| Agree/authorize | | YES |
| Sync devices | | YES |
| Test voice command | | YES |

The goal is NOT to repeat the original developer setup for every customer.

For a properly deployed production integration, each customer should perform essentially the same short account-linking procedure.

---

# Installer Checklist

Before giving the phone to the customer, verify:

[ ] Customer Home Assistant is online
[ ] External HTTPS access works
[ ] Google Assistant endpoint is available
[ ] Correct entities are exposed to Google
[ ] Customer has Google Home app
[ ] Nest/Google speaker is in customer's Google Home

Then the customer performs:

Google Home
    |
    v
+
    |
    v
Link app or service
    |
    v
Works with Google
    |
    v
Home Assistant integration
    |
    v
Log into Home Assistant
    |
    v
Agree and continue
    |
    v
"Hey Google, sync my devices"
    |
    v
Test voice command

Customer onboarding should take only a few minutes once the central Google integration and the customer's Home Assistant system are already configured.
