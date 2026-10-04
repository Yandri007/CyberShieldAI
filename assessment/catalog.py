"""Assessment copy, impact bands, and fixed display order."""

AREAS = (
    {
        "id": "password_security",
        "name": "Password security",
        "group": "Account protection",
        "question": "Are business account passwords unique rather than reused across accounts?",
        "helper": "If one account is exposed, reused passwords can put other business accounts at risk.",
        "impact": "high",
        "risk_reason": "Reused or weak passwords can make it easier for someone to access important business accounts.",
        "action_id": "password-unique-passwords",
        "verification_action_id": "password-verify-unique",
    },
    {
        "id": "mfa",
        "name": "Multi-factor authentication",
        "group": "Account protection",
        "question": "Is an extra sign-in check enabled for important business accounts?",
        "helper": "An extra check might be an approval prompt, security key, or one-time code after a password.",
        "impact": "high",
        "risk_reason": "Without an extra sign-in check, a stolen password can more easily lead to account takeover.",
        "action_id": "mfa-enable-extra-check",
        "verification_action_id": "mfa-check-important-accounts",
    },
    {
        "id": "backups",
        "name": "Backups",
        "group": "Business continuity",
        "question": "Are important business files backed up regularly and recoverable?",
        "helper": "A backup is a separate copy of important files that you can restore if the originals are lost or damaged.",
        "impact": "high",
        "risk_reason": "Missing or unreliable backups can leave important business information difficult or impossible to recover.",
        "action_id": "backups-recovery",
        "verification_action_id": "backups-verify-recovery",
    },
    {
        "id": "software_updates",
        "name": "Software and system updates",
        "group": "Devices and network",
        "question": "Are business devices and software kept up to date with security updates?",
        "helper": "Updates often fix known security problems in the software and devices your business uses.",
        "impact": "moderate",
        "risk_reason": "Out-of-date software can remain exposed to security problems that have already been fixed.",
        "action_id": "updates-enable-automatic",
        "verification_action_id": "updates-check-device-status",
    },
    {
        "id": "user_access",
        "name": "User access and permissions",
        "group": "Account protection",
        "question": "Do employees have access only to the business accounts and information they need?",
        "helper": "For example, staff who do not manage payroll usually do not need access to payroll information.",
        "impact": "high",
        "risk_reason": "Unneeded access can expose important business or customer information.",
        "action_id": "access-review-permissions",
        "verification_action_id": "access-review-account-list",
    },
    {
        "id": "wifi_security",
        "name": "Network and Wi-Fi security",
        "group": "Devices and network",
        "question": "Is business Wi-Fi protected from use by people who should not have access?",
        "helper": "Use a private Wi-Fi password and change the router's default administrator password.",
        "impact": "moderate",
        "risk_reason": "Weak Wi-Fi security can expose connected devices and business network traffic.",
        "action_id": "wifi-secure-router",
        "verification_action_id": "wifi-check-router-settings",
    },
    {
        "id": "device_protection",
        "name": "Device protection",
        "group": "Devices and network",
        "question": "Are business devices protected against malware and other harmful software?",
        "helper": "Protection may include built-in security tools or reputable endpoint protection kept up to date.",
        "impact": "moderate",
        "risk_reason": "A device without protection may be more likely to run harmful software or expose business files.",
        "action_id": "devices-check-protection",
        "verification_action_id": "devices-verify-protection",
    },
    {
        "id": "employee_practices",
        "name": "Employee security practices",
        "group": "People and awareness",
        "question": "Do employees know how to recognize and report suspicious messages?",
        "helper": "Suspicious messages may pressure someone to click a link, open an attachment, or share a password.",
        "impact": "moderate",
        "risk_reason": "A convincing suspicious message can lead to stolen passwords, harmful software, or exposed information.",
        "action_id": "employees-report-suspicious",
        "verification_action_id": "employees-check-reporting",
    },
)

ANSWER_POINTS_QUARTERS = {
    "yes": 50,       # 12.5 points
    "not_sure": 25,  # 6.25 points
    "no": 0,
}

ANSWER_LABELS = {
    "yes": "Yes",
    "not_sure": "Not sure",
    "no": "No",
}

PRIORITY_RANK = {"high": 0, "medium": 1}
