import random
import os
from art import logo


suits = ['♥', '♦', '♣', '♠']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}


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


while True:
    bank = 2000
    print(logo)
    print("Blackjack without split, but with betting and an addtional scoring mechanic.\nScore as close to 21 points as possible.\nIf all suits match in your hand, you score an addtional ten points and win 2x your bet.\n")
    player_name = input("What is your name? ")

    while True:
        while True:
            player_win = False
            bet = input(f"\nHow much do you want to bet? (Bank: ${bank}) $")
            if bet.isdigit():
                dealer_rng = random.randint(16,18)
                deck = [(suit, rank) for suit in suits for rank in ranks]
                random.shuffle(deck)
                player = Player(player_name)
                dealer = Player("Dealer")
                player.draw_card(deck)
                dealer.draw_card(deck)
                player.draw_card(deck)
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    player.show_hand()
                    print(f"Bank: ${bank}  |  Bet: {bet}")
                    choice = input("Draw card? (y/n): ")
                    if choice.lower() == 'y':
                        player.draw_card(deck)
                        if player.points > 21:
                            player.busted = True
                            os.system('cls' if os.name == 'nt' else 'clear')
                            player.show_hand()
                            bank -= int(bet)
                            print(f"Bank: ${bank}  |  Bet: {bet}")
                            print("Bust! You lose.")
                            break
                    elif choice.lower() == 'n':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        break
                    else:
                        os.system('cls' if os.name == 'nt' else 'clear')

                while dealer.points < dealer_rng and not player.busted:
                    dealer.draw_card(deck)
                    if dealer.points > 21:
                        dealer.busted = True
                        os.system('cls' if os.name == 'nt' else 'clear')
                        player.show_hand()
                        dealer.show_hand()
                        bank += int(bet)
                        print(f"Bank: ${bank}  |  Bet: {bet}")
                        print("Dealer busts! You win!\n")
                        break

                if not player.busted and not dealer.busted:
                    player.show_hand()
                if not dealer.busted and not player.busted:
                    dealer.show_hand()

                if player.points == dealer.points and not player.busted:
                    print(f"Bank: ${bank}  |  Bet: {bet}")
                    print("It's a tie!")
                elif player.points > dealer.points and not player.busted:
                    bank += int(bet)
                    print(f"Bank: ${bank}  |  Bet: {bet}")
                    print("You win!")
                elif player.points < dealer.points and not dealer.busted:
                    bank -= int(bet)
                    print(f"Bank: ${bank}  |  Bet: {bet}")
                    print("You lose!")

                player_suits = {card[0] for card in player.hand}
                if len(player_suits) == 1 and not player.busted and not player_win:
                    print("All cards in your hand are of the same suit!")
                    special_suit = player_suits.pop()
                    special_points = sum(values[card[1]] for card in player.hand)
                    special_score = special_points + 10
                    print(f"Special Suit Score: {special_score}\n")
                    if special_score > dealer.points and not player.busted and not player_win:
                        bank += (int(bet) * 2)
                        print("You turn things around and win with the special suit condition!\nYou also win 2x your bet!")
                    elif special_score < dealer.points and not player.busted and not player_win:
                        print("Dealer still wins!\n")
                    elif special_score == dealer.points and not player.busted and not player_win:
                        print("It's a tie!\n")

                while True:
                    choice2 = input("Play again? (y/n): ")
                    if choice2.lower() == 'n':
                        print(f"\nThank you for playing!\nYou cashed out with a total of ${bank}.\n")
                        exit()
                    elif choice2.lower() == 'y':
                        break
                    else:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        player.show_hand()
                        print(f"Bank: ${bank}  |  Bet: {bet}")
                break
            else:
                print("Invalid input. Please use numbers only.")