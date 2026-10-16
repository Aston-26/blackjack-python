from blackjack import Game, Player
from tables import HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY
# import matplotlib - do this when ready to add graphs

# CONSTANTS
NUMBER_OF_HANDS = 100000
DECKS_IN_SHOE = 2
# MAX_HANDS = 4 use this to control the maximum number of hands a player can have (resplitting control)
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

#
# max_hands is the maximum number of hands a player can currently have, i.e. 2 hands means 1 split is allowed per round
#

def basic_strategy(hand, dealer_upcard): # this function returns the mathematically optimal move every time
    dealer_card_value = dealer_upcard.get_card_value()

    if hand.can_split() and PAIR_STRATEGY[(hand.cards[0].rank, dealer_card_value)] == "P":
        return "split" # only considering splitting here, all cases where we hit/stand on a pair are handled later

    if hand.is_soft:
        score = hand.calculate_score()
        action = SOFT_STRATEGY[(score, dealer_card_value)]

        if action == "S":
            return "stand"
        elif action == "H":
            return "hit"
        elif action == "D":
            if len(hand.cards) == 2:
                return "double"
            else:
                return "hit"
        elif action == "Ds":
            if len(hand.cards) == 2:
                return "double"
            else:
                return "stand"
        else: # safety net error message as an action for hard hands should always be S, H, D or Ds
                    print("Unexpected action given in soft hand action")

    else: # the hand is hard so we use HARD_STRATEGY
        # these two checks ensure we dont accidentally pass any out of range scores to the dictonary and cause a key error
        # technically this means the dictionary can be made shorter for HARD_STRATEGY, but for completeness incase it is used later I will leave those cases
        score = hand.calculate_score()
        if score >= 17:
            return "stand"
        elif score <= 8:
            return "hit"
        
        action = HARD_STRATEGY[(score, dealer_card_value)]
        if action == "S":
            return "stand"
        elif action == "H":
            return "hit"
        elif action == "D":
            if len(hand.cards) == 2:
                return "double"
            else:
                return "hit"
        else: # safety net error message as an action for hard hands should always be S, H or D (not Ds)
            print("Unexpected action given in hard hand action")



def simulate(strategy, num_hands=NUMBER_OF_HANDS, deckcount=DECKS_IN_SHOE):
    player = Player(strategy)
    game = Game(deckcount, player, True)

    # consider a dedicated dataclass instead of a dictionary as I add support for tracking more metrics
    total_hands_played = 0
    results = { "Player": 0,
            "Dealer": 0,
            "Push": 0 }

    for _ in range(num_hands):
        round_results = game.play_round()
        total_hands_played += len(round_results)

        for outcome in round_results:
            if outcome == "Player":
                results["Player"] += 1
            elif outcome == "Dealer":
                results["Dealer"] += 1
            else:
                results["Push"] += 1

    # logically these print statements probably dont belong here so I will move them late
    print(f"Rounds played: {num_hands}")
    print(f"Total hands played: {total_hands_played}")
    return results


# small test
results = simulate(basic_strategy)

for key, pair in results.items():
    print(f"{key}: {pair}")
