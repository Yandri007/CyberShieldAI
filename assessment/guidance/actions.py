"""Fixed risk-linked actions and deterministic preventive-plan selection."""


def _risk_action(risk_id, kind, what, why, how):
    return {
        "risk_id": risk_id,
        "kind": kind,
        "kind_label": "Verification step" if kind == "verification" else "Recommended fix",
        "what_to_do": what,
        "why_it_matters": why,
        "how_to_start": how,
    }


def _preventive_action(area_id, what, why, how):
    return {
        "area_id": area_id,
        "action_id": f"maintain-{area_id.replace('_', '-')}",
        "kind": "preventive",
        "kind_label": "Preventive recommendation",
        "what_to_do": what,
        "why_it_matters": why,
        "how_to_start": how,
    }


ACTION_CATALOG = {
    "password-unique-passwords": _risk_action(
        "password_security", "remediation",
        "Use a different, strong password for each important business account, and store them in a trusted password manager.",
        "If one reused password is exposed, someone could try it to access other business accounts.",
        "Choose one important account and replace any reused password with a unique one. Consider a reputable password manager.",
    ),
    "password-verify-unique": _risk_action(
        "password_security", "verification",
        "Check whether important business accounts each use a different password.",
        "Confirming this practice helps establish whether one exposed password could put other accounts at risk.",
        "Ask whoever manages your business accounts whether passwords are unique and how that is checked. Do not share passwords during the review.",
    ),
    "mfa-enable-extra-check": _risk_action(
        "mfa", "remediation",
        "Turn on an extra sign-in check for important business accounts, starting with email and financial services.",
        "An extra check can help stop someone using a stolen password to sign in.",
        "Open the security settings for your main business email account and enable its multi-factor sign-in option.",
    ),
    "mfa-check-important-accounts": _risk_action(
        "mfa", "verification",
        "Confirm that an extra sign-in check is enabled on important business accounts.",
        "Checking account settings establishes whether a stolen password has another barrier to overcome.",
        "Review the security settings for your main business email and financial accounts, or ask their administrator to confirm.",
    ),
    "backups-recovery": _risk_action(
        "backups", "remediation",
        "Set up regular backups for important business files and test that a copy can be restored.",
        "Without a usable backup, lost, damaged, or encrypted business files may be difficult or impossible to recover.",
        "List the files your business cannot afford to lose, choose a backup method, and restore one test file to confirm it works.",
    ),
    "backups-verify-recovery": _risk_action(
        "backups", "verification",
        "Confirm that important files are backed up regularly and that a recent copy can be restored.",
        "A backup that has not been checked may not be usable when information is lost or damaged.",
        "Restore one non-sensitive test file, or ask your backup provider or IT support to demonstrate recovery.",
    ),
    "updates-enable-automatic": _risk_action(
        "software_updates", "remediation",
        "Turn on automatic security updates for business devices and the software they use.",
        "Updates often close known security problems that attackers may already understand.",
        "Check update settings on one business computer and enable automatic updates where available.",
    ),
    "updates-check-device-status": _risk_action(
        "software_updates", "verification",
        "Check whether business devices and software are receiving current security updates.",
        "Checking update status shows whether known software problems may still be unaddressed.",
        "Look at the update status on one business computer, then check how the other devices are managed.",
    ),
    "access-review-permissions": _risk_action(
        "user_access", "remediation",
        "Review who can access business accounts and files, and remove access that is no longer needed.",
        "Unneeded access can expose important business or customer information.",
        "Make a list of employees and shared services, then review access when someone changes roles or leaves.",
    ),
    "access-review-account-list": _risk_action(
        "user_access", "verification",
        "Confirm that each employee still needs the business accounts and information they can access.",
        "A review can uncover access that is broader or more out of date than the business intended.",
        "Ask the person who manages accounts to list who can access email, shared files, and financial tools.",
    ),
    "wifi-secure-router": _risk_action(
        "wifi_security", "remediation",
        "Protect business Wi-Fi with a private password and change the router's default administrator password.",
        "Weak Wi-Fi or router settings can expose connected devices and business traffic.",
        "Ask whoever manages the router to change any default login and confirm business Wi-Fi uses a private password.",
    ),
    "wifi-check-router-settings": _risk_action(
        "wifi_security", "verification",
        "Check that business Wi-Fi uses a private password and that the router's administrator password was changed.",
        "Verifying the router settings helps determine whether people without permission could join the business network.",
        "Ask the person who manages Wi-Fi or your internet provider to confirm these two settings.",
    ),
    "devices-check-protection": _risk_action(
        "device_protection", "remediation",
        "Turn on built-in or reputable protection against harmful software on business devices and keep it updated.",
        "Protection can help detect and block software that could compromise a device or its business files.",
        "Check the security status on one business device and turn on its built-in protection if it is off.",
    ),
    "devices-verify-protection": _risk_action(
        "device_protection", "verification",
        "Confirm that protection against harmful software is active and up to date on business devices.",
        "Checking a device's protection status helps show whether it has a current layer against harmful software.",
        "Check the built-in security status on one business device, or ask your support provider what protection is installed.",
    ),
    "employees-report-suspicious": _risk_action(
        "employee_practices", "remediation",
        "Show employees how to pause, avoid links or attachments they do not trust, and report suspicious messages.",
        "A convincing message can lead someone to share a password, expose information, or install harmful software.",
        "Agree on one simple way for employees to report a suspicious message and share it with the team.",
    ),
    "employees-check-reporting": _risk_action(
        "employee_practices", "verification",
        "Confirm that employees know how to recognize and report a suspicious message.",
        "A clear reporting route helps the business respond sooner if someone receives a suspicious message.",
        "Ask the team which person or channel they would use to report a suspicious email or text.",
    ),
}


