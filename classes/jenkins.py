from selenium import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by   import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time, copy, yaml, os

class selenium():
    DEFAULT_OPTIONS = {
                        'capabilities' : {
                                            "browserName" : "chrome",
                                            "version"     : "latest",
                                            "enableVNC"   :  False,
                                            "enableVideo" :  False
                                         }
                        }
    PWD = os.getenv("HOME")

    def __init__(self):
        self._options = copy.copy(selenium.DEFAULT_OPTIONS)

        with open("%s/.python_auth_cfg.yml" % selenium.PWD, 'r') as auth:

            auth_conf = yaml.load(auth, Loader=yaml.FullLoader)

        try:
            data_selenoid                   = auth_conf['selenoid_remote']
            selenoid_remote_user            = data_selenoid['username']
            selenoid_remote_user_password   = data_selenoid['password']
            selenoid_basic_url              = data_selenoid['basic_url']

            try:
                url_type            = 'https'
                selenoid_basic_url  =  selenoid_basic_url.split('%s://' % url_type)[1]

            except IndexError as error:
                print('<Your connection is not security>')
                url_type            = 'http'
                selenoid_basic_url  =  selenoid_basic_url.split('%s://' % url_type)[1]

            self.driver = webdriver.Remote("%s://%s:%s@%s:4444/wd/hub" % (url_type,
                                                                          selenoid_remote_user, 
                                                                          selenoid_remote_user_password,
                                                                          selenoid_basic_url), self._options['capabilities'])
        except KeyError as error:
            print("INTI Local browser, becouse i can't handle the dict(key = %s)" % error)
            self.driver = webdriver.Firefox()
            

        try:
            data_jenkins            = auth_conf['jenkins']
            admin_user              = data_jenkins['admin_user']
            admin_password          = data_jenkins['admin_password']
            self.jenkins_basic_url  = data_jenkins['jenkins_url']

            self.driver.get(self.jenkins_basic_url)

            self.driver.find_element_by_name("j_username").send_keys(admin_user)
            self.driver.find_element_by_name("j_password").send_keys(admin_password)
            self.driver.find_element_by_name("Submit").send_keys(Keys.RETURN)
            time.sleep(2)
            # timeuot from full download next page

        except KeyError as error:
            print("Sorry, but I can't handle the dict(key = %s)" % error)

    def user_create(self, **data_account):

        with open("config/jenkins_group_access.yml", 'r') as jenkins_group_access:
            jenkins_build_access_conf = yaml.load(jenkins_group_access, Loader=yaml.FullLoader)

        username    = data_account['username']
        password    = data_account['password']
        first_name  = data_account['first_name']
        last_name   = data_account['last_name']
        groupPolicy = jenkins_build_access_conf[data_account['groupPolicy']]

        

        self.driver.get("%s/securityRealm" % self.jenkins_basic_url)

        try:
            self.driver.find_element_by_link_text('%s' % username)

        except:
            self.driver.find_element_by_link_text('Create User').click()

            self.driver.find_element_by_name("username").send_keys("%s" % username)
            self.driver.find_element_by_name("password1").send_keys("%s" % password)
            self.driver.find_element_by_name("password2").send_keys("%s" % password)
            self.driver.find_element_by_name("fullname").send_keys("%s %s" % (first_name, last_name))
            self.driver.find_element_by_name("email").send_keys("%s@moysklad.ru" % username)

            self.driver.find_element_by_xpath("//button[@id='yui-gen3-button']").send_keys(Keys.RETURN)

            time.sleep(2)

            self.driver.get("%s/role-strategy/assign-roles" % self.jenkins_basic_url)

            self.driver.find_element_by_xpath("//tr[@nameref='rowSetStart3']/td/input[@name='_.']").send_keys("%s" % username)
            self.driver.find_element_by_xpath("//tr[@nameref='rowSetStart3']/td/span/span/button[@type='button']").click()
            self.driver.find_element_by_xpath("//tr[@nameref='rowSetStart2']/td/input[@name='_.']").send_keys("%s" % username)
            self.driver.find_element_by_xpath("//tr[@nameref='rowSetStart2']/td/span/span/button[@type='button']").click()

            self.driver.find_element_by_xpath("//tr[@name='[%s]']/td/input[@name='[dev]']" % username).click()
            time.sleep(2)

            for build_name in groupPolicy:
                self.driver.find_element_by_xpath("//tr[@name='[%s]']/td/input[@name='[%s]']" % (username, build_name)).click()
            
            self.driver.find_element_by_name("Apply").click()
            time.sleep(2)
            self.driver.find_element_by_name("Submit").click()
    
    def user_delete(self, username):

        try:
            self.driver.get("%s/securityRealm" % self.jenkins_basic_url)

            self.driver.find_element_by_link_text('%s' % username)
            self.driver.find_element_by_xpath("//a[@href='user/%s/delete']" % username ).click()
            time.sleep(1)

            self.driver.find_element_by_xpath("//button[@id='yui-gen3-button']").click()
            self.driver.get("%s/role-strategy/assign-roles" % self.jenkins_basic_url)

            time.sleep(2)
            self.driver.find_element_by_xpath("//table[@id='globalRoles']/tbody/tr[@name='[%s]']/td[@class='start']/a/img[@alt='remove']" % username).click()
            self.driver.find_element_by_xpath("//table[@id='projectRoles']/tbody/tr[@name='[%s]']/td[@class='start']/a/img[@alt='remove']" % username).click()

            self.driver.find_element_by_name("Apply").click()
            time.sleep(2)
            self.driver.find_element_by_name("Submit").click()

        except:
            pass

    def browser_close(self):
    
        self.driver.close()