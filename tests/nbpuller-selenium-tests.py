#!/usr/bin/python3

""" Selenium Tests for nbpuller extension for Jupyter Notebooks"""
import unittest
import time
import os
import constants
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class JupyterPullerTesting(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.bmail = os.environ['BMAIL']
        self.user = os.environ['USER']
        self.password = os.environ['PASSWORD']

    def test_routing(self):
        """ Tests to ensure that a user can reach the nbpuller route """
        driver = self.driver
        self.loginToJupyterNotebook(driver)
        self.startJupyterNotebookServer(driver)

        nbpuller_link = "{}{}{}".format(constants.DATAHUB_DEV_URL, \
            constants.JPY_USER_ROUTE,
            constants.NBPULLER_ROUTE)
        driver.get(nbpuller_link)

        self.assertIn(constants.MALFORMED_LINK_MESSAGE, driver.page_source)


    def test_all_pulls(self):
        driver = self.driver
        self.loginToJupyterNotebook(driver)
        self.startJupyterNotebookServer(driver)

        self.pullUsingParams(driver, constants.TEST_1_PARAMS,\
         constants.TEST_1_FILES, constants.TEST_1_REDIRECT_PATH)

    def pullUsingParams(self, driver, params, expectedFiles, expectedRedirectPath):
        """ Tests to ensure that once a user is authenticated into Google Drive CLI,
        he or she can also log their account out and revoke rights """
        driver = self.driver
        nbpuller_link = "{}{}{}?{}".format(constants.DATAHUB_DEV_URL, \
            constants.JPY_USER_ROUTE,
            constants.NBPULLER_ROUTE, params)
        print("\n" + nbpuller_link)
        driver.get(nbpuller_link)

        WebDriverWait(driver, constants.START_SERVER_WAIT_PERIOD).until( \
            EC.presence_of_element_located((By.XPATH, "//div[@class='list_item row']")))

        for file in expectedFiles:
            self.assertIn(file, driver.page_source)

        expectedLink = "{}{}{}".format(\
            constants.DATAHUB_DEV_URL,
            constants.JPY_USER_ROUTE,
            expectedRedirectPath)

        print("\n" + driver.current_url)
        print("\n" + expectedRedirectPath)
        self.assertEqual(driver.current_url, expectedLink)

    def startJupyterNotebookServer(self, driver):
        driver.find_element_by_xpath("//a[@id='start']").click()

        WebDriverWait(driver, constants.START_SERVER_WAIT_PERIOD).until( \
            EC.title_contains(constants.NOTEBOOK_PAGE_TITLE))

    def loginToJupyterNotebook(self, driver):
        """ From the initial Google login landing page, navigates and signs in
        using valid Berkeley credentials discerned from environment variables """
        driver.get(constants.DATAHUB_DEV_URL)

        # Verify Google
        driver.find_element_by_xpath("//input[@id='Email']").send_keys(self.bmail)
        driver.find_element_by_xpath("//input[@id='next']").click()

        # Verify CalNet
        WebDriverWait(driver, constants.DEFAULT_WAIT_PERIOD).until( \
            EC.title_contains(constants.CALNET_PAGE_TITLE))
        self.assertIn(constants.CALNET_PAGE_TITLE, driver.title)

        # Sign In via CalNet
        driver.find_element_by_xpath("//input[@id='username']").send_keys(self.user)
        driver.find_element_by_xpath("//input[@id='password']").send_keys(self.password)
        driver.find_element_by_xpath("//input[@class='button']").click()

        # Verify Login took us to correct location
        WebDriverWait(driver, constants.DEFAULT_WAIT_PERIOD).until( \
            EC.title_contains(constants.SERVER_PAGE_TITLE))
        self.assertIn(constants.SERVER_PAGE_TITLE, driver.title)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
