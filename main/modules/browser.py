from .wait import Wait


class Browser:
    def __init__(self, driver):
        self.driver = driver
        self.wait = Wait(driver)

    def scroll_to_element(self, element, offset=0):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        if offset != 0:
            script = "window.scrollTo(0, window.pageYOffset + " + str(offset) + ");"
            self.driver.execute_script(script)

    def scroll_to_element_by_xpath(self, xpath, offset=0):
        element = self.wait.find_element_by_xpath(xpath)
        self.scroll_to_element(element, offset)
