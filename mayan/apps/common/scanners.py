from mayan.apps.platforms_distillery.core.scanner import Scanner


class ProjectLeakScanner(Scanner):
    label = 'Project leak'
    patterns = (
        ('internal homelab domain', r'\brrlabs\.org\b'),
        ('AWS access key id', r'\bAKIA[0-9A-Z]{16}\b'),
        ('private key block', r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    )
