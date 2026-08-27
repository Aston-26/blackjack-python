import random


class Card:
    card_value = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10} # No ace as it can take two values and is handled later

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_card_value(self):
        return Card.card_value[self.rank]


class Shoe:
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]

    def __init__(self, deckcount, penetration=0.75):
        self.deckcount = int(deckcount)
        self.penetration = penetration # real number on the interval [0, 1] to represent the fraction of the shoe to play before reshuffling
        self.cut_card_threshold = round(self.deckcount * 52 * (1 - self.penetration))
        self.cards = []
        self.reset_shoe()

    def fill_shoe(self):
        for _ in range(self.deckcount):
            for suit in Shoe.suits:
                for rank in Shoe.ranks:
                    self.cards.append(Card(rank, suit))

    def shuffle_shoe(self):
        random.shuffle(self.cards)

    def reset_shoe(self):
        self.cards = [] # ensure when this function is called multiple times it clears all previous cards leftover
        self.fill_shoe()
        self.shuffle_shoe()

    def draw_card(self):
        return self.cards.pop()

    def check_reshuffle(self):
        if len(self.cards) <= self.cut_card_threshold:
            return True
        else:
            return False


class Hand:
    def __init__(self):
        self.cards = []
        self.is_soft = False
        self.is_bust = False
        self.is_doubled = False
        self.is_surrendered = False

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
        self.is_doubled = False
        self.is_surrendered = False


class Player:
    def __init__(self, strategy=None):
        self.hand = Hand()
        self.strategy = strategy

    def player_action(self, dealer_upcard):
        if self.strategy is None:
            action = input("Enter player move: ")
            return action
        else:
            return self.strategy(self.hand, dealer_upcard)


class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.show_all = False # Boolean to determine if a card should still be kept face down when displaying the dealers hand
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
        self.is_simulation = is_simulation # boolean where true represents this game is a simulation so do not display cards

    def setup_game(self): # deals initial cards and resets from previous rounds
        self.dealer.show_all = False
        self.player.hand.reset_hand()
        self.dealer.hand.reset_hand()
        if self.shoe.check_reshuffle():
            self.shoe.reset_shoe()

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

            elif current_action == "double":
                if len(self.player.hand.cards) == 2:
                   self.player.hand.is_doubled = True
                   self.player.hand.add_card(self.shoe.draw_card())
                   # when bet amount is added, put code here to double the bet amount
                   score = self.player.hand.calculate_score() # calculate score, because the break below means we will not otherwise calculate the new score of the hand
                   break # break out of loop to stop the player from hitting again after they double down
                else:
                    if self.is_simulation:
                        # defensive coding, if a strategy in simulation returns double when it shouldn't, the move is instead defaulted to hit
                        # beware, as this may cause strategies to behave in an unexpected way, so I will print an error message to make it clear if this occurs
                        print("Strategy tried to double when not allowed")
                        self.player.hand.add_card(self.shoe.draw_card())
                    else:
                        print("You cannot double down now.")

            elif current_action == "surrender":
                if len(self.player.hand.cards) == 2:
                    self.player.hand.is_surrendered = True
                    # when bankroll is added, half the player bet and return it to them here
                    break
                else:
                    print("You cannot surrender now")

            else:
                print("Invalid action")

            score = self.player.hand.calculate_score()

        if score > 21:
            self.player.hand.is_bust = True

    def dealer_turn(self):
        self.dealer.show_all = True

        if self.is_simulation == False:
            self.display_cards()

        action = self.dealer.dealer_action()
        while action == "hit":
            self.dealer.hand.add_card(self.shoe.draw_card())

            if self.is_simulation == False:
                self.display_cards() # add newlines where appropriate (so not just here) so that the command line running of the program looks cleaner
            action = self.dealer.dealer_action()

    def determine_winner(self):
        player_score = self.player.hand.calculate_score()
        dealer_score = self.dealer.hand.calculate_score()

        if dealer_score > 21:
            return "Player"
        elif dealer_score > player_score:
            return "Dealer"
        elif player_score > 21 or self.player.hand.is_surrendered:
            return "Dealer"
        elif player_score > dealer_score:
            return "Player"
        else:
            return "Push"

    def play_round(self):
        self.setup_game()
        self.player_turn()

        if self.player.hand.is_bust == True:
            return "Dealer" # player is bust so dealer wins

        if not self.player.hand.is_surrendered:
            self.dealer_turn()

        return self.determine_winner()

if __name__ == "__main__":
    print("Welcome!")
    # to make the code a bit simpler to read I have left .strip().lower() off user input, so it is their responsibility to enter their move correctly, I may change this later
    print("To play blackjack here, simply enter your move as hit/stand/double/surrender exactly as written here (lowercase with no spaces)")
    print("You can use \"double\" to double down, and \"surrender\" to surrender, but only on your first action for a hand")
    print("-" * 27)

    mygame = Game(6) # small test to play the game
    print(mygame.shoe.cut_card_threshold)
    result = mygame.play_round()
    print ("-" * 27)

    if mygame.player.hand.is_bust:
        mygame.display_cards()
        print("-" * 24)
        print("Player bust --> dealer wins")
    elif result != "Push":
        print(f"{result} wins")
    else:
        print("Push --> Bet returned") # in the case of a push the player keeps their bet, so I will put that in the message even though there is no support for betting yet