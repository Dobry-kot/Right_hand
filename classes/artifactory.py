import requests, json, copy, os, yaml

class artifactory():
    DEFAULTS_OPTIONS = { 
                         'headers' :  {
                                        'Content-Type' : 'application/json;charset=UTF-8'
                                       }
                         }   
    PWD = os.getenv("HOME")

    def __init__(self):
        self._options   = copy.copy(artifactory.DEFAULTS_OPTIONS)
        self._pwd       = artifactory.PWD

    def auth(self):
  
        with open("%s/.python_auth_cfg.yml" % self._pwd, 'r') as auth:

            auth_conf = yaml.load(auth, Loader=yaml.FullLoader)

        artifactory_conf            = auth_conf['artifactory']
        artifactory_admin_user      = artifactory_conf['admin_user']
        artifactory_admin_password  = artifactory_conf['admin_password']
        artifactory_basic_url       = artifactory_conf['artifactory_url']

        self._session   = requests.session()
        self.url        = artifactory_basic_url
        auth_url        = self.url + '/artifactory/ui/auth/login'
   
        self._options['headers']['Content-Type'] = 'application/json'

        try:
            payload = {
                        "user"      :"%s" % artifactory_admin_user,
                        "password"  :"%s" % artifactory_admin_password,
                        "type"      :"login"
                        }
       
        except KeyError as error:
            pass
                    
        auth = self._session.post(auth_url, 
                                  headers = self._options['headers'], 
                                  data    = json.dumps(payload)) 

        if auth.status_code == 200:
            return True

        else:
            print(auth.json())

    def user_delete(self, *usernames):
        
        user_delete_url = self.url + '/artifactory/ui/users/userDelete'

        self._options['headers']['Content-Type'] = 'application/json;charset=UTF-8'
        
        try:
            
            payload = {
                    "userNames": usernames[0]
                    }

            user_delete = self._session.post(user_delete_url, 
                                             headers = self._options['headers'], 
                                             data    = json.dumps(payload))
            print(user_delete.json())
            
        except KeyError and TypeError as error:
            print('Error:artifactory.user_delete <%s>' % error) 

    def user_create(self, **account_data):

        user_create_url = self.url + '/artifactory/ui/users'

        with open("config/user_group_policy.yml", 'r') as groupPolicy:
            group_policy_conf = yaml.load(groupPolicy, Loader=yaml.FullLoader)

     
        try:
            payload  = {"profileUpdatable"  : "true",
                        "name"              : "%s" % account_data['username'],
                        "email"             : "%s" % account_data['email'],
                        "password"          : "%s" % account_data['password'],
                        "retypePassword"    : "%s" % account_data['password'],
                        }
            groupNames = list() 

            try:
                user_group_policy = group_policy_conf[account_data['groupPolicy']]

                for groupName in user_group_policy:
                    groupNames.append({"groupName" : "%s" % groupName, "realm" : "artifactory" } )

                payload['userGroups'] = groupNames

            except KeyError as error:
                print('init.user_create | Error <groupPolicy: %s is not defined>' % error)
     
        except KeyError and TypeError as error:
            print(error)

        user_create = self._session.post(user_create_url,
                                         headers    =self._options['headers'], 
                                         data       =json.dumps(payload)) 

        if user_create.status_code == 200:
            return True
        
        else:
            print(user_create.json())
