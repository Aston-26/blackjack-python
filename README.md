# Blackjack & Simulation
My implementation of Blackjack in Python developed as a personal project to investigate expected vs. observed results, learn about convergence and large scale simulations, as well as practise writing object-oriented code in a clear and well-structured way. Includes support for simulating as many hands as you wish according to a player strategy such as basic strategy (optimal decisions) or a never bust strategy and displays the results. Dealer and shoe rules can also be changed, such as how many cards are dealt before the deck is reshuffled and if the dealer hits on a soft 17.

# Important
I will update this with the results of my simulations and graphs using Matplotlib but I am very busy currently so I will come back and do this as soon as possible. I have investigated how different house rules and sample sizes effect EV, convergence rate, convergence accuracy etc, but not had time to graph it or write it up properly here.

## Current version
- Command line Blackjack with core game rules and a basic simulation
- Full support for simulation up to any number of hands with adjustable rules
- Dealer's second card is hidden until the player has finished their turn
- Dealer hits on a soft 17
- Supports any number of decks in shoe
- Player and dealer logic with standard outcomes

## TODO
- Add bankroll and variable bet amounts
- ~~Add automatic simulation~~
- ~~Make shoe persistent and add settings to control when shoe is reset~~
- ~~Add statistics for results of simulation~~
- Display results of simulation (Matplotlib)
- Investigate the effect of bet amount on simulation results
- ~~Move draw_card() to shoe instead of hand~~
- There are more things that again I will add when I have time, I have a TODO list on paper
