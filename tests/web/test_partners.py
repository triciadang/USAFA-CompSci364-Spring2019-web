from selenium.webdriver.common import by
import six

from . import base


class TestPartners(base.Page):
    path = '/partners.html'

    # Requirement 1b (Test Case 3)
    def test_service_organizations(self, selenium):
        # table header
        for header in ['Name', 'Location', 'Phone']:
            xpath = ('//table//th/descendant-or-self::*[text()'
                     '[contains(normalize-space(),"{}")]]'.format(header))
            selenium.find_element(by.By.XPATH, xpath)

        # table content
        organizations = [
            {'name': 'Habitat for Humanity',
             'location': '2802 N. Prospect St., Colorado Springs, CO 80907',
             'phone': '(719) 475-7800',
             },
            {'name': 'Salvation Army Soup Kitchen',
             'location': '908 Yuma St., Colorado Springs, CO 80909',
             'phone': '(719) 636-3891',
             },
            {'name': 'Big Brothers Big Sisters of Colorado',
             'location': ('111 S. Tejon St., Suite 302, '
                          'Colorado Springs, CO 80903'),
             'phone': '(719) 633-2443',
             },
            {'name': 'Keep Colorado Springs Beautiful Inc.',
             'location': '20 E. Rio Grande St., Colorado Springs, CO 80903',
             'phone': '(719) 577-9111',
             },
        ]
        for organization in organizations:
            for key, value in six.iteritems(organization):
                xpath = ('//table//td/descendant-or-self::*[text()'
                         '[contains(normalize-space(),"{}")]]'.format(value))

                locator = (by.By.XPATH, xpath)
                message = ('Cannot find {} "{}" in service partners '
                           'table'.format(key, value, self.path))
                assert base.has_element(selenium, *locator), \
                    self._create_message(message, locator=locator)
