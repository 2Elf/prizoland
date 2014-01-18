# -*- coding: utf-8 -*-

import unittest
import logging
from ConfigParser import SafeConfigParser

from selenium import webdriver

from prizoland.loginer import Loginer
from  prizoland.page_object import MainPage
from conf import settings


LOGIN = settings['login']
PASSWORD = settings['password']
SOCIAL_NETWORK = settings['social_network']
# TESTED_URL = 'http://rc.prizoland.com'
TESTED_URL = 'http:{0}:{1}'.format(settings['host'],
                                   settings['port'] )
CONFIG_PATH = settings['storage']

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class TestCase(unittest.TestCase):

    @staticmethod
    def setUpClass():
        '''
            It is running before executing tests.
            Here we run browser, login to defined social network
            and go to tested page
        '''
        driver = webdriver.Firefox()
        driver.implicitly_wait(60)
        loging_instance = Loginer(LOGIN, PASSWORD, SOCIAL_NETWORK, driver)
        loging_instance.log_in()
        main_page = MainPage(driver, TESTED_URL)
        main_page.login_with(SOCIAL_NETWORK)
        panda_main = main_page.go_panda_page()
        TestCase.achives_page = panda_main.continue_quest()
        TestCase.achives_page.skip_explaining()
        TestCase.driver = driver
        TestCase.config = SafeConfigParser()
        TestCase.config.read(CONFIG_PATH)

    def verify_achive_properties(self, id):
        '''
            This function is used by each test.

            It takes 'key' as parameter and use it
            for getting access to achivement (ACH) in UI and
            obtaining actual values of properties for current ACH from UI.
            We use 'key' for obtaining expected results for ACH
            from config file. And after that we compare actual and expected results.
        '''
        text_field_name = 'text'
        description_field_name = 'description_text'
        sub_description_field_name = 'sub_description_text'
        button_field_name = 'button_text'
        money_field_name = 'money'

        #  Find achivement by key and get all actual properties for it
        #  encode all values to utf-8 from unicode
        achivement = TestCase.achives_page.find_echivement_by_key(id)
        actual_text = achivement.get_text().encode('utf8')
        actual_description_text = achivement.get_description_text().encode('utf8')
        actual_sub_description_text = achivement.get_sub_description_text().encode('utf8')
        actual_button_text = achivement.get_button_text().encode('utf8')
        actual_money_costs = achivement.get_money_cost().encode('utf8')
        progress_text = achivement.get_progress_text().encode('utf8')

        #  Use TestCase.config  as config
        config = TestCase.config

        #  Print all actual properties of current achivement
        logging.debug('\nAchivement id: {0}'.format(id))
        logging.debug('Text: {0}'.format(actual_text))
        logging.debug('Description: {0}'.format(actual_description_text))
        logging.debug('Sub description: {0}'.format(actual_sub_description_text))
        logging.debug('Button_text: {0}'.format(actual_button_text))
        logging.debug('Bottom_text: {0}'.format(actual_money_costs))
        logging.debug('Progress item_text: {0}'.format(progress_text))
        logging.debug('Completed: {0}'.format(achivement.is_completed()))

        #  Check if config file doesn't contain section for current achivement
        #  we create it, write there actual results and fail test for validate
        #  results we got to the config file
        if not config.has_section(id):
            config.add_section(id)
            config.set(id, text_field_name, actual_text)
            config.set(id, description_field_name, actual_description_text)
            config.set(id, sub_description_field_name, actual_sub_description_text)
            config.set(id, button_field_name, actual_button_text)
            config.set(id, money_field_name, actual_money_costs)
            with open(CONFIG_PATH, 'wb') as configfile:
                config.write(configfile)
            self.fail('Config file doesn\'t contain values for achivment with {0} data-id'
                      .format(id))

        #  Get expected results from config file
        expected_text = config.get(id, text_field_name)
        expected_description_text = config.get(id, description_field_name)
        expected_sub_description_text = config.get(id, sub_description_field_name)
        expected_button_text = config.get(id, button_field_name)
        expected_money_costs = config.get(id, money_field_name)

        # If achivement is completed, we will gain empty values
        # for button and money.
        if achivement.is_completed():
            expected_button_text = ''
            expected_money_costs = ''

        # Compare actual and expected results.
        self.assertEqual(expected_text, actual_text,
                         'Expected text for {0}:\n "{1}" != Acual: "{2}"'\
                          .format(id, expected_text, actual_text))
        self.assertEqual(expected_description_text, actual_description_text,
                         'Expected description_text for {0}:\n "{1}" != Acual: "{2}"'\
                         .format(id, expected_description_text, actual_description_text))
        self.assertEqual(expected_sub_description_text, actual_sub_description_text,
                         'Expected sub_description_text for {0}:\n "{1}" != Acual: "{2}"'\
                         .format(id, expected_sub_description_text, actual_sub_description_text))
        self.assertEqual(expected_button_text, actual_button_text,
                         'Expected button_text for {0}: "{1}" != Acual:\n "{2}"'\
                         .format(id, expected_button_text, actual_button_text))
        self.assertEqual(expected_button_text, actual_button_text,
                         'Expected button_text for {0}: "{1}" != Acual:\n "{2}"'\
                         .format(id, expected_button_text, actual_button_text))
        self.assertEqual(expected_button_text, actual_button_text,
                         'Expected money for achivement for {0}:\n "{1}" != Acual: "{2}"'\
                         .format(id, expected_money_costs, actual_money_costs))


    def test_reg(self):
        self.verify_achive_properties('46')

    def test_first_gaming(self):
        self.verify_achive_properties('47')

    def test_first_level(self):
        self.verify_achive_properties('48')

    def test_autumn_legend(self):
        self.verify_achive_properties('49')

    # def test_active_panda(self):
    #     self.verify_achive_properties('BO2_ActivePanda')
    #
    # def test_share_progress(self):
    #     self.verify_achive_properties('ShareProgressVK')
    #
    # def test_game_per_day(self):
    #     self.verify_achive_properties('GamePerDay1')

    @unittest.expectedFailure
    def test_money(self):
        money = TestCase.achives_page.get_money()
        self.assertRaises(ValueError, int, money)

    @staticmethod
    def tearDownClass():
        '''
            It executes after running all tests,
            we close browser.
        '''
        TestCase.driver.close()
