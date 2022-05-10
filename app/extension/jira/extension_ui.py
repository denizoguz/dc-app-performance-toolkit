import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS


def view_issue_with_wp_worklog_tab(webdriver, datasets):
    page = BasePage(webdriver)
    # Add custom_dataset_query: worklogAuthor is not EMPTY to jira.yml file
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue_with_wp_worklog_tab")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}?page=com.deniz.jira.worklog:com.deniz.jira.worklog.worklog-issue-tab-panel")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "worklog-by-user-table"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "wp-ts-worklog-detail-popup"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()


def view_weekly_user_timesheet(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_weekly_user_timesheet")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/WPShowTimesheetAction!customTimesheet.jspa?periodMode=WEEK&targetType=USER&calendarType=CUSTOM&groupingType=ISSUE"
                           f"#targetType=USER&targetKey=currentUser()&groupingType=Project,"
                           f"Issue&periodMode=PERIOD&startDate=2020-09-02&endDate=2020-09-08&&&periodLocked=false&calendarType=CUSTOM&saveToUserHistory=false&extraIssueFilter=&showIssuesWithoutWorklog=false&viewType=TIMESHEET")
            page.wait_until_visible((By.CSS_SELECTOR, "p.wp-weekly-total"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()


def view_monthly_user_timesheet(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_monthly_user_timesheet")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/WPShowTimesheetAction!customTimesheet.jspa?periodMode=WEEK&targetType=USER&calendarType=CUSTOM&groupingType=ISSUE#targetType=USER&targetKey=currentUser()&groupingType=Project,Issue&periodMode=MONTH&startDate=2020-09-01&endDate=2020-09-30&&&periodLocked=false&calendarType=CUSTOM&saveToUserHistory=false&extraIssueFilter=&showIssuesWithoutWorklog=false&viewType=TIMESHEET")
            page.wait_until_invisible((By.CSS_SELECTOR, "div.waitMe"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()


def view_monthly_project_timesheet(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_monthly_project_timesheet")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/WPShowTimesheetAction!customTimesheet.jspa?periodMode=WEEK&targetType=PROJECT&calendarType=CUSTOM&groupingType=ISSUE#targetType=PROJECT&targetKey=AANES&groupingType=Project&periodMode=MONTH&startDate=2020-09-01&endDate=2020-09-30&periodLocked=false&calendarType=CUSTOM&saveToUserHistory=false&extraIssueFilter=&showIssuesWithoutWorklog=false&viewType=TIMESHEET")
            page.wait_until_visible((By.CSS_SELECTOR, "tr[data-project-key='AANES']"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()


def view_approve_timesheet(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_approve_timesheet")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/WorklogPROConfigurationAction!displayTimesheetApproval.jspa#selectedPeriodId=157&groupingType=project")
            page.wait_until_visible((By.ID, "wp-modal-dialog"))
            page.wait_until_clickable((By.LINK_TEXT, 'Default')).click()
        sub_measure()
    measure()


def view_worklog_calendar(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_worklog_calendar")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/WorklogPROWorklogCalendar!default.jspa?targetUsername=currentUser()&startDate=2020-10-04&viewType=agendaWeek")
            page.wait_until_visible((By.ID, "wp-fullcalendar"))
        sub_measure()
    measure()

