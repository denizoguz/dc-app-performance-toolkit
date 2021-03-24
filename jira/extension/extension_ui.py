import random
import time
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from jira.selenium_ui.conftest import print_timing, AnyEc, application_url, generate_random_string

APPLICATION_URL = application_url()
timeout = 20


# def custom_action(webdriver, datasets):
#     @print_timing
#     def measure(webdriver, interaction):
#         @print_timing
#         def measure(webdriver, interaction):
#             webdriver.get(f'{APPLICATION_URL}/plugins/servlet/some-app/reporter')
#             WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'plugin-element')))
#         measure(webdriver, 'selenium_app_custom_action:view_report')
#
#         @print_timing
#         def measure(webdriver, interaction):
#             webdriver.get(f'{APPLICATION_URL}/plugins/servlet/some-app/administration')
#             WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'plugin-dashboard')))
#         measure(webdriver, 'selenium_app_custom_action:view_dashboard')
#     measure(webdriver, 'selenium_app_custom_action')

def view_issue_and_create_reminder(webdriver, datasets):
    issue_key = random.choice(datasets["issues"])[0]
    @print_timing
    def measure(webdriver, interaction):
        @print_timing
        def measure(webdriver, interaction):
            webdriver.get(f"{APPLICATION_URL}/browse/{issue_key}")
            _wait_until(webdriver, EC.visibility_of_element_located((By.ID, "summary-val")), interaction)
        measure(webdriver, 'selenium_app_custom_action:view_issue')

        @print_timing
        def measure(webdriver, interaction):
            webdriver.find_element_by_id('add-reminder-for-jira-link').click()
            _wait_until(webdriver, EC.visibility_of_element_located((By.ID, "add-reminder-dialog-web-panel")), interaction)
        measure(webdriver, "selenium_app_custom_action:create_reminder_open")

        @print_timing
        def measure(webdriver, interaction):
            _wait_until(webdriver, EC.element_to_be_clickable((By.ID, "add-reminder-summary")), interaction).send_keys(f"Testing reminder creation {time.time()}")

            text_description = f'Description: {generate_random_string(100)}'
            element = webdriver.find_element_by_id('add-reminder-comment')
            _write_to_text_area(webdriver, element, text_description, interaction)

            _wait_until(webdriver, EC.element_to_be_clickable((By.ID, "add-reminder-date")), interaction).send_keys(f"31/Mar/29 11:04 AM")

            @print_timing
            def measure(webdriver, interaction):
                _wait_until(webdriver, EC.element_to_be_clickable((By.ID, "add-reminder-submit")), interaction).click()
                _wait_until(webdriver, EC.invisibility_of_element_located((By.ID, "add-reminder-dialog-web-panel")), interaction)
            measure(webdriver, "selenium_app_custom_action:create_reminder_form_submit")
        measure(webdriver, "selenium_app_custom_action:create_reminder_form_fill_and_submit")
    measure(webdriver, 'selenium_app_custom_action:create_reminder')