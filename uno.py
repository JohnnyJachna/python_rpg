import random
import time

def get_color(color):
    selected_color = None
    if color == "red":
        selected_color = "\033[0;31m"
    elif color == "yellow":
        selected_color = "\033[1;33m"
    elif color == "green":
        selected_color = "\033[0;32m"
    elif color == "blue": 
        selected_color = "\033[0;34m"
    elif color == "black":
        selected_color = "\033[1;30m"
    else:
        selected_color = "\033[0m"
    return selected_color


class Card:
    def __init__(self, color, type = "None"):
        self.color = color
        self.type = type
    
    #def set_next_player(self, game):
        #game.turn_over()
    
    def get_text_color(self):
        text_color = get_color(self.color)
        return text_color    


class Number(Card):
    def __init__(self, color, number, type = "number"):
        super().__init__(color)
        self.number = number
        self.type = type

    def __str__(self):
        formatted_card = f"{self.get_text_color()}{str(self.number)}\033[0m"
        #str(self.color) + " " + str(self.number)
        return formatted_card


class Draw(Card):
    def __init__(self, color, type = "draw"):
        super().__init__(color)
        self.type = type

    def __str__(self):
        formatted_card = f"{self.get_text_color()}+2\033[0m"
        #str(self.color) + " draw"
        return formatted_card
    
    def next_player_draw(self, game):
        #print("\nNEXT PLAYER DRAW 2\n")
        drawing = 2
        next_player = game.turn_order[1]
        while drawing > 0:
            game.draw_from_deck(next_player)
            #print(f"{next_player.name} drew {next_player.hand[len(next_player.hand) - 1]}")
            drawing -= 1
        print(f"{next_player.name} drawing two cards\n")
        time.sleep(3)
        #self.set_next_player(game)
        game.turn_over()


class Reverse(Card):
    def __init__(self, color, type = "reverse"):
        super().__init__(color)
        self.type = type

    def __str__(self):
        formatted_card = f"{self.get_text_color()}reverse\033[0m"
        #str(self.color) + " reverse"
        return formatted_card

    def reverse_turn_order(self, game):
        #print("REVERSE REVERSE")
        game.turn_order.reverse()


class Skip(Card):
    def __init__(self, color, type = "skip"):
        super().__init__(color)
        self.type = type

    def __str__(self):
        formatted_card = f"{self.get_text_color()}skip\033[0m"
        #str(self.color) + " skip"
        return formatted_card

    def skip_turn(self, game):
        #print("SKIP")
        #self.set_next_player(game)
        #self.set_next_player(game)
        game.turn_over()
        game.turn_over()


class Wild(Card):
    def __init__(self, color = "black", type = "wild"):
        self.color = color
        self.type = type
    
    def __str__(self):
        formatted_card = f"{self.get_text_color()}wild\033[0m"
        #str(self.color) + " wild"
        return  formatted_card
    
    def set_color(self, color, game):
        self.color = color
        #self.set_next_player(game)
        game.turn_over()


class WildDraw(Card):
    def __init__(self, color = "black", type = "wild_draw"):
        self.color = color
        self.type = type

    def __str__(self):
        formatted_card = f"{self.get_text_color()}+4\033[0m"
        #str(self.color) + " draw wild"
        return formatted_card
    
    def set_color(self, color, game):
        self.color = color
        self.next_player_draw(game)

    def next_player_draw(self, game):
        #print("\nNEXT PLAYER DRAW 4\n")
        drawing = 4
        next_player = game.turn_order[1]
        while drawing > 0:
            game.draw_from_deck(next_player)
            #print(f"{next_player.name} drew {next_player.hand[len(next_player.hand) - 1]}")
            drawing -= 1
        print(f"{next_player.name} drawing four cards\n")
        time.sleep(3)
        #self.set_next_player(game)
        game.turn_over()


