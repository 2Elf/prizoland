# -*- coding: utf-8 -*-

"""
    Module contains class that
    can log in into list of social networks:
    Vk, facebook, odnoclassniki
"""

from selenium.webdriver.common.keys import Keys

FB_PAGE = 'https://www.facebook.com/'
FB_LOGIN_ID = 'email'
FB_PASSWORD_ID = 'pass'
FB_LOGIN_BUTON_ID = 'u_0_f'
FB_LOGOUT_BUTTON_ID = 'logout_form'

VK_PAGE = 'http://vk.com/'
VK_LOGIN_ID = 'quick_email'
VK_PASSWORD_ID = 'quick_pass'
VK_LOGIN_BUTON_ID = 'quick_login_button'
VK_LOGOUT_BUTTON_ID = 'logout_link'

ODNOKLASSNIKI_PAGE = 'http://www.odnoklassniki.ru/'
ODNOKLASSNIKI_LOGIN_ID = 'field_email'
ODNOKLASSNIKI_PASSWORD_ID = 'field_password'
ODNOKLASSNIKI_LOGIN_BUTON_XP = "//input[@value='Log in']"
ODNOKLASSNIKI_LOGOUT_BUTTON_ID = ''

FB_SYNONYMS = ['fb', 'Facebook', 'Fb']
VK_SYNONYMS = ['vk', 'Vkontakte', 'Vk']
ODNOKLASSNIKI_SYNONYMS = ['Odnoklassniki']


class Loginer():
    """
        Class defines methods we use to login
        into  social networks using webdriver
        It takes auth data , webdriver, and social_network parameter.
        It starts browser, go to social network page, input auth data
        and login and then create new tab for running tests on it
    """

    def __init__(self, login, password, sosial_network, driver):
        """
        """
        self.start_page = FB_PAGE
        self.login_id = FB_LOGIN_ID
        self.password_id = FB_PASSWORD_ID
        self.login_button_ident = FB_LOGIN_BUTON_ID
        self.logout_element = FB_LOGOUT_BUTTON_ID
        self.button_access_method = driver.find_element_by_id

        if sosial_network in VK_SYNONYMS:
            self.start_page = VK_PAGE
            self.login_id = VK_LOGIN_ID
            self.password_id = VK_PASSWORD_ID
            self.login_button_ident = VK_LOGIN_BUTON_ID
            self.logout_element = VK_LOGOUT_BUTTON_ID
        elif sosial_network in ODNOKLASSNIKI_SYNONYMS:
            self.start_page = ODNOKLASSNIKI_PAGE
            self.login_id = ODNOKLASSNIKI_LOGIN_ID
            self.password_id = ODNOKLASSNIKI_PASSWORD_ID
            self.login_button_ident = ODNOKLASSNIKI_LOGIN_BUTON_XP
            self.logout_element = ODNOKLASSNIKI_LOGOUT_BUTTON_ID
            self.button_access_method = driver.find_element_by_xpath

        self.driver = driver
        self.login = login
        self.password = password


    def log_in(self):
        '''
            Method logs to defined elear social network
            and returns if it was successfully
        '''
        try:
            #  go to social network page
            self.driver.get(self.start_page)
            #  input login
            self.driver.find_element_by_id(self.login_id).clear()
            self.driver.find_element_by_id(self.login_id).send_keys(self.login)
            #  input password
            self.driver.find_element_by_id(self.password_id).clear()
            self.driver.find_element_by_id(self.password_id).send_keys(self.password)
            #  click on login button
            self.button_access_method(self.login_button_ident).click()
            self.driver.find_element_by_id(self.logout_element)
            #  open new tab for tests after login
            # time.sleep(5)
            # body = self.driver.find_element_by_tag_name('body')
            # body.send_keys(Keys.CONTROL + 't')
            return True
        except:
            return False
