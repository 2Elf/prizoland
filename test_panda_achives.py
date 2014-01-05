# -*- coding: utf-8 -*-

import unittest
from ConfigParser import SafeConfigParser
from selenium import webdriver
from loginer import Loginer
from  page_object import MainPage
import time

LOGIN = "79670452475"
PASSWORD = "C3NPWqjRe"
SOCIAL_NETWORK = 'vk'
TESTED_URL = 'http://prizoland.com'
CONFIG_PATH = 'achives_data.cfg'


class TestCase(unittest.TestCase):
    @staticmethod
    def setUpClass():
        driver = webdriver.Firefox()
        driver.implicitly_wait(60)
        loging_instance = Loginer(LOGIN, PASSWORD, SOCIAL_NETWORK, driver)
        loging_instance.log_in()
        main_page = MainPage(driver, TESTED_URL)
        main_page = main_page.login_with(SOCIAL_NETWORK)
        panda_main = main_page.go_panda_page()
        TestCase.achives_page = panda_main.continue_quest()
        TestCase.achives_page.skip_explaining()
        TestCase.driver = driver
        TestCase.config = SafeConfigParser()
        TestCase.config.read(CONFIG_PATH)

    def verify_achive_properties(self, key):
        text_field_name = 'text'
        description_field_name = 'description_text'
        sub_description_field_name = 'sub_description_text'
        button_field_name = 'button_text'
        money_field_name = 'money'

        #  Find achivement by key and get all actual properties for it
        #  encode all values to utf-8 from unicode
        achivement = TestCase.achives_page.find_echivement_by_key(key)
        actual_text = achivement.get_text().encode('utf8')
        actual_description_text = achivement.get_description_text().encode('utf8')
        actual_sub_description_text = achivement.get_sub_description_text().encode('utf8')
        actual_button_text = achivement.get_button_text().encode('utf8')
        actual_money_costs = achivement.get_money_cost().encode('utf8')
        progress_text = achivement.get_progress_text().encode('utf8')
        #  Use TestCase.config  as config
        config = TestCase.config
        #  Print all actual properties of current achivement
        print key
        print 'Text: {}'.format(actual_text)
        print 'Description: {0}'.format(actual_description_text)
        print 'Sub description: {0}'.format(actual_sub_description_text)
        print 'Button_text: {0}'.format(actual_button_text)
        print 'Bottom_text: {0}'.format(actual_money_costs)
        print 'Progress item_text: {0}'.format(progress_text)
        print 'Completed: {0}'.format(achivement.is_completed())
        print ''
        #  Check if config file doesn't contain section for current achivement
        #  we create it, write there actual results and fail test for validate
        #  results we got to the config file
        if not config.has_section(key):
            config.add_section(key)
            config.set(key, text_field_name, actual_text)
            config.set(key, description_field_name, actual_description_text)
            config.set(key, sub_description_field_name, actual_sub_description_text)
            config.set(key, button_field_name, actual_button_text)
            config.set(key, money_field_name, actual_money_costs)
            with open(CONFIG_PATH, 'wb') as configfile:
                config.write(configfile)
            self.fail('Config file doesn\'t contain values for achivment with {0} data-key'
            .format(key))
            #  Get expected results from config file
        expected_text = config.get(key, text_field_name)
        expected_description_text = config.get(key, description_field_name)
        expected_sub_description_text = config.get(key, sub_description_field_name)
        expected_button_text = config.get(key, button_field_name)
        expected_money_costs = config.get(key, money_field_name)
        #  If achivement is completed, we will gain empty values
        #  for button and money
        if achivement.is_completed():
            expected_button_text = ''
            expected_money_costs = ''
            #  compare actual and expected results
        self.assertEqual(expected_text, actual_text,
                         'Expected text for {0}: "{1}" != Acual: "{2}"'.format(key, expected_text,
                                                                               actual_text))
        self.assertEqual(expected_description_text, actual_description_text,
                         'Expected description_text for {0}: "{1}" != Acual: "{2}"'.format(key,
                                                                                           expected_description_text,
                                                                                           actual_description_text))
        self.assertEqual(expected_sub_description_text, actual_sub_description_text,
                         'Expected sub_description_text for {0}: "{1}" != Acual: "{2}"'.format(key,
                                                                                               expected_sub_description_text,
                                                                                               actual_sub_description_text))
        self.assertEqual(expected_button_text, actual_button_text,
                         'Expected button_text for {0}: "{1}" != Acual: "{2}"'.format(key, expected_button_text,
                                                                                      actual_button_text))
        self.assertEqual(expected_button_text, actual_button_text,
                         'Expected button_text for {0}: "{1}" != Acual: "{2}"'.format(key, expected_button_text,
                                                                                      actual_button_text))
        self.assertEqual(expected_button_text, actual_button_text,
                         'Expected money for achivement for {0}: "{1}" != Acual: "{2}"'.format(key,
                                                                                               expected_money_costs,
                                                                                               actual_money_costs))

    def test_reg(self):
        self.verify_achive_properties('Register')

    def test_first_gaming(self):
        self.verify_achive_properties('Install')

    def test_first_level(self):
        self.verify_achive_properties('BO1_FirstLevel')

    def test_autumn_legend(self):
        self.verify_achive_properties('BO1_PlatinumPanda')

    def test_active_panda(self):
        self.verify_achive_properties('BO2_ActivePanda')

    def test_share_progress(self):
        self.verify_achive_properties('ShareProgressVK')

    def test_game_per_day(self):
        self.verify_achive_properties('GamePerDay_BO')

    @unittest.expectedFailure
    def test_money(self):
        money = TestCase.achives_page.get_money()
        self.assertRaises(ValueError, int, money)

    @staticmethod
    def tearDownClass():
        TestCase.driver.close()


if __name__ == '__main__':
    unittest.main()



