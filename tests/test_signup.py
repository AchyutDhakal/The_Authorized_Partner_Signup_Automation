import pytest
from pages.signup_page import SignupPage
from utils.test_runner import create_driver
from utils.otp_reader import get_otp_from_email
from data.test_data import VALID_DATA
from utils.assertions import assert_true, assert_equal
import time
import allure


class TestSignup:
    def setup_method(self):
        self.driver = create_driver()
        self.signup_page = SignupPage(self.driver)

        self.driver.get("https://authorized-partner.vercel.app/")

    def teardown_method(self):
        self.driver.quit()

    @allure.title("Test User Signup")
    @pytest.mark.parametrize("valid_data",VALID_DATA)
    def test_user_signup(self, valid_data):
        with allure.step("Navigate to Signup form"):
            self.signup_page.navigate_to_signup_form()

        with allure.step("Asserting navigation to signup form"):
            assert_true(self.signup_page.is_element_visible(self.signup_page.FIRST_NAME_INPUT), "Could not navigate to signup form", "navigate_to_signup", self.signup_page)

        with allure.step("Fill up personal details"):
            self.signup_page.enter_personal_details(valid_data)

        with allure.step("Enter otp"):
            self.signup_page.enter_otp(get_otp_from_email())
        
        with allure.step("Filling out Agency Details"):
            self.signup_page.enter_agency_details(valid_data)

        with allure.step("Filling up professional experience"):
            self.signup_page.enter_professional_experience(valid_data)

        with allure.step("Verification and preferences"):
            self.signup_page.verification(valid_data)
            self.signup_page.click_element(self.signup_page.SUBMIT_BUTTON)

        with allure.step("Assertion"):
            profile_name = self.signup_page.get_element_text(self.signup_page.PROFILE_NAME)
            assert_equal(profile_name, f"{valid_data["firstName"]} {valid_data["lastName"]}", "Actual and expected names don't match", "signup", self.signup_page)


