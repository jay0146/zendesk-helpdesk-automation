import os
import time
import random
import requests

SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
ADMIN_EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")

if not SUBDOMAIN or not ADMIN_EMAIL or not API_TOKEN:
    raise SystemExit("Missing env vars. Set ZENDESK_SUBDOMAIN, ZENDESK_EMAIL, ZENDESK_API_TOKEN.")

API_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2/tickets.json"
AUTH = (f"{ADMIN_EMAIL}/token", API_TOKEN)

ASSIGNEE_ID = 47359747319195

REQUESTERS = [
    ("Zoe Bennett", "zoe.bennett@northbridgecorp.com"),
    ("Ibrahim Farah", "ibrahim.farah@northbridgecorp.com"),
    ("Kiara Wallace", "kiara.wallace@northbridgecorp.com"),
    ("Jonah Price", "jonah.price@northbridgecorp.com"),
    ("Mina Sato", "mina.sato@northbridgecorp.com"),
    ("Dante Alvarez", "dante.alvarez@northbridgecorp.com"),
    ("Layla Morgan", "layla.morgan@northbridgecorp.com"),
    ("Evan Chen", "evan.chen@northbridgecorp.com"),
    ("Sienna Brooks", "sienna.brooks@northbridgecorp.com"),
    ("Noah Whitman", "noah.whitman@northbridgecorp.com"),
    ("Amara James", "amara.james@northbridgecorp.com"),
    ("Owen Richardson", "owen.richardson@northbridgecorp.com"),
    ("Priya Nair", "priya.nair@northbridgecorp.com"),
    ("Malik Thompson", "malik.thompson@northbridgecorp.com"),
    ("Camila Reyes", "camila.reyes@northbridgecorp.com"),
    ("Tariq Lawson", "tariq.lawson@northbridgecorp.com"),
    ("Holly Spencer", "holly.spencer@northbridgecorp.com"),
    ("Rafael Costa", "rafael.costa@northbridgecorp.com"),
    ("Jade Sinclair", "jade.sinclair@northbridgecorp.com"),
    ("Felix Novak", "felix.novak@northbridgecorp.com"),
]

ISSUES = [
    ("Laptop will not start", "Pressed power button and nothing happens. Charger light is on but screen stays black."),
    ("WiFi keeps disconnecting", "Connection drops every few minutes and calls keep cutting out. Restarted laptop and still happening."),
    ("New employee onboarding access", "New hire starts tomorrow. Need email account, shared drive access, and Teams added."),
    ("Microsoft Outlook search not working", "Search returns no results even for emails I know exist. Restart did not fix it."),
    ("Software install request", "Need Visual Studio Code and Python installed for a training session next week."),
    ("Phishing email reported", "I got an email asking for my password and it looks suspicious. I did not click anything."),
    ("Cannot access shared folder", "Marketing folder says access denied. I had access last week."),
    ("Printer printing blank pages", "Print job goes through but pages come out blank. Tried different document and same issue."),
    ("Headset microphone not detected", "Teams says no mic available. It works on my phone but not on this computer."),
    ("VPN connects but no internal sites load", "VPN says connected but internal portal will not open. External sites work fine."),
    ("Locked out after password change", "Changed password and now I cannot sign in. It says incorrect password."),
    ("Monitor flickering", "Second monitor keeps flickering and sometimes goes black for a second."),
    ("Storage almost full warning", "Getting low disk space popups and apps are running slow."),
    ("Calendar invites not sending", "When I send meeting invites, people do not receive them or they show up hours later."),
    ("MFA codes not coming through", "Trying to log in and it asks for a code but I am not getting texts."),
    ("Website certificate warning", "Browser shows a security warning when opening the internal HR site."),
    ("Request new keyboard and mouse", "Current keyboard sticks and mouse double clicks. Need replacement."),
    ("File recovery request", "Accidentally deleted a folder from the shared drive. Need it restored if possible."),
    ("Teams stuck on loading", "Teams opens but stays on loading screen forever. Reinstall did not help."),
    ("Suspicious sign in alert", "Got an alert for a login attempt from a different state. I was not there."),
]

PRIORITIES = ["low", "normal", "high", "urgent"]

def pick_priority(subject: str) -> str:
    s = subject.lower()
    if "phishing" in s or "suspicious" in s or "certificate" in s or "mfa" in s:
        return "urgent"
    if "vpn" in s or "wifi" in s or "locked" in s or "will not start" in s:
        return "high"
    if "access" in s or "not working" in s or "blank pages" in s or "not detected" in s:
        return "normal"
    return random.choice(PRIORITIES)

def create_ticket():
    name, email = random.choice(REQUESTERS)
    subject, body = random.choice(ISSUES)
    priority = pick_priority(subject)

    payload = {
        "ticket": {
            "subject": subject,
            "comment": {"body": body},
            "priority": priority,
            "assignee_id": ASSIGNEE_ID,
            "requester": {"name": name, "email": email},
        }
    }

    r = requests.post(API_URL, auth=AUTH, json=payload, timeout=30)
    if r.status_code not in (200, 201):
        print("Failed:", r.status_code, r.text)
        return None

    ticket = r.json().get("ticket", {})
    ticket_id = ticket.get("id")
    print(f"Created {ticket_id} | {priority.upper()} | {name} | {subject}")
    return ticket_id

def run(count=20, min_wait=10, max_wait=35):
    for i in range(count):
        create_ticket()
        if i < count - 1:
            time.sleep(random.randint(min_wait, max_wait))

if __name__ == "__main__":
    run(count=20, min_wait=10, max_wait=35)