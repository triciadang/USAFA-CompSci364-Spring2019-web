from builtins import range

from selenium.webdriver.common import by
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import ui
import six
from six.moves.urllib import parse as urlparse

from . import base


class TestVolunteer(base.Page):
    path = '/volunteer.html'  # Requirement 1

    # Requirement 1.c (Test Case 4)
    def test_page_contains_form(self, selenium):
        form = selenium.find_element(by.By.XPATH, '//form[@action="demo.php"]')
        assert form.get_attribute('method') == 'post'

        for name in ['firstName', 'lastName', 'emailAddress', 'age', 'gender',
                     'carAccess']:
            assert selenium.find_element(
                by.By.XPATH,
                '//form[@action="demo.php"]//input[@name="{}"]'.format(name))

    def _input_form_values(self, selenium, **kwargs):
        # default values for form fields -- all valid
        values = {
            'firstName': 'John',
            'lastName': 'Doe',
            'emailAddress': 'john.doe@example.com',
            'age': 20,
            'gender': 'male',
            'carAccess': False,
        }
        values.update(**kwargs)  # overwrite with specified values

        for name, value in six.iteritems(values):
            xpath = ('//form[@action="demo.php"]'
                     '//input[@name="{}"]').format(name)
            inputElement = selenium.find_element(by.By.XPATH, xpath)

            inputElementType = inputElement.get_attribute('type')
            if 'radio' == inputElementType:
                inputElement.find_element(
                        by.By.XPATH,
                        '..//input[@name="{}" and @value="{}"]'.format(name,
                                                                       value))
                inputElement.click()
            elif 'checkbox' == inputElementType:
                if inputElement.is_selected() != value:
                    inputElement.click()
            else:
                inputElement.clear()
                inputElement.send_keys(value)

    # Requirement 1.d (Test Case 5)
    def test_empty_form_validation(self, selenium):
        form = selenium.find_element(by.By.XPATH, '//form[@action="demo.php"]')
        form.submit()

        assert self.path == urlparse.urlparse(selenium.current_url).path

    def _test_form_validation(self, selenium, name, value, path=None):
        if path is None:
            path = self.path

        self._input_form_values(selenium)

        xpath = ('//form[@action="demo.php"]//input[@name="{}"]').format(name)
        inputElement = selenium.find_element(by.By.XPATH, xpath)

        base.set_input_value(selenium, xpath, value)
        inputElement.submit()

        assert path == urlparse.urlparse(selenium.current_url).path, \
            'Volunteer form submission with {} = "{}"'.format(name, value)

        # TODO: Check for error message

    # Requirement 1.d.i (Test Case 6)
    def test_form_validation_firstname_okay(self, selenium):
        for value in ['characters', 'CAPITALIZED', 'hyphen-ated']:
            # following successful form submission, the URL will be /demo.php
            # so load the original URL (i.e., /volunteer.html) before the next
            # test value
            selenium.get(self.get_url())
            assert self.path == urlparse.urlparse(selenium.current_url).path

            self._test_form_validation(selenium, 'firstName', value,
                                       path='/demo.php')

    # Requirement 1.d.i (Test Case 7)
    def test_form_validation_lastname_invalid_character(self, selenium):
        for value in ['1', '_', '.', '[', 'invalid 1', 'invalid_']:
            self._test_form_validation(selenium, 'lastName', value)

    # Requirement 1.d.i (Test Case 8)
    def test_form_validation_lastname_length(self, selenium):
        self._test_form_validation(selenium, 'lastName', 'A' * 50 + 'Z')

    # Requirement 1.d.i (Test Case 9)
    def test_form_validation_lastname_okay(self, selenium):
        for value in ['characters', 'CAPITALIZED', 'hyphen-ated']:
            # following successful form submission, the URL will be /demo.php
            # so load the original URL (i.e., /volunteer.html) before the next
            # test value
            selenium.get(self.get_url())
            assert self.path == urlparse.urlparse(selenium.current_url).path

            self._test_form_validation(selenium, 'lastName', value,
                                       path='/demo.php')

    # Requirement 1.d.i (Test Case 10)
    def test_form_validation_firstname_invalid_character(self, selenium):
        for character in ['1', '_', '.', '[', 'invalid 1', 'invalid_']:
            self._test_form_validation(selenium, 'firstName', character)

    # Requirement 1.d.i (Test Case 11)
    def test_form_validation_firstname_length(self, selenium):
        self._test_form_validation(selenium, 'firstName', 'A' * 50 + 'Z')

    # Requirement 1.d.ii (Test Case 12)
    def test_form_validation_email_okay(self, selenium):
        for value in ['valid.address@example.com', 'Valid.address@example.com',
                      'valid-address@example.com', 'valid_address@example.com',
                      'valid123@example.com']:
            # following successful form submission, the URL will be /demo.php
            # so load the original URL (i.e., /volunteer.html) before the next
            # test value
            selenium.get(self.get_url())
            assert self.path == urlparse.urlparse(selenium.current_url).path

            self._test_form_validation(selenium, 'emailAddress', value,
                                       path='/demo.php')

    # Requirement 1.d.ii (Test Case 13)
    def test_form_validation_email_invalid_character(self, selenium):
        for character in ['#', '*', '&', '@']:
            address = 'invalid' + character + '@example.com'
            self._test_form_validation(selenium, 'emailAddress', address)

    # Requirement 1.d.ii (Test Case 14)
    def test_form_validation_email_length(self, selenium):
        self._test_form_validation(selenium, 'emailAddress',
                                   'A' * 50 + '@example.com')

    # Requirement 1.d.ii (Test Case 15)
    def test_form_validation_email_without_at_sign(self, selenium):
        self._test_form_validation(selenium, 'emailAddress', 'invalid.address')

    # Requirement 1.d.iii (Test Case 16)
    def test_form_validation_age_okay(self, selenium):
        for value in range(17, 30):
            # following successful form submission, the URL will be /demo.php
            # so load the original URL (i.e., /volunteer.html) before the next
            # test value
            selenium.get(self.get_url())
            assert self.path == urlparse.urlparse(selenium.current_url).path

            self._test_form_validation(selenium, 'age', value,
                                       path='/demo.php')

    # Requirement 1.d.iii (Test Case 17)
    def test_form_validation_age_not_numeric(self, selenium):
        for value in ['not numeric', 'neither', '#', '123+something']:
            self._test_form_validation(selenium, 'age', value)

    # Requirement 1.d.iii (Test Case 18)
    def test_form_validation_age_under_limit(self, selenium):
        self._test_form_validation(selenium, 'age', 16)

    # Requirement 1.d.iii (Test Case 19)
    def test_form_validation_email_over_limit(self, selenium):
        self._test_form_validation(selenium, 'age', 30)

    # Requirement 1.e (Test Case 20)
    def test_form_submission(self, selenium):
        self._input_form_values(selenium)

        form = selenium.find_element(by.By.XPATH, '//form[@action="demo.php"]')
        form.submit()

        ui.WebDriverWait(selenium, 3).until(
            expected_conditions.url_to_be(self.origin + '/demo.php')
        )
