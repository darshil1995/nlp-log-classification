import re

PATTERNS = {
    "User Action": re.compile(
        r"(?:User User\d+ logged (in|out))|"
        r"(?:Account with ID .* created by .*)",
        re.IGNORECASE
    ),
    "System Notification": re.compile(
        r"(?:Backup (?:started|ended|completed successfully))|"
        r"(?:System (?:updated to version|reboot initiated by user) .*)|"
        r"(?:File .* uploaded successfully by user .*)|"
        r"(?:Disk cleanup completed successfully.)",
        re.IGNORECASE
    )
}

def classify_with_regex(log_message):
    for label, pattern in PATTERNS.items():
        if pattern.search(log_message):
            return label
    return None

if __name__ == "__main__":
    print(classify_with_regex("Backup completed successfully."))
    print(classify_with_regex("Account with ID 1234 created by User1."))
    print(classify_with_regex("Hey Bro, chill ya!"))