from datetime import datetime, timezone
from getpass import getpass
from pathlib import Path
import json

from playwright.sync_api import sync_playwright

BASE_URL = 'http://127.0.0.1:8000'
REPORT_DIR = Path.home()
checks = {}

username = input('Mayan username [analytics_test]: ').strip() or 'analytics_test'
password = getpass('Mayan password: ')

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='/usr/bin/google-chrome-stable',
        headless=True
    )

    page = browser.new_page(
        viewport={'width': 1440, 'height': 900},
        device_scale_factor=1
    )

    try:
        page.goto(BASE_URL)
        page.locator('#id_username').fill(username)
        page.locator('#id_password').fill(password)
        page.get_by_role('button', name='Sign in').click()

        page.locator('#id_username').wait_for(
            state='hidden', timeout=20000
        )
        checks['Login'] = True

        page.goto(f'{BASE_URL}/dashboards/dashboards/1/')

        for title in ('Activity by User', 'Activity by Event Type'):
            page.get_by_text(title, exact=True).first.wait_for(
                state='visible', timeout=20000
            )
            checks[title] = True

        user_table = page.get_by_role(
            'columnheader', name='Username'
        ).locator('xpath=ancestor::table[1]')

        users = {}
        for row in user_table.locator('tbody tr').all():
            cells = row.locator('td').all_inner_texts()
            if len(cells) >= 2:
                users[cells[0].strip()] = int(cells[1].strip())

        assert len(users) >= 3, f'Expected 3 users, found {users}'
        assert all(count > 0 for count in users.values())
        checks['Multiple users with activity counts'] = True

        canvas = page.locator('#canvas-chart')
        canvas.wait_for(state='visible', timeout=20000)
        page.wait_for_timeout(5000)

        drawn = canvas.evaluate(
            """c => c.getContext('2d')
                .getImageData(0, 0, c.width, c.height)
                .data.some((v, i) => i % 4 === 3 && v > 0)"""
        )
        assert drawn, 'Chart canvas is empty'
        checks['Chart canvas rendered'] = True

        screenshot = REPORT_DIR / 'analytics-e2e-proof.png'
        page.screenshot(path=str(screenshot), full_page=True)

        print('Users:', users)
        print('Screenshot:', screenshot)

    finally:
        browser.close()

report = {
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'checks': checks,
    'users': users,
    'result': 'PASS' if all(checks.values()) else 'FAIL'
}

report_path = REPORT_DIR / 'analytics-e2e-report.json'
report_path.write_text(json.dumps(report, indent=2))

print('\nE2E TEST RESULTS')
for name, passed in checks.items():
    print(f'{"PASS" if passed else "FAIL"}: {name}')

print('Report:', report_path)
