# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
from loginer import Loginer
from  page_object import MainPage

LOGIN = "zaxarenkovr@bk.ru"
PASSWORD = "zRQB792"
SOCIAL_NETWORK = 'Facebook'
TESTED_URL = 'http://prizoland.com'


class TestCase(unittest.TestCase):

    @staticmethod
    def setUpClass():
        driver = webdriver.Firefox()
        driver.implicitly_wait(60)
        loging_instance = Loginer(LOGIN , PASSWORD, SOCIAL_NETWORK,  driver)
        loging_instance.log_in()
        main_page = MainPage(driver, TESTED_URL)
        main_page.login_with(SOCIAL_NETWORK)
        bubble_main = main_page.go_bubble_page()
        TestCase.achives_page = bubble_main.continue_quest()
        TestCase.achives_page.skip_explaining()
        TestCase.driver = driver

    def test_reg(self):
        achivement = TestCase.achives_page.find_echivement_by_key('Register')
        print achivement.text
        self.assertEqual(u'Авторизация', achivement.get_text())

    def test_like_fb(self):
        achivement = TestCase.achives_page.find_echivement_by_key('LikeFB')
        print achivement.text
        self.assertEqual(u'Группа поддержки', achivement.get_text())

    @unittest.expectedFailure
    def test_money(self):
        money = TestCase.achives_page.get_money()
        self.assertRaises(ValueError,int, money)

    @staticmethod
    def tearDownClass():
        TestCase.driver.close()


if __name__ == '__main__':
    unittest.main()



