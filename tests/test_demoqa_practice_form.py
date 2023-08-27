import allure
import data.users as users
from pages.registration_page import RegistrationPage


@allure.title("Successful registration")
def test_filling_form(setup_browser):
    with allure.step('Open a registration page'):
        page = RegistrationPage()
        page.open()

    with allure.step('Fill the registration form'):
        page.register(users.john)

    with allure.step('Check if the registration was successful'):
        page.assert_registration(users.john)