class Game:
    def __init__(self, deck = [], players = [], turn_num = 0, pile = []):
        self.deck = deck
        self.players = players
        self.turn_order = players
        self.turn_num = turn_num
        self.pile = pile

    def create_start_deck(self):
        self.deck.populate_deck()
        self.deck.shuffle_deck()

    def draw_from_deck(self, player):
        if len(self.deck.deck) > 0:
            player.add_to_hand(self.deck.remove_card())
        else:
            print("reshuffle")
            print(self.deck)
            self.pile = self.deck.pile_to_deck(self.pile)
            print(self.deck)
    
    def place_on_pile(self, card, player):
        self.pile.insert(0, card)
        if card.type == "draw":
            card.next_player_draw(self)
        elif card.type == "skip":
            card.skip_turn(self)
        elif card.type == "reverse":
            card.reverse_turn_order(self)
        elif card.type == "wild" or card.type == "wild_draw":
            chosen_color = player.choose_color()
            #print(f"\nChosen color: {chosen_color}\n")
            card.set_color(chosen_color, self)
        else:
            #card.set_next_player(self)
            self.turn_over()
        self.turn_num += 1

    def print_pile(self):        
        if len(self.pile) > 0:
            print(f"Pile: {self.pile[0]}\n")
        else:
            print("Pile empty\n")

    def get_start_hand(self):
        START_NUM_CARDS = 7
        for player in self.players:
            index = 0
            while index < START_NUM_CARDS: 
                self.draw_from_deck(player)
                index += 1
    
    def is_card_playable(self, played_card):
        is_playable = False       
        if self.turn_num > 0:
            top_card = self.pile[0] 
            if played_card.color == top_card.color: #Color
                is_playable = True
            elif played_card.type == top_card.type: #Type
                is_playable = True
                if played_card.type == "number": #Numbers
                    if played_card.number == top_card.number: 
                        is_playable = True
                    else:
                        is_playable = False
            elif played_card.color == "black": #Wild
                is_playable = True
        else: 
            is_playable = True #First turn
        return is_playable
    
    def get_current_player(self):
        current_player = self.turn_order[0]
        return current_player
    
    def turn_over(self):
        current_player = self.turn_order[0] #Save current player
        self.turn_order.pop(0) #Remove current player from front of list
        self.turn_order.append(current_player) #Add current player to end of list
    
    def check_win(self, player):
        is_winner = False
        if len(player.hand) == 0:
            print(f"{player.name} wins!")
            is_winner = True
        return is_winner


class Deck:
    def __init__(self, deck = []):
        self.deck = deck
    
    def __str__(self):
        formatted_deck = ', '.join(map(str, self.deck))
        return formatted_deck

    def populate_deck(self):
        colors = ["red", "yellow", "green", "blue"]
        
        def add_number_cards(color):
            index = 0
            number_added = 0            
            while index < 2:
                number_added = 0
                while number_added < 10:
                    self.deck.append(Number(color, number_added))
                    number_added += 1
                index += 1
        
        def add_special_cards():
            index = 0
            color_index = 0
            
            while index < 2:
                color_index = 0
                while color_index < 4:
                    self.deck.append(Draw(colors[color_index]))
                    self.deck.append(Reverse(colors[color_index]))
                    self.deck.append(Skip(colors[color_index]))
                    color_index += 1
                index += 1

        def add_wilds():
            index = 0
            while index < 4:
                self.deck.append(Wild())
                index += 1

            index = 0
            while index < 4:
                self.deck.append(WildDraw())
                index += 1
        
        #Add number cards to deck
        for card_colors in colors:
            add_number_cards(card_colors)
        #Add skips, reverses, and draw (+2) cards to deck
        add_special_cards()
        #Add wilds and wild draws (+4) to deck
        add_wilds()            
        
        return self.deck

    def shuffle_deck(self):
        # Deck must be populated first!
        random.shuffle(self.deck)
        return self.deck

    def remove_card(self):
        drawn_card = self.deck[0]
        self.deck.pop(0)
        return drawn_card
    
    def pile_to_deck(self, pile):
        top_card = pile[0]
        for card in pile:
            if card.type == "wild" or card.type == "wild_draw":
                card.color = "black"
            self.deck.append(card)
            pile.remove(card)
        self.deck.pop(0)
        pile.append(top_card)
        return pile


