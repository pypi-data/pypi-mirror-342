from clicknium.core.models.web.basewebdriver import BaseWebDriver
from clicknium.core.models.web.webextension import WebExtension


class WebDriver(BaseWebDriver):

    def __init__(self, browser_type, is_custom = False):
        super(WebDriver, self).__init__(browser_type, is_custom)
        self.extension = WebExtension(browser_type, is_custom)