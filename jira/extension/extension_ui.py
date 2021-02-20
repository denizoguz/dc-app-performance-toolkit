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


def view_issue_with_similar_issues(webdriver, datasets):
    page = BasePage(webdriver)
    issue_key = datasets["issues"]

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue_with_sim")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}?page=com.deniz.jira.similarissues:similar-issues-tab-panel")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "similar_issue_overlay_table"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()

def custom_action(webdriver, datasets):
    @print_timing
    def measure(webdriver, interaction):
        @print_timing
        def measure(webdriver, interaction):
            webdriver.get(f'{APPLICATION_URL}/plugins/servlet/some-app/reporter')
            WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'plugin-element')))
        measure(webdriver, 'selenium_app_custom_action:view_report')

        @print_timing
        def measure(webdriver, interaction):
            webdriver.get(f'{APPLICATION_URL}/plugins/servlet/some-app/administration')
            WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'plugin-dashboard')))
        measure(webdriver, 'selenium_app_custom_action:view_dashboard')
    measure(webdriver, 'selenium_app_custom_action')
