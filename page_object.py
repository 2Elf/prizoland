# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


class PagePattern():
    def __init__(self, driver):
        self.driver = driver

    def get_current_url(self):
        '''
            It returns current url
        '''
        return self.driver.current_url


    def go_page(self, url):
        '''
            It goes to page
        '''
        self.driver.get(url)

    def mouse_over_on(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        return self


class MainPage(PagePattern):
    login_class_name = 'login-link'
    bubble_coocing_link_text = 'Продолжить квест'
    panda_continue_link_text = 'Продолжить'
    panda_begin_link_text = 'Начать'


    def __init__(self, driver, start_url):
        PagePattern.__init__(self, driver)
        self.go_page(start_url)
        self.is_logged = False


    def login_with(self, sn_name='Facebook'):
        if sn_name in ['fb', 'FB']:
            sn_name = 'Facebook'
        elif sn_name in ['Vk', 'vk']:
            sn_name = 'Вконтакте'
        elif sn_name in ['Odnoklassniki']:
            sn_name = 'Одноклассники'
        self.driver.find_element_by_class_name(MainPage.login_class_name).click()
        self.driver.find_element_by_link_text(sn_name).send_keys(Keys.ENTER)
        self.is_logged = True
        return self

    def go_bubble_page(self):
        '''
            It clicks on reference to continue bubble quest
            and goes to bubble quest page
        '''
        self.driver.find_element_by_link_text(MainPage.bubble_coocing_link_text).click()
        return BubbleCookingMain(self.driver)

    def go_panda_page(self):
        '''

        '''
        self.driver.find_element_by_link_text(MainPage.panda_continue_link_text).click()
        return PandaMain(self.driver)


class BubbleCookingMain(PagePattern):
    '''

    '''
    continue_link_text = 'Продолжить'

    def continue_quest(self):
        '''
            It clicks on button 'Продолжить квест'
        '''
        self.driver.find_element_by_link_text(BubbleCookingMain.continue_link_text).click()
        return AchivesPage(self.driver)


class PandaMain(PagePattern):
    '''
        It contains methods to access controls
        on Panda game web Page
    '''
    continue_link_text = 'Продолжить'

    def continue_quest(self):
        '''
            It continues
        '''
        self.driver.find_element_by_link_text(PandaMain.continue_link_text).click()
        return AchivesPage(self.driver)


class AchivesPage(PagePattern):
    '''
        It contains method for access to achivments
    '''
    skip_link_text = 'пропустить'
    money_element_xpath = '//span[@tokenanim="userTokens"]'

    def __init__(self, driver):
        PagePattern.__init__(self, driver)
        self.is_logged = False

    def skip_explaining(self):
        '''
            It skips message with explaining
            how it works
        '''
        self.driver.find_element_by_link_text(AchivesPage.skip_link_text).click()
        return self

    def find_echivement_by_key(self, data_key):
        achivement = Achivement(self.driver, data_key)
        return achivement

    def get_money(self):
        money_element = self.driver.find_element_by_xpath(AchivesPage.money_element_xpath)
        return money_element.text


class Achivement:
    achivement_key_xpath_pattern = "//article[@data-key='{0}']"
    description_css_selector = 'div.achievement__description.ng-binding'
    sub_description_css_selector = 'div.achievement__sub-description.ng-binding'
    progress_class_name = 'icon-timed__inner'
    bottom_class_name = 'achievement__bottom'
    button_tag_name = 'button'
    class_value_completed = 'achievement_state_completed'


    def __init__(self, driver, key):
        self.driver = driver
        self.ref = driver.find_element_by_xpath(Achivement.achivement_key_xpath_pattern.format(key))
        self.class_value = self.ref.get_attribute('class')
        self.text = self.ref.text
        #  over on achivement to get overlay data (description, sub_description, button)
        actions = ActionChains(self.driver)
        actions.move_to_element(self.ref).perform()
        actions.release(self.ref).perform()
        actions.move_to_element(self.ref).perform()
        self.description = self.ref.find_element_by_css_selector( \
            Achivement.description_css_selector)
        self.sub_description = self.ref.find_element_by_css_selector( \
            Achivement.sub_description_css_selector)
        actions.release(self.ref).perform()
        actions.move_to_element(self.ref).perform()
        self.progress_icon = self.ref.find_element_by_class_name(Achivement.progress_class_name)
        self.button = self.ref.find_element_by_tag_name(Achivement.button_tag_name)
        #  get bottom element
        self.bottom = self.ref.find_element_by_class_name(Achivement.bottom_class_name)
        actions.release(self.ref).perform()


    def get_ref(self):
        '''
            It returns achivement bloc element
        '''
        return self.ref

    def get_text(self):
        '''
            It returns achivement text ( see detail in http://clip2net.com/s/6u4O0f )
            excluding bottom_text and progress_icon_text
        '''
        text = self.text.replace(self.bottom.text, '').strip()
        text = text.replace(self.get_progress_text(), '').strip()
        return text

    def get_money_cost(self):
        return self.bottom.text

    def get_progress_text(self):
        return self.progress_icon.text

    def get_description_text(self):
        '''
            It returns description text. ( see detail in http://clip2net.com/s/6u4O0f )
            self.description.text contains both : description_text and
            sub_description_text, so we replace sub_description_text with ''(empty string)
            and after that strip it, and get true description_text
        '''
        sub_description_text = self.get_sub_description_text()
        text = self.description.text
        text = text.replace(sub_description_text, '').strip()
        return text

    def get_sub_description_text(self):
        return self.sub_description.text

    def get_button_text(self):
        return self.button.text

    def is_completed(self):
        return Achivement.class_value_completed in self.class_value

