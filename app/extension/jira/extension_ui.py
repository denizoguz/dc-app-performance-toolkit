import random
import time

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.set_credentials(username=username, password=password)
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()


def view_issue_and_create_reminder(webdriver, datasets):
    page = BasePage(webdriver)

    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
        sub_measure()

        @print_timing("selenium_app_custom_action:create_reminder_open")
        def sub_measure():
            page.find_element_by_id('add-reminder-for-jira-link').click()
            page.wait_until_visible((By.ID, "add-reminder-dialog-web-panel"))  # Wait for summary field visible
        sub_measure()

        @print_timing("selenium_app_custom_action:create_reminder_form_fill_and_submit")
        def sub_measure():
            page.wait_until_clickable((By.ID, "add-reminder-summary")).send_keys(f"Testing reminder creation {time.time()}")

            page.wait_until_clickable((By.ID, "add-reminder-comment")).send_keys(f"Description: {page.generate_random_string(100)} {time.time()}")

            page.wait_until_clickable((By.ID, "add-reminder-date")).send_keys(f"31/Mar/29 11:04 AM")

            @print_timing("selenium_app_custom_action:create_reminder_form_submit")
            def sub_measure2():
                page.wait_until_clickable((By.ID, "add-reminder-submit")).click()
                page.wait_until_invisible((By.ID, "add-reminder-dialog-web-panel"))
            sub_measure2()
        sub_measure()
    measure()
