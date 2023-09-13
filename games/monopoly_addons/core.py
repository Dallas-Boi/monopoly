# Created 1-17-23 Tuesday
# This file is the core to monopoly. If this file is missing then monopoly will not work
import requests
import json
# Opens the property data File
with open('gameData/propertyDetails.json', 'r') as pd:
    propData = json.load(pd)

# This makes a players data
class Players:
    # Declears variables
    player_name = ""
    player_color = ""
    player_spot = 1
    player_cash = 2000
    player_skipTurn = 0
    player_jailed = False
    player_properties = {}
    player_inventory = {}
    player_ooj = []

    # Player loans
    player_hasLoan = False
    player_loanAmount = 0
    player_loan_payIn = 0

    # This will make the player
    def __init__(self, name, color, spot, cash, skipTurn, jailed, props, inv, ooj, hasLoan, loanAmount, payIn):
        self.player_name = name
        self.player_color = color
        self.player_spot = spot
        self.player_cash = cash
        self.player_skipTurn = skipTurn
        self.player_jailed = jailed
        self.player_properties = props
        self.player_inventory = inv
        self.player_ooj = ooj

        # Player loans
        self.player_hasLoan = hasLoan
        self.player_loanAmount = loanAmount
        self.player_loan_payIn = payIn
    
    # Returns the player name
    def get_player_name(self):
        return self.player_name

    # This returns the players color
    def get_player_color(self):
        return self.player_color

    # Returns "player_spot":
    def get_player_spot(self):
        return self.player_spot

    # Sets "player_spot"
    def set_player_spot(self, new):
        self.player_spot = new

    # Adds to "player_spot"
    def add_player_spot(self, new):
        self.player_spot += new

    # Returns "player_properties"
    def get_player_properties(self):
        return self.player_properties

    # Adds to "player_properties"
    def add_player_properties(self, new):
        self.player_properties[new] = {'name': propData[new]['name'],'house': 0, 'mortgage': False, 'nextHouse': True, 'removeHouse': True}

    # Removes from "player_properties"
    def take_player_properties(self, new):
        del self.player_properties[new]

    # Sets the property "nextHouse"
    def set_player_property_nextHouse(self, spot, value):
        self.player_properties[spot]['nextHouse'] = value

    # Sets the property "removeHouse"
    def set_player_property_removeHouse(self, spot, value):
        self.player_properties[spot]['removeHouse'] = value
    
    # Sets the property "nextHouse"
    def set_player_property_mortgage(self, spot, value):
        self.player_properties[spot]['mortgage'] = value

    # Adds a House to the players property
    def add_player_property_house(self, spot):
        self.player_properties[spot]['house'] += 1
    
    # Removes a House to the players property
    def take_player_property_house(self, spot):
        self.player_properties[spot]['house'] -= 1

    # Adds to the players Cash
    def add_player_cash(self, amount):
        self.player_cash += amount

    # Substracts from the players Cash
    def take_player_cash(self, amount):
        self.player_cash -= amount

    # Sets the players Cash
    def set_player_cash(self, amount):
        self.player_cash = amount

    # Returns the players Cash
    def get_player_cash(self):
        return self.player_cash
    
    # Returns "player_skipTurn"
    def get_player_skipTurn(self):
        return self.player_skipTurn

    # Sets "player_skipTurn"
    def set_player_skipTurn(self, set):
        self.player_skipTurn = set
    
    # Adds to "player_skipTurn"
    def add_player_skipTurn(self, add):
        self.player_skipTurn += add;
    
    # Removes from "player_skipTurn"
    def take_player_skipTurn(self, take):
        self.player_skipTurn -= take;

    # Returns the players jail status
    def get_player_jail(self):
        return self.player_jailed

    # Sets the players jail status
    def set_player_jail(self, status):
        self.player_jailed = status
    
    # Returns "player_inventory"
    def get_player_inventory(self):
        return self.player_inventory

    # Adds to "player_inventory"
    def add_player_inventory(self, new):
        self.player_inventory[new] = 0
    
    # Takes from "player_inventory"
    def take_player_inventory(self, new):
        del self.player_inventory[new]

    # Adds to "player_ooj"
    def add_player_ooj(self, card):
        self.player_ooj.append(card)
    
    # Removes from "player_ooj"
    def remove_player_ooj(self):
        self.player_ooj.remove(self.get_player_ooj()[0])

    # Returns "player_ooj"
    def get_player_ooj(self):
        return self.player_ooj

    # Player Loans
    # Returns "player_hasLoan" 
    def get_player_hasLoan(self):
        return self.player_hasLoan
    # Sets "player_hasLoan"

    def set_player_hasLoan(self, new):
        self.player_hasLoan = new

    # Returns "player_loanAmount"
    def get_player_loanAmount(self):
        return self.player_loanAmount
    
    # Sets "player_loanAmount"
    def set_player_loanAmount(self, new):
        self.player_loanAmount = new

    # Returns "player_loan_payIn"
    def get_player_loan_payIn(self):
        return self.player_loan_payIn
    
    # Sets "player_loan_payIn"
    def set_player_loan_payIn(self, new):
        self.player_loan_payIn = new
    
    # Adds to "player_loan_payIn"
    def add_player_loan_payIn(self, new):
        self.player_loan_payIn += new
    
    # Substracts from "player_loan_payIn"
    def take_player_loan_payIn(self, new):
        self.player_loan_payIn -= new

