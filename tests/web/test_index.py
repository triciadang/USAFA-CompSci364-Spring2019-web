from selenium.webdriver.common import by
from six.moves.urllib import parse as urlparse

from . import base


class TestIndex(base.Page):
    path = '/index.html'  # Requirement 1

    # Requirement 1 (Test Case 1)
    def test_website_available(self, selenium):
        assert self.path == urlparse.urlparse(selenium.current_url).path, \
            'CSL website is not available ({})'.format(self.get_url())

    # Requirement 1.a (Test Case 2)
    def test_contains_description_and_image(self, selenium):
        description = ('The Cadet Service Learning program is designed to '
                       'foster and facilitate service learning activities for '
                       'cadets at the United States Air Force Academy.')

        xpath = ('//body/descendant::*[text()[contains('
                 'normalize-space(),"{}")]]'.format(description))
        locator = (by.By.XPATH, xpath)
        assert base.has_element(selenium, *locator), \
            self._create_message('Missing CSL description', locator=locator)

        assert selenium.find_element(by.By.TAG_NAME, 'img')
        assert selenium.find_element(by.By.XPATH, '//img[@src="csl-logo.jpg"]')
