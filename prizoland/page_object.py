# -*- coding: utf-8 -*-

import logging
import time

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


DEFAULT_IMPLICITY_WAIT = 60
SMALL_IMPLICITY_WAIT = 5

class PagePattern():
    '''
        Page pattern class gather common behaviour
        for all tested web pages.

        Properties:
            driver - passed into constructor selenium.webdriver.X()
        Methods:
            get_current_url() - returns current url
            go_page(url) - go to passed page 'url'
            mouse_over_on(element) - over mouse on 'element'
    '''

    def __init__(self, driver):
        self.driver = driver

    def get_current_url(self):
        '''It return current url.'''
        return self.driver.current_url


    def go_page(self, url):
        '''It open page url.'''
        self.driver.get(url)
        return self

    def mouse_over_on(self, element):
        '''Function does mouse over on.'''
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        return self


class MainPage(PagePattern):
    '''
        Main page class gather function
        for main page of tested source.
        Is inherited from PagePattern.

        Methods:
            login_with(sn_name) - login to tested site with
                                  passed social network 'sn_name'
            go_bubble_page() - goes to BubbleCooking quest page
            go_panda_page() - goes to Panda quest page
    '''
    login_class_name = 'login-link'
    bubble_coocing_link_text = 'Продолжить квест'
    panda_continue_link_text = 'Продолжить'
    panda_begin_link_text = 'Начать'

    def __init__(self, driver, start_url):
        PagePattern.__init__(self, driver)
        self.go_page(start_url)
        self.is_logged = False

    def login_with(self, sn_name='Facebook'):
        '''
            Login to site using passed social network

            Method is used for login from main page.
            We click on login link, and after that,
            depends on passed parameter sn_name',
            we choose on which reference we click.
            It returns self.

            Parameters:
                sn_name - name of social network we use for login
                         Possible values:
                               'Facebook'(default), 'fb', 'Fb', 'FB',
                               'Vk', 'vk', 'VK',
                               'Odnoklassniki'
        '''
        if sn_name in ['fb', 'FB', 'Fb']:
            sn_name = 'Facebook'
        elif sn_name in ['Vk', 'vk', 'VK']:
            sn_name = 'Вконтакте'
        elif sn_name in ['Odnoklassniki']:
            sn_name = 'Одноклассники'
        self.driver.find_element_by_class_name(MainPage.login_class_name).click()
        self.driver.find_element_by_link_text(sn_name).send_keys(Keys.ENTER)
        self.is_logged = True
        return self

    def go_bubble_page(self):
        '''
            It clicks on reference to continue 'Bubble' quest
            and goes to bubble quest page.

            It returns instance of BubbleCookingMain class.
        '''
        self.driver.find_element_by_link_text(MainPage.bubble_coocing_link_text).click()
        return BubbleCookingMain(self.driver)

    def go_panda_page(self):
        '''
            First we try begin quest and click on
            button 'Начать'.
            If it is not evailable we try click
            button "Продолжить"

            It returns instance of PandaMain class
        '''
        begin_link_text = MainPage.panda_begin_link_text
        continue_link_text = MainPage.panda_continue_link_text
        self.driver.implicitly_wait(SMALL_IMPLICITY_WAIT)
        try:
            self.driver.find_element_by_link_text(begin_link_text).click()
        except NoSuchElementException:
            self.driver.find_element_by_link_text(continue_link_text).click()
        self.driver.implicitly_wait(DEFAULT_IMPLICITY_WAIT)
            # logging.DEBUG('We got NoSuchElementException on finding {0}'
            #               .format(begin_link_text))
        logging.info('We went to Panda quest page ')
        return PandaMain(self.driver)

class ChoosePage(PagePattern):
    '''
        Class gather methods available on
        choose page
    '''
    continue_link_xpath = '''//button[@ng-click="choose_continue('/BubbleOrigins/play/')"]'''
    prize_group_xpath = '//div[@class="choose__group group_order_{0}"]'
    priz_image_class = 'prize__image'
    choose_button_class = 'button'

    def __init__(self, driver):
        PagePattern.__init__(self, driver)
        self.new_choose = 'choose-prizes' in self.driver.current_url
        if self.new_choose:
            self.prises_choosen = True

    def choose_prizes(self):
        '''
        It choose three first prizes in the list
        '''
        for group_id in range(1,4):
            grop_xpath = ChoosePage.prize_group_xpath.format(group_id)
            group = self.driver.find_element_by_xpath(grop_xpath)
            prize_element = group.find_element_by_class_name(ChoosePage.priz_image_class)
            self.mouse_over_on(prize_element)
            group.find_element_by_class_name(ChoosePage.choose_button_class).click()

    def continue_with_it(self):
        '''
        It click on  'Продолжить' link
        after prizes choosing.
        '''
        if self.new_choose:
            self.driver.find_element_by_xpath(ChoosePage.continue_link_xpath).click()
        else:
            self.choose_prizes()

        return self

class QuestMain(PagePattern):
    '''
       It gather common functions for quest
       pages BubbleCooking and Panda

       Methods:
       continue_quest() - it goes to page with achievements
    '''
    continue_link_text = 'Продолжить'

    def continue_quest(self):
        '''
            It goes to page with achievements

            It clicks on button 'Продолжить', goes to
            page with achievements and returns instance
            of AchivesPage class.
        '''
        self.driver.find_element_by_link_text(QuestMain.continue_link_text).click()
        time.sleep(SMALL_IMPLICITY_WAIT)
        if 'choose' in self.driver.current_url:
            choose_page = ChoosePage(self.driver)
            choose_page.continue_with_it()

        return AchivesPage(self.driver)


