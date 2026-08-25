import random


class Card:
    card_value = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10} # No ace as it can take two value and is handled later

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_card_value(self):
        return Card.card_value[self.rank]


class Shoe:
    def __init__(self, deckcount):
        self.deckcount = int(deckcount)
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        self.cards = []
        self.reset_shoe()

    def fill_shoe(self):
        for _ in range(self.deckcount):
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card(rank, suit))

    def shuffle_shoe(self):
        random.shuffle(self.cards)

    def reset_shoe(self):
        self.cards = [] # ensure when this function is called multiple times it clears all previous cards leftover
        self.fill_shoe()
        self.shuffle_shoe()

    def draw_card(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.is_soft = False
        self.is_bust = False
        self.is_doubled = False

    def add_card(self, card):
        self.cards.append(card)

    def calculate_score(self):
        score = 0
        usable_aces = 0

        for card in self.cards:
            if card.rank == "Ace":
                score += 11
                usable_aces += 1
            else:
                score += card.get_card_value()

        while score > 21 and usable_aces > 0:
            score -= 10
            usable_aces -= 1

        if usable_aces >= 1:
            self.is_soft = True
        else:
            self.is_soft = False

        return score

    def show_hand(self):
        for card in self.cards:
            print(card.rank, "of", card.suit)

    def reset_hand(self):
        self.cards = []
        self.is_soft = False
        self.is_bust = False
#        self.is_doubled = False


class Player:
    def __init__(self, strategy=None):
        self.hand = Hand()
        self.strategy = strategy

    def player_action(self, dealer_upcard):
        if self.strategy is None:
            action = input("Enter player move: (hit/stand/double) ")
            return action
        else:
            return self.strategy(self.hand, dealer_upcard)


class Dealer:
    def __init__(self): # S17 should be a boolean where True indicates the dealer hits on a soft 17
        self.hand = Hand()
        self.show_all = False # Boolean to determine if a card should still be kept face down when displaying the dealaers hand
        #self.hit_on_S17 = True

    def dealer_action(self):
        score = self.hand.calculate_score()
        if score <= 16:
            action = "hit"
        elif score == 17:
            if self.hand.is_soft:
                action = "hit"
            else:
                action = "stand"
        else:
            action = "stand"

        return action
    

class Game:
    def __init__(self, deckcount, player=None, is_simulation=False):
        if player is None:
            self.player = Player()
        else:
            self.player = player

        self.dealer = Dealer()
        self.shoe = Shoe(deckcount)
        self.is_simulation = is_simulation # boolean where true represents this game is a simulation so do not display all cards every turn

    def setup_game(self): # deals initial cards and resets from previous rounds
        self.player.hand.reset_hand()
        self.dealer.hand.reset_hand()
        self.shoe.reset_shoe() # come back and change this later to investiage the effect of when the shoe is shuffled
        self.dealer.show_all = False

        for _ in range(2):
            self.player.hand.add_card(self.shoe.draw_card())
            self.dealer.hand.add_card(self.shoe.draw_card())

    def display_cards(self):
        print("----- Players hand -----")
        self.player.hand.show_hand()

        print("----- Dealers hand -----")
        if self.dealer.show_all == False:
            print(f"{self.dealer.hand.cards[0].rank} of {self.dealer.hand.cards[0].suit}")
            print("Face-down card")
        else:
            self.dealer.hand.show_hand()

    def player_turn(self):
        score = self.player.hand.calculate_score()
        
        while score < 21:
            if self.is_simulation == False:
                self.display_cards()

            dealer_upcard = self.dealer.hand.cards[0]
            current_action = self.player.player_action(dealer_upcard)

            if current_action == "hit":
                self.player.hand.add_card(self.shoe.draw_card())
            elif current_action == "stand":
                break
#            elif current_action == "double":
#                if len(self.player.hand.cards) == 2:
#                   pass
            else:
                print("Invalid action (hit/stand/double)")
            score = self.player.hand.calculate_score()

        if score > 21:
            self.player.hand.is_bust = True
            if self.is_simulation == False:
                print("Player bust --> dealer wins")
                self.display_cards()

    def dealer_turn(self):
        self.dealer.show_all = True

        if self.is_simulation == False:
            self.display_cards()

        action = self.dealer.dealer_action()
        while action == "hit":
            self.dealer.hand.add_card(self.shoe.draw_card())

            if self.is_simulation == False:
                self.display_cards() # maybe add time delay before to make it clearer
            action = self.dealer.dealer_action()

    def determine_winner(self): # different name for this function?
        player_score = self.player.hand.calculate_score()
        dealer_score = self.dealer.hand.calculate_score()

        if player_score > 21:
            return "Dealer"
        elif dealer_score > 21:
            return "Player"
        elif player_score > dealer_score:
            return "Player"
        elif dealer_score > player_score:
            return "Dealer"
        else:
            return "Push"

    def play_round(self):
        self.setup_game()
        self.player_turn()

        if self.player.hand.is_bust == True:
            return "Dealer" # player is bust so dealer wins

        self.dealer_turn()

        return self.determine_winner()

if __name__ == "__main__":
    print("Welcome!")
    print("You can play blackjack here, simply enter your move as hit/stand/double")
    print("You can use \"double\" to double down, but only on your first move of a hand")
    print("-" * 24)

    mygame = Game(2) # small test to play the game
    result = mygame.play_round()
    print ("-" * 24)

    if result != "Push":
        print(f"{result} wins")
    else:
        print("Push --> Bet returned") # in the case of a push the player keeps their bet, so I will put that in the message even though there is no support for betting yet