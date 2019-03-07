from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os

from gmail import Gmail

DEBUG = False
HEADLESS = False

@fixture
def browser(context):
    options = ChromeOptions()
    # options = FirefoxOptions()
    # options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    if HEADLESS:
        options.add_argument('--headless')
        if DEBUG:
            options.add_argument('--remote-debugging-port=9222')
    context.browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
    # context.browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_options=options)
    yield context.browser
    context.browser.quit()

def before_all(context):
    context.gmail = Gmail(context, timeout=30)

def before_scenario(context, scenario):
    use_fixture(browser, context)

def after_scenario(context, scenario):
    context.gmail.delete_emails()
    context.browser.quit()

def after_step(context, step):
    if DEBUG and step.status == 'failed':
        step_name = step.name.replace(' ', '_')
        image_name = os.path.join(context.gmail.debug_dir, f'{step.step_type}_{step_name}.png')
        context.browser.save_screenshot(image_name)
