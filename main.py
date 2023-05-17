import random
import os
from art import logo

# Variables
suits = ['♥', '♦', '♣', '♠']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Objects
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.points = 0
        self.busted = False
    def draw_card(self, deck):
        card = deck.pop()
        self.hand.append(card)
        self.points += values[card[1]]
    def show_hand(self):
        print(f"{self.name}'s Hand:")
        card_lines = [[] for _ in range(7)]
        for card in self.hand:
            cardsuit, cardrank = card
            if cardrank == "10":
                card_lines[0].append('┌───────┐')
                card_lines[1].append(f'| {cardrank}    |')
                card_lines[2].append('|       |')
                card_lines[3].append(f'|   {cardsuit}   |')
                card_lines[4].append('|       |')
                card_lines[5].append(f'|    {cardrank} |')
                card_lines[6].append('└───────┘')
            else:
                card_lines[0].append('┌───────┐')
                card_lines[1].append(f'| {cardrank}     |')
                card_lines[2].append('|       |')
                card_lines[3].append(f'|   {cardsuit}   |')
                card_lines[4].append('|       |')
                card_lines[5].append(f'|     {cardrank} |')
                card_lines[6].append('└───────┘')
        for line in card_lines:
            print(' '.join(line))
        print(f"Total: {self.points}\n")

# Init
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    bank = 2000
    print(logo)
    print("A modified version of split-less blackjack with an addtional scoring mechanic.\nScore as close to 21 points as possible without going over and busting.\nAces always hold a value of 11, meaning it's an instant bust if you first draw two aces.\nIf all suits match in your hand, you gain +10 to your hand value and can win 2x your bet.\n")
    player_name = input("What is your name? ")

    # Turn start and bet
    while True:
        while True:
            player_win = False
            player_gameover = False
            player_endgame = False
            player_blackjack = False
            player_afterblackjack = False
            dealer_rng = random.randint(16,18)
            player = Player(player_name)
            dealer = Player("Dealer")
            bet = input(f"\nHow much do you want to bet? (Bank: ${bank}) $")
            if bet.isdigit():
                if int(bet) > int(bank):
                    print("Your bet is too large.")
                    continue
                elif int(bet) <= int(bank):
                    deck = [(suit, rank) for suit in suits for rank in ranks]
                    random.shuffle(deck)
                    player.draw_card(deck)
                    dealer.draw_card(deck)
                    player.draw_card(deck)

                    # Player turn
                    while True:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        player.show_hand()

                        # Instant blackjack and bust conditions
                        if player.points > 21 and not player_afterblackjack:
                            player.busted = True
                            os.system('cls' if os.name == 'nt' else 'clear')
                            player.show_hand()
                            bank -= int(bet)
                            if bank <= 0:
                                player_gameover = True
                            print(f"Bank: ${bank}  |  Bet: ${bet}")
                            print(f"Instant bust! You lose ${bet}.")
                            break
                        if player.points == 21 and not player_afterblackjack:
                            player_win = True
                            player_blackjack = True
                            os.system('cls' if os.name == 'nt' else 'clear')
                            player.show_hand()
                            bank += int(bet)
                            print(f"Bank: ${bank}  |  Bet: ${bet}")
                            print(f"Blackjack! You win ${bet}!")
                            break

                        # Draw card
                        print(f"Bank: ${bank}  |  Bet: ${bet}")
                        choice = input("Draw card? (y/n): ")
                        if choice.lower() == 'y' and not player_blackjack:
                            player.draw_card(deck)
                            player_afterblackjack = True
                            if player.points > 21:
                                player.busted = True
                                os.system('cls' if os.name == 'nt' else 'clear')
                                player.show_hand()
                                bank -= int(bet)
                                if bank <= 0:
                                    player_gameover = True
                                print(f"Bank: ${bank}  |  Bet: ${bet}")
                                print(f"Bust! You lose ${bet}.")
                                break
                        elif choice.lower() == 'n':
                            os.system('cls' if os.name == 'nt' else 'clear')
                            break
                        else:
                            os.system('cls' if os.name == 'nt' else 'clear')

                    # Dealer turn
                    while dealer.points < dealer_rng and not (player.busted or player_gameover or player_blackjack):
                        dealer.draw_card(deck)
                        if dealer.points > 21:
                            dealer.busted = True
                            os.system('cls' if os.name == 'nt' else 'clear')
                            player.show_hand()
                            dealer.show_hand()
                            bank += int(bet)
                            print(f"Bank: ${bank}  |  Bet: ${bet}")
                            print(f"Dealer busts! You win ${bet}!")
                            break

                    # Hand display conditions
                    if not (player.busted or dealer.busted or player_gameover or player_blackjack):
                        player.show_hand()
                        dealer.show_hand()

                    # Win/lose/tie conditions
                    if player.points == dealer.points and not (player.busted or player_gameover or player_blackjack):
                        print(f"Bank: ${bank}  |  Bet: ${bet}")
                        print("It's a tie.")
                    elif player.points > dealer.points and not (player.busted or player_gameover or player_blackjack):
                        bank += int(bet)
                        player_win = True
                        print(f"Bank: ${bank}  |  Bet: ${bet}")
                        print(f"You win ${bet}!")
                    elif player.points < dealer.points and not (dealer.busted or player_gameover or player_blackjack):
                        bank -= int(bet)
                        if bank <= 0:
                            player_gameover = True
                        print(f"Bank: ${bank}  |  Bet: ${bet}")
                        print(f"You lose ${bet}.")

                    # Special scoring
                    player_suits = {card[0] for card in player.hand}
                    if len(player_suits) == 1 and not (player.busted or player_win or player_gameover or dealer.busted or player_blackjack):
                        print("\nAll cards in your hand are of the same suit!")
                        special_suit = player_suits.pop()
                        special_points = sum(values[card[1]] for card in player.hand)
                        special_score = special_points + 10
                        print(f"Special Suit Score: {special_score}\n")
                        if special_score > dealer.points and player.points == dealer.points:
                            bank += int(bet)
                            print(f"You win your bet with the special suit condition!\nYou now have ${bank}!")
                        elif special_score > dealer.points:
                            bank += (int(bet) * 3)
                            print(f"You win your bet back with the special suit condition!\nYou also gain an addtional 2x your bet and now have ${bank}!")
                        elif special_score < dealer.points:
                            print("Dealer still wins!")
                        elif special_score == dealer.points:
                            print("It's a tie.")

                # Bet amount check
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')

                # End game conditions
                while not player_gameover:
                    choice2 = input("\nPlay again? (y/n): ")
                    if choice2.lower() == 'n':
                        print(f"\nThank you for playing!\nYou cashed out with a total of ${bank}.")
                        player_endgame = True
                        break
                    elif choice2.lower() == 'y':
                        break
                    else:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        player.show_hand()
                        print(f"Bank: ${bank}  |  Bet: ${bet}")
                if player_gameover or player_endgame:
                    if player_gameover:
                        print("\nGame over! Your bank balance is $0.")
                    while True:
                        choice2 = input("\nRestart game? (y/n): ")
                        if choice2.lower() == 'n':
                            print("\nGoodbye.\n")
                            exit()
                        elif choice2.lower() == 'y':
                            break
                        else:
                            os.system('cls' if os.name == 'nt' else 'clear')
                break

            # Numeric bet check
            else:
                print("Invalid input. Please use whole numbers only.")
        if player_gameover or player_endgame:
            break