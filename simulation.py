from blackjack import Game, Player
# import matplotlib - do this when ready to add graphs

# CONSTANTS
NUMBER_OF_HANDS = 100
DECKS_IN_SHOE = 2
# ideas to add when necessary - initial balance, bet amount, hit on soft 17 (here instead of in blackjack.py?), number of simulations, blackjack payout, when to reshuffle shoe etc.

def never_bust_strategy(hand, dealer_upcard): # dealer_upcard will not be used, but for best OOP practices the main program should not be changed to check if the strategy being used requires this information or not
    score = hand.calculate_score()

    if hand.is_soft:
        if score >= 18: # You cannot bust when hitting on a soft hand, but hitting on a soft hand >= 18 reduces expected value
            return "stand"
    else:
        if score > 11:
            return "stand"
        
    return "hit"


def basic_strategy(hand, dealer_upcard):
    pass # this return the mathematically optimal move every time


def simulate(strategy, num_hands=NUMBER_OF_HANDS, deckcount=DECKS_IN_SHOE):
    player = Player(strategy)
    game = Game(deckcount, player, True)

    # consider a dedicated dataclass instead of a dictionary as I add support for tracking more metrics
    results = { "Player": 0,
            "Dealer": 0,
            "Push": 0 }

    for _ in range(num_hands):
        result = game.play_round()

        if result == "Player": # maybe a win on a doubled hand should count as +2? Not sure yet
            results["Player"] += 1
        elif result == "Dealer":
            results["Dealer"] += 1
        else:
            results["Push"] += 1

    return results


# small test
results = simulate(never_bust_strategy)

for key, pair in results.items():
    print(f"{key}: {pair}")