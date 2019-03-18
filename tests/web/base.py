import abc

import pytest
from selenium.common import exceptions
from selenium.webdriver.common import by
import six


@pytest.mark.incremental
@six.add_metaclass(abc.ABCMeta)
class Page(object):
    origin = 'http://localhost:8000'
    path = None

    @pytest.fixture
    def selenium(self, selenium):
        assert self.path.startswith('/')

        url = self.get_url()

        selenium.get(url)  # Requirement 1
        return selenium

    def _create_message(self, message, **kwargs):
        if 'locator' in kwargs:
            locator = kwargs['locator']
            kwargs['locator'] = ':'.join(locator)
        if 'url' not in kwargs:
            kwargs['url'] = self.get_url()

        for key, value in six.iteritems(kwargs):
            message += '\n    {} = {}'.format(key, value)

        return message

    def get_url(self):
        return self.origin + self.path


def get_element(selenium, *args, **kwargs):
    try:
        element = selenium.find_element(*args)
        return element
    except exceptions.NoSuchElementException:
        message = kwargs.get('message')
        if message is not None:
            pytest.fail('{}\n    {}'.format(message, ' = '.join(args)))
        else:
            raise


def has_element(selenium, *args):
    try:
        selenium.find_element(*args)
        return True
    except exceptions.NoSuchElementException:
        return False


def set_input_value(selenium, xpath, value):
    """Set the value of an input element, overriding HTML maxlength attribute.

    This function sets the value of the input element specified by an XPath
    expression, bypassing the enforcement of the HTML maxlength attribute,
    which is otherwise enforced when using Selenium's send_keys() method.
    """

    def _assert_input_value(element, value):
        assert element.get_attribute('value') == str(value), \
                'Error setting value of {} to "{}"'.format(xpath, value)

    inputElement = get_element(selenium, by.By.XPATH, xpath)

    inputElement.clear()
    inputElement.send_keys(value)

    try:
        _assert_input_value(inputElement, value)
    except AssertionError as e:
        script = \
            """var result = document.evaluate('{xpath}', document, null,
                   XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
               result.value = '{value}'""".format(xpath=xpath, value=value)
        selenium.execute_script(script)

        try:
            _assert_input_value(inputElement, value)
        except AssertionError:
            raise e
