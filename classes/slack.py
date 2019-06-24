import os, yaml, requests

class slack(object):
    
    PWD = os.getenv("HOME")

    def __init__(self):
        pass   

    def defaultOptions(self):

        try:
            with open("%s/.python_auth_cfg.yml" % slack.PWD, 'r') as auth:
                auth_conf = yaml.load(auth, Loader=yaml.FullLoader)

            auth_data = auth_conf['slack']

            self.token      =  auth_data['api_token']
            self.namespace  =  auth_data['name_space']
            self.api_url    = 'https://%s.slack.com/api' % self.namespace

            self.command    = {
                                'user_list'     : '%s/users.list' % self.api_url,
                                'user_inactive' : '%s/users.admin.setInactive' % self.api_url,
                                'users_invite'  : '%s/users.admin.invite' % self.api_url
                            }
        except KeyError as error:
            print('slack.init | Error <%s>' % error )

        return self.command

    class users(object):

        def __init__(self):
            self._slack     = slack()
            self._options   = self._slack.defaultOptions()
            self._token     = self._slack.token
  
        def search(self, **username):

            data_accounts  = {
                              'token'     : self._token
                              }

            r  = requests.post(self._options['user_list'], data = data_accounts)

            if r.status_code == 200:
                members = r.json().get('members')
        
                for user_data in members:
                    email = user_data.get('profile').get('email')

                    if email != None :
                        user_name   = email.split('@')[0]
                        status      = user_data.get('deleted')

                        if user_name == username['username'] :
                            self.user_id = user_data.get('id')
                            print(self.user_id, user_name)
                            return self.user_id
                        else:
                            pass
                    else:
                        pass
            else:
                print('slack.init.users.search | Error <%s>' % r.status_code)
    
        def inactive(self, user_id):
   
            data_account_inactive   =   {
                                        'token' : self._token,
                                        'user'  : user_id
                                        }
            print(data_account_inactive)
            r = requests.post(self._options['user_inactive'], data=data_account_inactive)
            print('slack.init.user_inactive |','| {}'.format(r.json()))

        def invite(self, **data_account):
            
            data_account_create = {
                                'email'     : data_account['email'],
                                'first_name': data_account['first_name'],
                                'last_name' : data_account['last_name'],
                                'token'     : self._token,
                                'set_active': "true",
                                'resend'    : "true"
                                }
            print(data_account_create)
            r = requests.post(self._options['users_invite'], data = data_account_create)
            print('slack.init | <%s | %s>' % (r.status_code, r.json()))
