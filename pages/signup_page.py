from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SignupPage(BasePage):
    LOGIN_LINK = (By.XPATH,"//p[normalize-space()='Login']")
    SIGNUP_LINK =(By.XPATH,"//a[normalize-space()='Sign Up']")
    PRIVACY_POLICY_CHECKBOX =(By.ID,"remember")
    CONTINUE_BUTTON =(By.XPATH,"//button[normalize-space()='Continue']")
    FIRST_NAME_INPUT =(By.NAME,"firstName")
    LAST_NAME_INPUT=(By.NAME,"lastName")
    EMAIL_INPUT=(By.XPATH,"//input[@id='«r2»-form-item']")
    PHONE_NUMBER_INPUT=(By.NAME,"phoneNumber")
    PASSWORD_INPUT=(By.XPATH,"//input[@name='password']")
    CONFIRM_PASSWORD_INPUT=(By.NAME,"confirmPassword")
    NEXT_BUTTON=(By.XPATH,"//button[normalize-space()='Next']")
    OTP_INPUT=(By.XPATH,"//input[@class='disabled:cursor-not-allowed']")
    VERIFY_CODE_BUTTON=(By.XPATH,"//button[normalize-space()='Verify Code']")
    RESEND_BUTTON=(By.XPATH,"//span[@class='text-primary cursor-pointer']")
    AGENCY_NAME_INPUT=(By.NAME,"agency_name")
    ROLE_IN_AGENCY=(By.NAME,"role_in_agency")
    AGENCY_EMAIL=(By.NAME,"agency_email")
    AGENCY_WEBSITE=(By.NAME,"agency_website")
    AGENCY_ADDRESS=(By.NAME,"agency_address")
    REGION_OF_OPERATION=(By.XPATH,"//button[@role='combobox']")
    REGION_SELECTION=(By.XPATH,"//span[normalize-space()='United States of America']")
    EXPERIENCE_YEAR=(By.XPATH,"//button[normalize-space()='Select Your Experience Level']")
    CLICK_EXPERIENCE=(By.XPATH,"//span[normalize-space()='1 year']")
    STUDENTS_RECRUITED=(By.NAME,"number_of_students_recruited_annually")
    FOCUS_AREA=(By.NAME,"focus_area")
    SUCCESS_METRICS=(By.NAME,"success_metrics")
    SERVICES=(By.XPATH,"//label[normalize-space()='Visa Processing']")
    BUSINESS_REGISTRATION=(By.NAME,"business_registration_number")
    PREFERRED_COUNTRIES=(By.XPATH,"//span[normalize-space()='Select Your Preferred Countries']")
    CLICK_PREFERRED_COUNTRIES=(By.XPATH,"//span[normalize-space()='United States of America']")
    PREFERRED_INSTITUTION=(By.XPATH,"//label[normalize-space()='Universities']")
    UPLOAD_FILE=(By.XPATH,"(//input[@type='file'])[1]")
    SUBMIT_BUTTON=(By.XPATH,"//button[normalize-space()='Submit']")
    PROFILE_NAME = (By.XPATH,"//h3[@class='text-[20px] font-satoshi-bold leading-snug']")


    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_signup_form(self):
        self.click_element(self.LOGIN_LINK)
        self.click_element(self.SIGNUP_LINK)
        self.click_element(self.PRIVACY_POLICY_CHECKBOX)
        self.click_element(self.CONTINUE_BUTTON)

    def enter_personal_details(self, personal_details):
        self.fill_form_dynamically(personal_details)
        self.click_element(self.NEXT_BUTTON)   

    def enter_otp(self, otp):
        self.enter_text(self.OTP_INPUT, otp)    
        self.click_element(self.VERIFY_CODE_BUTTON) 

    def enter_agency_details(self, agency_details):
        self.wait.until(EC.visibility_of_element_located(self.AGENCY_NAME_INPUT))
        self.fill_form_dynamically(agency_details)
        self.click_element(self.REGION_OF_OPERATION)
        self.click_element(self.REGION_SELECTION)
        self.click_element(self.NEXT_BUTTON)

    def enter_professional_experience(self, professional_details):
        self.wait.until(EC.visibility_of_element_located(self.EXPERIENCE_YEAR))
        self.fill_form_dynamically(professional_details)
        self.click_element(self.SERVICES)
        self.click_element(self.NEXT_BUTTON)

    def verification(self, business_number, file_path =r"G:\Downloads\469061042_878683714461045_4077351663019849769_n.jpg"):
        self.wait.until(EC.visibility_of_element_located(self.BUSINESS_REGISTRATION))
        self.fill_form_dynamically(business_number)
        self.click_element(self.PREFERRED_COUNTRIES)
        self.click_element(self.CLICK_PREFERRED_COUNTRIES)
        self.click_element(self.PREFERRED_INSTITUTION)

        self.wait.until(EC.presence_of_element_located(self.UPLOAD_FILE)).send_keys(file_path)
        





        