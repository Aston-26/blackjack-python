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


class Hand:

    def __init__(self):
        self.cards = []
        self.is_soft = False
        self.is_bust = False

    def draw_card(self, thisshoe):
        chosen_card = thisshoe.cards.pop()
        self.cards.append(chosen_card)

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
            print(card.rank, card.suit)

    def reset_hand(self):
        self.cards = []
        self.is_soft = False
        self.is_bust = False


class Player:

    def __init__(self):
        self.hand = Hand()

    def player_action(self):
        action = input("Would you like to hit or stand? (hit/stand) ")
        return action


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

    def __init__(self, deckcount):
        self.player = Player()
        self.dealer = Dealer()
        self.shoe = Shoe(deckcount)

    def setup_game(self): # deals initial cards and resets from previous rounds
        self.player.hand.reset_hand()
        self.dealer.hand.reset_hand()
        self.shoe.reset_shoe() # come back and change this later to investiage the effect of when the shoe is shuffled
        self.dealer.show_all = False

        for _ in range(2):
            self.player.hand.draw_card(self.shoe)
            self.dealer.hand.draw_card(self.shoe)

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
            self.display_cards()
            current_action = self.player.player_action()
            if current_action == "hit":
                self.player.hand.draw_card(self.shoe)
            elif current_action == "stand":
                break
            else:
                print("Invalid action (hit/stand)")
            score = self.player.hand.calculate_score()

        if score > 21:
            self.player.hand.is_bust = True
            print("----- Player Bust; dealer wins -----")
            self.display_cards()


    def dealer_turn(self):
        self.dealer.show_all = True
        self.display_cards()
        action = self.dealer.dealer_action()

        while action == "hit":
            self.dealer.hand.draw_card(self.shoe)
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


mygame = Game(2)
print(mygame.play_round())