PREVENTIVE_ACTIONS = {
    "password_security": _preventive_action(
        "password_security",
        "Keep using a different password for each important business account.",
        "Regularly checking this practice helps prevent password reuse from building up as accounts change.",
        "Add password practices to a quarterly review of important business accounts.",
    ),
    "mfa": _preventive_action(
        "mfa",
        "Keep an extra sign-in check enabled for important business accounts.",
        "Rechecking account settings helps keep this extra protection in place as accounts and staff change.",
        "Include business email and financial accounts in your next account settings review.",
    ),
    "backups": _preventive_action(
        "backups",
        "Periodically test restoring a sample file from your business backups.",
        "A regular restore check helps catch backup problems before important files are needed.",
        "Choose a recurring date to restore one non-sensitive sample file and confirm it opens.",
    ),
    "software_updates": _preventive_action(
        "software_updates",
        "Keep automatic security updates on for business devices and software.",
        "Checking update settings helps known software issues get fixed as they are discovered.",
        "Add update status to a monthly check of the devices your business relies on.",
    ),
    "user_access": _preventive_action(
        "user_access",
        "Review staff access when roles change and on a regular schedule.",
        "Periodic reviews help remove access that is no longer needed as responsibilities change.",
        "Add access checks to your employee joiner, role-change, and leaver steps.",
    ),
    "wifi_security": _preventive_action(
        "wifi_security",
        "Keep the business Wi-Fi password and router administrator settings private and current.",
        "Reviewing network settings helps keep access limited to people who should be on the business network.",
        "Add the router and Wi-Fi settings to a regular review with whoever manages your internet service.",
    ),
    "device_protection": _preventive_action(
        "device_protection",
        "Keep device protection turned on and up to date across business computers and phones.",
        "Regular checks help maintain protection as devices are replaced or updated.",
        "Include device protection status in a monthly check of business devices.",
    ),
    "employee_practices": _preventive_action(
        "employee_practices",
        "Remind employees how to pause and report suspicious messages.",
        "Simple reminders help keep the reporting habit clear as the team changes.",
        "Share the team's reporting contact or channel in a brief staff reminder.",
    ),
}


def select_actions(assessment):
    """Select actions for up to three real findings, then fill with prevention."""
    selected = []

    for finding in assessment["findings"][:3]:
        action_id = finding["action_id"]
        action = ACTION_CATALOG[action_id]
        if action["risk_id"] != finding["risk_id"]:
            raise ValueError("The selected action does not match its risk finding.")
        expected_kind = "verification" if finding["certainty"] == "verification" else "remediation"
        if action["kind"] != expected_kind:
            raise ValueError("The selected action does not match the finding certainty.")
        selected.append(
            {
                **action,
                "action_id": action_id,
                "risk_id": finding["risk_id"],
                "risk_addressed": finding["area"],
                "priority": finding["priority"],
                "priority_label": finding["priority_label"],
                "certainty": finding["certainty"],
                "certainty_label": finding["certainty_label"],
            }
        )

    if len(selected) < 3:
        for area in assessment["areas"]:
            if area["answer"] != "yes":
                continue
            action = PREVENTIVE_ACTIONS[area["id"]]
            selected.append(
                {
                    **action,
                    "action_id": action["action_id"],
                    "risk_id": None,
                    "risk_addressed": "No identified finding; maintain the reported control.",
                    "priority": None,
                    "priority_label": None,
                    "certainty": None,
                    "certainty_label": None,
                }
            )
            if len(selected) == 3:
                break

    return selected