# This handles the property Data
class grid_spot:
    spot_id = 0
    spot_name = ""
    color = ""
    x = 0
    y = 0
    # Constructor
    def __init__(self, sid, name, color, x, y):
        self.spot_id = sid
        self.spot_name = name
        self.color = color
        self.x = x
        self.y = y
    
    # Returns the spot_id
    def get_spot_id(self):
        return self.spot_id
    # Returns the spot_name
    def get_spot_name(self):
        return self.spot_name
    # Returns the color
    def get_spot_color(self):
        return self.color
    # Returns the Spot x
    def get_spot_x(self):
        return self.x
    # Returns the spot y
    def get_spot_y(self):
        return self.y

# Made 1-6-23 Friday
# This is the class for making sure money Exploits are taken care of
class check_for_exploit:
    before_money = 0
    before_spot = 0
    enable_anti_cheat = True

    # Constructor
    def __init__(self, before, spot):
        self.before_money = before
        self.before_spot = spot

    # Updates the "before_money" variable
    def update_before_money(self, new):
        self.before_money = new

    # Adds the loan the player got to the before money
    def add_real_money(self, amount):
        self.before_money += amount

    # This checks the new money amount compared to the started money amount
    def check_exploit(self, after):
        if self.enable_anti_cheat == True:
            self.compare = after - self.before_money
            #print(f'before: {self.before_money} | after: {after} | difference {self.compare}')
            # Checks for an increase of money
            if self.compare >= 750:
                return 'EXPLOIT'
            else:
                return 'good'

# This makes saving a game more usable and not have so many characters in the save key
class save_monopoly_V2:
    save_data_ID = ""
    save_game_mode = ""
    save_turn = ""
    save_version = ""

    # Arrays
    save_players = {}
    save_cards = {}
    save_ooj_used = {}
    save_houses = []

    def __init__(self, gameID, game_mode, turn, version, playersDB, cardsDB, ooj, housesDB):
        self.save_data_ID = gameID
        self.save_game_mode = game_mode
        self.save_turn = turn
        self.save_version = version
        self.save_players = playersDB
        self.save_cards = cardsDB
        self.save_ooj = ooj
        self.save_houses = housesDB

    # Loads the given save
    def update_save_game(self, game_mode, turn, playersDB, cardsDB, ooj, housesDB):
        self.save_game_mode = game_mode
        self.save_turn = turn
        self.save_players = playersDB
        self.save_cards = cardsDB
        self.save_ooj = ooj
        self.save_houses = housesDB
    
    # Returns "save_game_mode"
    def get_save_game_mode(self):
        return self.save_game_mode
    
    # Returns "save_players"
    def get_save_players(self):
        return self.save_players
    
    # Returns "save_turn"
    def get_save_turn(self):
        return self.save_turn

    # Returns "save_cards"
    def get_save_cards(self):
        return self.save_cards

    # Returns "save_ooj"
    def get_save_ooj(self):
        return self.save_ooj

    # Returns "save_houses"
    def get_save_houses(self):
        return self.save_houses
    
    # Returns "save_version"
    def get_save_version(self):
        return self.save_version

    # Sends the save data to the Server
    def send_data(self):
        data = {
            "saveID": self.save_data_ID, 
            "game_mode": self.save_game_mode, 
            "turn": self.save_turn,
            "version": self.save_version,
            "cards": self.save_cards,
            "oojUsed": self.save_ooj_used,
            "houses": self.save_houses,
            'players': {}
        }
        # Makes the players
        for key, value in self.save_players.items():
            data['players'][key] = {
                'name': value.get_player_name(),
                'color': value.get_player_color(),
                'spot': value.get_player_spot(),
                'cash': value.get_player_cash(),
                'jailStatus': value.get_player_jail(),
                'inventory': value.get_player_inventory(),
                'prop': value.get_player_properties(),
                'ooj': value.get_player_ooj(),
                'skipTurn': value.get_player_skipTurn(),
                'loans': {
                    'hasLoan': value.get_player_hasLoan(),
                    'loanAmount': value.get_player_loanAmount(),
                    'payIn': value.get_player_loan_payIn()
                }
            }
            
        save = requests.get(url=f'https://easyGO.theweebmonkey.repl.co/save_game?data={data}')
        print(save.text)

# Request the data needed from the server
def load_save(key, version):
    from games.monopoly import load_monopoly_data
    save = requests.get(url=f'https://easyGO.theweebmonkey.repl.co/get_save?key={key}')
    
    data = json.loads(save.text)
    load_monopoly_data(data)