class Player:
    def __init__(self, name, hand):
        self.hand = hand
        self.name = name
    
    def __str__(self):
        return str(self.name)

    def show_hand(self):
        formatted_hand = ', '.join(map(str, self.hand))
        print(f"{self.name} hand: {formatted_hand}\n")
    
    def add_to_hand(self, card):
        self.hand.append(card)

    def place_card(self, card):
        placed_card = card
        self.hand.remove(card)
        return placed_card
    
    def has_playable_hand(self, game):
        playable_hand = False
        if len(self.get_playable_hand()) > 0:
            playable_hand = True
        return playable_hand
    
    def get_playable_hand(self):
        #self.show_hand()
        playable_hand = []
        for card in self.hand:
            if game.is_card_playable(card):
                playable_hand.append(card)
        return playable_hand

    def player_turn(self, game):
        game.print_pile()
        #self.show_hand()
        print(f"{self.name} selecting card.\n")
        time.sleep(2)
        selecting = True
        while selecting: 
            if self.has_playable_hand(game):                
                if self.has_uno(): #Uno
                    test = random.random()
                    #print(f"random num = {test}")
                    if test < .1: # 10% sChance for not calling uno
                        print(f"{self.name} forgot to call uno!")
                        game.draw_from_deck(self)
                        game.draw_from_deck(self)
                        print(f"{self.name} drew two cards\n")
                        #self.show_hand()
                        game.turn_over()
                        break
                
                playable_hand = self.get_playable_hand()
                random_playable_card_index = random.randint(0, (len(playable_hand) - 1))
                #print(random_playable_card_index)
                selection = playable_hand[random_playable_card_index]            
                print(f"{self.name} placed {selection}\n")
                game.place_on_pile(self.place_card(selection), self)
                selecting = False
            else:
                print(f"{self.name} didn't have a playable card")
                time.sleep(2)
                print(f"\n{self.name} drew a card\n")
                game.draw_from_deck(self)
                #print(f"{self.name} drew a {self.hand[len(self.hand) - 1]}")
                if not game.is_card_playable(self.hand[len(self.hand) - 1]): #if picked up card is not playable, move to next turn
                    selecting = False
                    game.turn_over()
        
        return self.check_for_win(game)
    
    def choose_color(self):
        colors_list = []
        color_num_list = []

        for card in self.hand:
            colors_list.append(card.color)
        
        #print(f"Colors list: {colors_list}")
        red_num = colors_list.count("red")
        yellow_num = colors_list.count("yellow")
        green_num = colors_list.count("green")
        blue_num = colors_list.count("blue")
        
        color_num_list = [red_num, yellow_num, green_num, blue_num]
        #print(f"Color num list: {color_num_list}")
        
        most_color = max(color_num_list)
        color_num_selection = color_num_list.index(most_color)
        
        if color_num_selection == 0:
            color_selection = "red"
        elif color_num_selection == 1:
            color_selection = "yellow"
        elif color_num_selection == 2:
            color_selection = "green"
        else:
            color_selection = "blue"

        #print(f"Color selection: {color_selection}")
        return color_selection
    
    def has_uno(self):
        uno = False
        #print("checking uno")
        if len(self.hand) == 2: #when player has two cards and check before about to place 2nd to last
            uno = True
            #print("uno true")
        return uno

    def check_for_win(self, game):
        is_winner = game.check_win(self)
        return is_winner

