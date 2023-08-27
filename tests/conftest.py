import pytest
import os
from selenium import webdriver
from dotenv import load_dotenv
from selene import browser
from utils import attach
from selenium.webdriver.chrome.options import Options

RES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))
DEFAULT_BROWSER_VERSION = '100.0'


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='100.0'
    )

@pytest.fixture(scope='function')
def setup_browser(request):
    browser.config.base_url = 'https://demoqa.com'

    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION

    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    browser.config.driver = driver
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video(browser)

    browser.quit()