class BubbleCookingMain(QuestMain):
    '''
        It contains methods to access controls
        unique on BubbleCooking quest page
    '''
    pass


class PandaMain(QuestMain):
    '''
        It contains methods to access controls
        unique on Panda quest page
    '''
    pass


class AchivesPage(PagePattern):
    '''
        Class contains methods for access to elements
        on achievements page .
        It is inherited form PagePattern.

        Properties:
            self.is_logged - boolean if some user is logged now
        Methods:
            skip_explaining() - press on
            find_echivement_by_key(data_key) - return instance
                of Achivement class found by data_key
            get_money() - it return number of earned money in text
    '''
    skip_link_text = 'пропустить'
    money_element_xpath = '//span[@tokenanim="userTokens"]'
    achives_popup_xpath = '//div[@class="dialogs dialogs_type_done-tasks"]'
    exelent_link_tag = 'button'

    def __init__(self, driver):
        PagePattern.__init__(self, driver)
        self.is_logged = False

    def handle_new_achives(self):
        '''
           It waits for new achives
           and click on 'Отлично' button.
        '''
        self.driver.implicitly_wait(SMALL_IMPLICITY_WAIT)
        handled = False
        count = 0
        while not handled:
            count += 1
            try:
                achives_popup = self.driver.find_element_by_xpath(AchivesPage.achives_popup_xpath)
                exelent_link = achives_popup.find_element_by_tag_name(AchivesPage.exelent_link_tag)
                counter = 0
                while not exelent_link.is_displayed():
                    counter += 1
                    time.sleep(1)
                    if counter >=DEFAULT_IMPLICITY_WAIT:
                        break
                exelent_link.click()
                handled = True
            except:
                logging.info("Pop up on new achives doesn't appear or wos not found")
            self.driver.refresh()
            if count == 2:
               break
        self.driver.implicitly_wait(DEFAULT_IMPLICITY_WAIT)
        return handled


    def skip_explaining(self):
        '''
            It skips message with explaining
            how user earn his virtual money
        '''
        link = AchivesPage.skip_link_text
        try:
            self.driver.find_element_by_link_text(link).click()
        except NoSuchElementException:
            logging.debug('Link {0} was not found'.format(link))
        return self

    def find_echivement_by_key(self, data_key):
        '''
            It is looking for achivement
            and return instance of Achivement
            class.
        '''
        return Achivement(self.driver, data_key)

    def get_money(self):
        '''
           It return number of earned money
           in text format.
        '''
        money_element = self.driver.find_element_by_xpath(AchivesPage.money_element_xpath)
        return money_element.text


class Achivement:
    '''
        Class of achivement element collect achivement
        properties and methods we can do with it.

        Methods:
            get_ref() - return achivement element (selenium element object)
            get_text() - return achivement text
            get_money_cost() - return money for achivement in string
            get_progress_text() - return progress text
            get_description_text() - return description text
            get_sub_description_text() - return sub description text
            get_button_text() - return button text
            is_completed - return if achivement is completed (boolean)
    '''
    achivement_id_xpath_pattern = "//article[@data-id='{0}']"
    description_css_selector = 'div.achievement__description.ng-binding'
    sub_description_css_selector = 'div.achievement__sub-description.ng-binding'
    progress_class_name = 'icon-timed__inner'
    bottom_class_name = 'achievement__bottom'
    button_tag_name = 'button'
    class_value_completed = 'achievement_state_completed'

    def __init__(self, driver, id):
        self.driver = driver
        try:
            xpath = Achivement.achivement_id_xpath_pattern.format(id)
            self.ref = driver.find_element_by_xpath(xpath)
        except NoSuchElementException as err:
            raise NameError('Got {0} when try detect {1}'.format(err, xpath))

        self.class_value = self.ref.get_attribute('class')
        self.text = self.ref.text
        # Over on achivement to get overlay data (description, sub_description, button).
        actions = ActionChains(self.driver)
        actions.move_to_element(self.ref).perform()
        actions.release(self.ref).perform()
        actions.move_to_element(self.ref).perform()
        self.description = self.ref.find_element_by_css_selector(
                                Achivement.description_css_selector)
        self.sub_description = self.ref.find_element_by_css_selector(
                                    Achivement.sub_description_css_selector)
        actions.release(self.ref).perform()
        actions.move_to_element(self.ref).perform()
        self.progress_icon = self.ref.find_element_by_class_name(Achivement.progress_class_name)
        self.button = self.ref.find_element_by_tag_name(Achivement.button_tag_name)
        #  Get bottom element.
        self.bottom = self.ref.find_element_by_class_name(Achivement.bottom_class_name)
        actions.release(self.ref).perform()

    def get_ref(self):
        '''It returns achivement bloc element.'''
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
        '''Return text money for achivement.'''
        return self.bottom.text

    def get_progress_text(self):
        '''
            Return progress text.

            '1/6' for example.
            It is empty for most achievements.'''
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
        '''Return sub description text'''
        return self.sub_description.text

    def get_button_text(self):
        '''Return button text'''
        return self.button.text

    def is_completed(self):
        '''Return if achivement is completed'''
        return Achivement.class_value_completed in self.class_value
