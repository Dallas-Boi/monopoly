# Made 1-27-23 Friday
# This file handles and Saves current account details

import requests

class account:
    account_id = ''
    account_name = ''

    # Constructor
    def __init__(self, id, name):
        self.account_id = id
        self.account_name = name
    
    # Returns 'account_id"
    def get_account_id(self):
        return self.account_id
    
    # Returns "account_name"
    def get_account_name(self):
        return self.account_name

# When the user signsup
def signUp_handle(name, word):
    global user_account
    sending = requests.post(f'https://easyGO.theweebmonkey.repl.co/account?username={name}&password={word}')

    details = eval(sending.text)
    user_account = account(details['id'], details['name'])
    from games.monopoly_addons import multi_core
