from jira import JIRA
from jira.exceptions import JIRAError
import requests, os, yaml, time

class jira():

    def __init__(self):
        pass

    def auth(self):
        PWD = os.getenv("HOME")
  
        with open("%s/.python_auth_cfg.yml" % PWD, 'r') as auth:

            auth_conf = yaml.load(auth, Loader=yaml.FullLoader)

        jira_conf            = auth_conf['jira']
        jira_admin_user      = jira_conf['admin_user']
        jira_admin_api_token = jira_conf['admin_api_token']
        jira_basic_url       = jira_conf['jira_basic_url']
        
        self.jira_basic_url  = jira_basic_url 
        self.jira_options    = {
                                   'server'        : jira_basic_url,
                                   'max_retries'   : 1
                               } 
        try:
            self._session = JIRA(self.jira_options, basic_auth=(jira_admin_user, jira_admin_api_token))

        except JIRAError and TypeError and KeyError as error:
            print('jira.init.auth <%s>' % error)
            
        return self._session

    def user_invite(self, email):

        self.USERNAME = email.split('@')[0]
       
        try:
            self._session.add_user(self.USERNAME, email, active=True)
        
        except JIRAError as error:
            print('jira.init.user_invite <%s>' % error.text)
   
    def user_delete(self, username):

        try:
            DELETE_USER = self._session.delete_user(username)

        except JIRAError as error:
            print('jira.init.user_delete <%s>' % error.text)

    def user_blocked(self, username):
        DEACTIVATE_USER = self._session.deactivate_user(username)

        try:
            DELETE_USER = self._session.deactivate_user(username)

        except JIRAError and TypeError and KeyError as error:
            print('jira_api_user.init.user_blocked <%s>' % error)

    def user_add_group(self, groupName):

        time.sleep(15)
        with open("config/jira_group_access.yml", 'r') as jira_group_access:
            jira_group_access = yaml.load(jira_group_access, Loader=yaml.FullLoader)

        try:
            group_list = jira_group_access[groupName]

            for group in group_list:
                
                try:
                    self._session.add_user_to_group(self.USERNAME , group)

                except JIRAError and TypeError and KeyError as error:
                    print('jira_api_user.init.user_add_group <%s>' % error)

        except KeyError as error:
            print('init.user_add_group | add default group | Error < groupName: %s is not defined >' % groupName)

        
          