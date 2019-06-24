import random, string, gitlab
from gitlab import exceptions , GitlabCreateError
class gitlab_api():

    def __init__(self):
        pass

    def auth(self):
        self.gitlab_api = gitlab.Gitlab.from_config()

    def user_create(self, **data_account):

        try:
            USER    = self.gitlab_api.users.list(search = '%s' % data_account['username'])[0]

        except :    
            try:  
                CREATE_USER = self.gitlab_api.users.create({'email'            : '%s'    %  data_account['email'],
                                                            'password'         : '%s'    %  data_account['password'],
                                                            'username'         : '%s'    %  data_account['username'],
                                                            'name'             : '%s %s' % (data_account['first_name'], 
                                                                                            data_account['last_name']),
                                                            'skip_confirmation': True
                                                            })
            except GitlabCreateError as error:
                print('gitlab_api_users.init.blocked_user | Error <%s>' % error)
                
    def user_delete(self, username):

        try:
            user  = self.gitlab_api.users.list(username = username)[1]
            user.delete()

        except IndexError or GitlabCreateError as error:
            print('gitlab_api_users.init.user_delete | Error <%s>' % error)

    def user_deactivate(self, username):

        try:
            USER  = self.gitlab_api.users.list(username = username)[0]
            USER.block()

        except IndexError or GitlabCreateError as error:
            print('gitlab_api_users.init.user_delete | Error <%s>' % error )