import random
import time
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from jira.selenium_ui.conftest import print_timing, AnyEc, application_url, generate_random_string
from jira.selenium_ui.modules import _wait_until

APPLICATION_URL = application_url()
timeout = 20


def log_work(webdriver, datasets):
    @print_timing
    def measure(webdriver, interaction):
        # open log work dialog
        WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'add-worklog-issue-right-panel-link')), interaction)

        @print_timing
        def measure(webdriver, interaction):
            webdriver.find_element_by_id('add-worklog-issue-right-panel-link').click()
            WebDriverWait(webdriver, timeout).until(EC.visibility_of_element_located((By.ID, 'add-worklog-dialog-timesheet')), interaction)
        measure(webdriver, "selenium_create_worklog:open_log_work_dialog")

        # create worklog
        @print_timing
        def measure(webdriver, interaction):
            timeSpent = webdriver.find_element_by_id('log-work-time-logged')
            timeSpent.send_keys("15m")
            logWorkButton = webdriver.find_element_by_id('worklogpro-log-work-submit')
            logWorkButton.click()

            WebDriverWait(webdriver, timeout).until(EC.invisibility_of_element_located((By.ID, 'add-worklog-dialog-timesheet')), interaction)

        measure(webdriver, "selenium_create_issue:fill_and_submit_log_work_form")

    measure(webdriver, 'selenium_log_work')


def view_weekly_user_ts(webdriver, datasets):
    period = random.choice(datasets["periods_weekly"])
    start_date = period[0]
    end_date = period[1]
    username = random.choice(datasets["timesheet_users"])[0]

    @print_timing
    def measure(webdriver, interaction):
        webdriver.get(f'{APPLICATION_URL}/secure/WPShowTimesheetAction!customTimesheet.jspa?periodMode=WEEK&targetType=USER&calendarType=CUSTOM&groupingType=ISSUE#targetType=USER&targetKey={username}&groupingType=Issue&periodMode=WEEK&startDate={start_date}&endDate={end_date}&periodLocked=false&calendarType=CUSTOM&saveToUserHistory=false&extraIssueFilter=&viewType=TIMESHEET')
        _wait_until(webdriver, EC.visibility_of_element_located((By.CLASS_NAME, "last_day")), interaction)
    measure(webdriver, "selenium_view_weekly_user_ts")


def view_monthly_user_ts(webdriver, datasets):
    period = random.choice(datasets["periods_monthly"])
    start_date = period[0]
    end_date = period[1]
    username = random.choice(datasets["timesheet_users"])[0]

    @print_timing
    def measure(webdriver, interaction):
        webdriver.get(f'{APPLICATION_URL}/secure/WPShowTimesheetAction!customTimesheet.jspa?periodMode=MONTH&targetType=USER&calendarType=CUSTOM&groupingType=ISSUE#targetType=USER&targetKey={username}&groupingType=Issue&periodMode=MONTH&startDate={start_date}&endDate={end_date}&periodLocked=false&calendarType=CUSTOM&saveToUserHistory=false&extraIssueFilter=&viewType=TIMESHEET')
        _wait_until(webdriver, EC.visibility_of_element_located((By.CLASS_NAME, "last_day")), interaction)
    measure(webdriver, "selenium_view_monthly_user_ts")


def view_weekly_project_ts(webdriver, datasets):
    period = random.choice(datasets["periods_weekly"])
    start_date = period[0]
    end_date = period[1]
    project_key = random.choice(datasets["projects"])[0]

    @print_timing
    def measure(webdriver, interaction):
        webdriver.get(f'{APPLICATION_URL}/secure/WPShowTimesheetAction!customTimesheet.jspa?periodMode=WEEK&targetType=PROJECT&calendarType=CUSTOM&groupingType=ISSUE#targetType=PROJECT&targetKey={project_key}&groupingType=Issue&periodMode=WEEK&startDate={start_date}&endDate={end_date}&periodLocked=false&calendarType=CUSTOM&saveToUserHistory=false&extraIssueFilter=&viewType=TIMESHEET')
        _wait_until(webdriver, EC.visibility_of_element_located((By.CLASS_NAME, "last_day")), interaction)
    measure(webdriver, "selenium_view_weekly_project_ts")


def view_monthly_project_ts(webdriver, datasets):
    period = random.choice(datasets["periods_monthly"])
    start_date = period[0]
    end_date = period[1]
    project_key = random.choice(datasets["projects"])[0]

    @print_timing
    def measure(webdriver, interaction):
        webdriver.get(f'{APPLICATION_URL}/secure/WPShowTimesheetAction!customTimesheet.jspa?periodMode=MONTH&targetType=PROJECT&calendarType=CUSTOM&groupingType=ISSUE#targetType=PROJECT&targetKey={project_key}&groupingType=Issue&periodMode=MONTH&startDate={start_date}&endDate={end_date}&periodLocked=false&calendarType=CUSTOM&saveToUserHistory=false&extraIssueFilter=&viewType=TIMESHEET')
        _wait_until(webdriver, EC.visibility_of_element_located((By.CLASS_NAME, "last_day")), interaction)
    measure(webdriver, "selenium_view_monthly_project_ts")