class User(Player):
    def __init__(self, name, hand):
        super().__init__(name, hand)
    
    def player_turn(self, game):
        print(f"{self.name}'s turn!\n")
        self.show_hand()
        time.sleep(1)
        def card_prompt():
            game.print_pile()
            print("Select a card to place\n")
            index = 0
            while index < len(self.hand):
                if game.is_card_playable(self.hand[index]):                        
                    print(f"\033[1m{str(index + 1)}.\033[0m {str(self.hand[index])}")
                else:
                    print(f"\033[2m{str(index + 1)}.\033[0m {str(self.hand[index])}")
                index += 1
            print()

        def select_card():
            looping = True
            #called_uno = False
            #playable_hand = self.get_playable_hand()
            selected_card = None
            user_selection = None
            
            while looping:
                try:
                    user_selection = int(input(">")) - 1
                    print()
                except: 
                    print("\nPlease select a whole number.\n")
                else: 
                    if user_selection < len(self.hand) and user_selection > -1:
                        if game.is_card_playable(self.hand[user_selection]):
                            looping = False
                        else:
                            print("Please select a playable card\n")
                    else:   
                        print("Please select an available card\n")
            selected_card = self.hand[user_selection]
            return selected_card

        selecting = True

        while selecting:
            if self.has_playable_hand(game):
                
                if self.has_uno():
                    card_prompt()
                    uno_input = input(">")
                    if uno_input != "u":
                        print("\nYou didn't say uno!\n")
                        game.draw_from_deck(self)
                        print(f"{self.hand[len(self.hand) - 1]} drawn from deck.")
                        game.draw_from_deck(self)
                        print(f"{self.hand[len(self.hand) - 1]} drawn from deck.\n")
                    else: 
                        print("\nUno!\n")
                
                card_prompt()
                selected_card = select_card()
                game.place_on_pile(self.place_card(selected_card), self)
                selecting = False
            else:
                #game.draw_from_deck(self)
                #print(f"No playable cards, {self.hand[len(self.hand) - 1]} drawn from deck.\n")
                print(f"No playable cards\n")
                drawing = True
                while drawing:
                    print("Press 1 to draw a card\n")
                    user_input = input(">")
                    if user_input == "1":
                        game.draw_from_deck(self)
                        print(f"\n{self.hand[len(self.hand) - 1]} drawn from deck.\n")
                        drawing = False
                if not game.is_card_playable(self.hand[len(self.hand) - 1]): #if picked up card is not playable, move to next turn
                    game.turn_over()
                    selecting = False
        
        return self.check_for_win(game)
        

    def choose_color(self):
        selecting = True
        color = "None"
        while selecting:
            try:
                #print("\nChoose a color:\n1. Red\n2. Yellow\n3. Green\n4. Blue")
                print("Choose a color:")
                def prompt_color(color, num):                    
                    print(f"{get_color(color)}{num}. {color}{get_color("end")}")
                prompt_color("red", "1")
                prompt_color("yellow", "2")
                prompt_color("green", "3")
                prompt_color("blue", "4")
                print()
                color_selection = int(input(">"))
                print()
            except:
                print("\nPlease select a whole number.\n")
            else:
                if color_selection < 1 or color_selection > 4:
                    print("\nPlease select a number between 1 and 4.\n")
                else:
                    selecting = False
        
        if color_selection == 1:
            color = "red"
        elif color_selection == 2:
            color = "yellow"
        elif color_selection == 3:
            color = "green"
        else:
            color = "blue"
        
        return color

player_one = User("Johnny", [])
player_two = User("Student", [])
player_three = Player("Sean", [])
player_four = Player("BillyBob", [])
game_deck = Deck()
game = Game(game_deck, [player_one, player_two, player_three, player_four])

playing= True

game.create_start_deck()
game.get_start_hand()

print("Instructions:\n")
print("-Normal Uno rules")
print("-When you have two cards left, press 'u' then 'enter' to call uno")
print("-You draw two cards if you don't press 'u' correctly")
print("-The game will not prompt for you to press 'u' when you should, so don't forget!")
print("-The computer has a 10% not to call uno when it should and will draw appropriately\n")

while playing:
    #print(game_deck)
    if game.get_current_player().player_turn(game): #If current turn returns with a winner = true, end game
        playing = False

print("Game over.")