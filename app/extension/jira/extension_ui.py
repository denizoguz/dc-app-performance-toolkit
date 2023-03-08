import random
import time

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Issue, PopupManager
from selenium_ui.jira.pages.selectors import IssueLocators

from util.api.jira_clients import JiraRestClient
from util.conf import JIRA_SETTINGS

client = JiraRestClient(JIRA_SETTINGS.server_url, JIRA_SETTINGS.admin_login, JIRA_SETTINGS.admin_password)
rte_status = client.check_rte_status()

def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']
        project_key = issue_key.split('-')[0]

    @print_timing("selenium_app_custom_action:bundles")
    def measure_bundles():
        @print_timing("selenium_app_custom_action:bundles:get_bundles")
        def measure_get_bundles():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}?selectedItem=com.deniz.jira.versioning:cbsv-configuration-management-bundle-panel")
            page.wait_until_visible((By.CSS_SELECTOR, "#cbsv-bundle-list div[role='rowgroup'] div[role='row']:first-child"))  # Wait for first row to be visible
        measure_get_bundles()

        @print_timing("selenium_app_custom_action:bundles:get_bundle_details")
        def measure_get_bunle_content():
            page.wait_until_clickable((By.CSS_SELECTOR, "span[aria-label='Expand']")).click()
            page.wait_until_visible((By.CSS_SELECTOR, "span[aria-label='Collapse']"))  # Wait for toggle symbol change
        measure_get_bunle_content()
    measure_bundles()

    @print_timing("selenium_app_custom_action:component_versions")
    def measure_component_versions():
        @print_timing("selenium_app_custom_action:component_versions:get_components")
        def measure_get_components():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}?selectedItem=com.deniz.jira.versioning:cbsv-configuration-management-component-versions-panel")
            page.wait_until_visible((By.CSS_SELECTOR, "#cbsv-configuration div[role='rowgroup'] div[role='row']:first-child"))  # Wait for first row to be visible
        measure_get_components()

        @print_timing("selenium_app_custom_action:component_versions:get_component_versions")
        def measure_get_component_versions():
            page.wait_until_clickable((By.CSS_SELECTOR, "span[aria-label='Expand']")).click()
            page.wait_until_visible((By.CSS_SELECTOR, "span[aria-label='Collapse']"))  # Wait for toggle symbol change
        measure_get_component_versions()
        # @print_timing("selenium_app_custom_action:component_versions:edit_component_version")
        # def measure_get_bunle_content():
        #     page.wait_until_clickable((By.CSS_SELECTOR, "#cbsv-configuration div[role='rowgroup'] div[role='row'] div[role='gridcell']:last-child button")).click() #open context menu
        #     page.wait_until_visible((By.XPATH, "//button[text()='Edit'")).click() #Click on edit
        #     page.wait_until_visible((By.CSS_SELECTOR, "textarea[name='description'")).send_keys("T")  #Add description
        # measure_get_bunle_content()

    measure_component_versions()

    @print_timing("selenium_app_custom_action:subcomponents")
    def measure_subcomponents():
        @print_timing("selenium_app_custom_action:subcomponents:subcomponents_page")
        def measure_get_subcomponents_page():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}?selectedItem=com.deniz.jira.versioning:cbsv-configuration-management-subcomponents-panel")
            page.wait_until_visible((By.CSS_SELECTOR, "#cbsv-subcomponents-tree-settings"))  # Wait for tree to be visible
        measure_get_subcomponents_page()

        @print_timing("selenium_app_custom_action:subcomponents:edit_issue_with_subcomponents")
        def edit_issue():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_clickable((By.ID, "edit-issue")).click()  # Click on edit
            page.wait_until_clickable((By.ID, "cbsv-subcomponents-dialog-trigger")).click()
            page.wait_until_visible((By.ID, "cbsv-subcomponents-tree"))
            page.wait_until_clickable((By.CSS_SELECTOR, ".fancytree-node:not(.fancytree-folder) .fancytree-checkbox")).click()
            page.wait_until_clickable((By.ID, "cbsv-subcomponents-select")).click()
            page.wait_until_clickable((By.ID, "resolution")).click()
            from selenium.webdriver.support.select import Select
            select = Select(page.wait_until_visible((By.ID, "resolution")))
            select.select_by_value("10000")


            @print_timing("selenium_app_custom_action:subcomponents:edit_issue_with_subcomponents:save_edit_issue_form")
            def sub_measure():
                page.wait_until_clickable((By.ID, "edit-issue-submit")).click()  # submit the dialog
                page.wait_until_invisible((By.ID, "edit-issue-dialog"))  # wait for edit issue dialog to close

            sub_measure()
        edit_issue()
    measure_subcomponents()
    PopupManager(webdriver).dismiss_default_popup()

    @print_timing("selenium_app_custom_action:version_hierarchy")
    def measure_version_hierarchy():
        @print_timing("selenium_app_custom_action:bundles:get_version_hierarchy")
        def measure_get_version_hierarchy():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}?selectedItem=com.deniz.jira.versioning:cbsv-configuration-management-version-graph-panel")
            page.wait_until_visible((By.LINK_TEXT, "Table View")).click()
            page.wait_until_visible((By.LINK_TEXT, "Graph View")).click()
        measure_get_version_hierarchy()
    measure_version_hierarchy()

    @print_timing("selenium_app_custom_action:subprojects")
    def measure_subprojects():
        @print_timing("selenium_app_custom_action:subprojects:subprojects_page")
        def measure_get_subprojects_page():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}?selectedItem=com.deniz.jira.versioning:cbsv-configuration-management-subprojects-panel")
            page.wait_until_visible((By.CSS_SELECTOR, "#cbsv-subprojects-tree"))  # Wait for tree to be visible
        measure_get_subprojects_page()

    @print_timing("selenium_app_custom_action:release_calendar")
    def measure_release_calendar():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}?selectedItem=com.deniz.jira.versioning:cbsv-configuration-management-release-calendar-panel")
        page.wait_until_visible((By.CSS_SELECTOR, "#component-release-calendar"))  # Wait for tree to be visible
    measure_release_calendar()



