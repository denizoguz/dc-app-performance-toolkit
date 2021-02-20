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
    issue_key = datasets["issues"]

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue_with_sim")
        def sub_measure():
            webdriver.get(f"{APPLICATION_URL}/browse/{issue_key}?page=com.deniz.jira.similarissues:similar-issues-tab-panel")
            WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'summary-val')))
            WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'similar_issue_overlay_table')))
        sub_measure()
    measure()

def view_issue_with_similar_issues(webdriver, datasets):
    issue_key = datasets["issues"]
    @print_timing
    def measure(webdriver, interaction):
        @print_timing
        def measure(webdriver, interaction):
            webdriver.get(f"{APPLICATION_URL}/browse/{issue_key}?page=com.deniz.jira.similarissues:similar-issues-tab-panel")
            WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'summary-val')))
            # WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'similar_issue_overlay_table')))
        measure(webdriver, 'selenium_app_custom_action:view_issue_with_sim')

        # @print_timing
        # def measure(webdriver, interaction):
        #     webdriver.get(f'{APPLICATION_URL}/plugins/servlet/some-app/administration')
        #     WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'plugin-dashboard')))
        # measure(webdriver, 'selenium_app_custom_action:view_dashboard')
    measure(webdriver, 'view_issue_with_similar_issues')
