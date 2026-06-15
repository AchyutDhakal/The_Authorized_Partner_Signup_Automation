from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import os
import time
import allure
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,20)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_clickable_element(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def find_visible_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def click_element(self, locator):
        element = self.find_clickable_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, locator, text):
        for attempt in range(3):
            try:
                element = self.find_clickable_element(locator)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                element.click()
                element.clear()
                element.send_keys(text)
                return
            except StaleElementReferenceException:
                if attempt == 2:
                    raise
                time.sleep(1)

    def is_element_present(self, locator):
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False
        
    def is_element_visible(self, locator):
        try:
            self.find_visible_element(locator)
            return True
        except TimeoutException:
            return False
        
    def get_element_text(self, locator):
        element = self.find_element(locator)
        return element.text

    def take_screenshot(self, name):
        screenshot_dir = "Screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        timestamp = time.time()
        file_name = f"{screenshot_dir}/{name}_{timestamp}.png"

        self.driver.save_screenshot(file_name)

        allure.attach.file(
            file_name,
            name=name,
            attachment_type = allure.attachment_type.PNG
        )


    def fill_form_dynamically(self, form_data: dict):
        self._scroll_full_page()
        self._fill_dropdowns(form_data)
        self._fill_inputs(form_data)
        self._fill_textareas(form_data)


    def _scroll_full_page(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        last_height = 0
        while True:
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(0.3)
            new_height = self.driver.execute_script("return window.scrollY")
            if new_height == last_height:
                break
            last_height = new_height
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)


    def _fill_dropdowns(self, form_data: dict):
        processed = set()

        while True:
            found_new = False
            selects = self.driver.find_elements(
                By.XPATH, "//select[@aria-hidden='true']"
            )

            for index, select in enumerate(selects):
                try:
                    options = select.find_elements(By.TAG_NAME, "option")
                    option_texts = [opt.text.strip() for opt in options if opt.text.strip()]
                    identifier = option_texts[0] if option_texts else f"select_{index}"
                except StaleElementReferenceException:
                    break

                if identifier in processed:
                    continue

                processed.add(identifier)
                found_new = True
                print(f"Dropdown: '{identifier}'")

                if identifier in form_data and form_data[identifier] is None:
                    print(f"  → Leaving blank")
                    break

                value = form_data.get(identifier) or (option_texts[1] if len(option_texts) > 1 else option_texts[0])
                print(f"  → Using value: '{value}'")

                try:
                    self.driver.execute_script(
                        "arguments[0].removeAttribute('aria-hidden');", select
                    )
                    from selenium.webdriver.support.ui import Select as SeleniumSelect
                    SeleniumSelect(select).select_by_visible_text(str(value))
                    print(f"  → Selected '{value}'")
                    time.sleep(0.5)
                except Exception as e:
                    print(f"  → Failed: {e}")
                break

            if not found_new:
                break

    def _fill_inputs(self, form_data: dict):
        inputs = self.driver.find_elements(By.XPATH, "//input[not(@type='hidden') and not(@type='submit') and not(@type='checkbox') and not(@type='radio') and not(@type='file')]")
        print(f"\n--- Found {len(inputs)} inputs ---")
        for input_el in inputs:
            name = input_el.get_attribute("name")
            placeholder = input_el.get_attribute("placeholder")
            input_type = input_el.get_attribute("type")
            print(f"Input: name='{name}' placeholder='{placeholder}' type='{input_type}'")
            if name in form_data and form_data[name] is None:
                print(f"  → Skipping")
                continue
            value = form_data.get(name) or form_data.get(placeholder)
            if value:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_el)
                    input_el.click()
                    input_el.clear()
                    if input_type == "date":
                        self.driver.execute_script("""
                            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                                window.HTMLInputElement.prototype, 'value').set;
                            nativeInputValueSetter.call(arguments[0], arguments[1]);
                            arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                            arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                        """, input_el, value)
                    else:
                        input_el.send_keys(str(value))
                    print(f"  → Filled '{value}'")
                except StaleElementReferenceException:
                    print(f"  → Stale, skipping")


    def _fill_textareas(self, form_data: dict):
        textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
        for textarea in textareas:
            name = textarea.get_attribute("name")
            if name in form_data and form_data[name] is None:
                continue
            value = form_data.get(name)
            if value:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", textarea)
                    textarea.click()
                    textarea.clear()
                    textarea.send_keys(value)
                    print(f"Filled textarea '{name}'")
                except StaleElementReferenceException:
                    pass


