import unittest

from e5toolbox.scrapper.E5SeleniumWebdriver import E5SeleniumWebDriver


# E5
class E5SeleniumWebdriverTest(unittest.TestCase):

    # E5
    def test_init(self) -> None:
        e5webdriver: E5SeleniumWebDriver = E5SeleniumWebDriver()

        # Act
        e5webdriver.init()

        # Assert
        self.assertTrue(expr=e5webdriver.status.success,
                        msg=f"{e5webdriver.status.error_context} : {e5webdriver.status.exception}")
        self.assertTrue(expr=e5webdriver.is_connected,
                        msg=f"{e5webdriver.status.error_context} : {e5webdriver.status.exception}")

        # Quit
        e5webdriver.quit()

    # E5
    def test_quit(self) -> None:
        e5webdriver: E5SeleniumWebDriver = E5SeleniumWebDriver()
        e5webdriver.init()

        # Act
        e5webdriver.quit()

        # Assert
        self.assertTrue(e5webdriver.status.success,
                        msg=f"{e5webdriver.status.error_context} : {e5webdriver.status.exception}")
        self.assertFalse(e5webdriver.is_connected,
                         msg=f"{e5webdriver.status.error_context} : {e5webdriver.status.exception}")
