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
    print(logo)
    print("Blackjack with betting and an addtional scoring mechanic.\nScore as close to 21 points as possible.\nIf the suits match in your hand, you gain an addtional ten points.\n")
    player_name = input("What is your name? ")
    while True:
        while True:
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
                choice = input("Draw card? (y/n): ")
                if choice.lower() == 'y':
                    player.draw_card(deck)
                    if player.points > 21:
                        player.busted = True
                        os.system('cls' if os.name == 'nt' else 'clear')
                        player.show_hand()
                        print("Bust! You lose.")
                        choice = input("Play again? (y/n): ")
                        if choice.lower() == 'y':
                            break
                        if choice.lower() == 'n':
                            print("Thank you for playing!")
                            exit()
                elif choice.lower() == 'n':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue

            while dealer.points < 17:
                dealer.draw_card(deck)
                if dealer.points > 21:
                    dealer.busted = True
                    os.system('cls' if os.name == 'nt' else 'clear')
                    player.show_hand()
                    dealer.show_hand()
                    print("Dealer busts!")
                    break

            if not player.busted and not dealer.busted:
                player.show_hand()
            if not dealer.busted:
                dealer.show_hand()

            if player.points == dealer.points and not player.busted:
                print("It's a tie!")
            elif player.points > dealer.points and not player.busted:
                print("You win!")
            elif player.busted == True:
                print("Busted. You lost!")
                break
            elif player.points < dealer.points and not dealer.busted:
                print("You lose!")

            player_suits = set([card[0] for card in player.hand])
            if len(player_suits) == 1 and player.busted == False:
                print("Special Suit Condition: All cards in your hand are of the same suit!")
                special_suit = player_suits.pop()
                special_points = sum(values[card[1]] for card in player.hand)
                special_score = special_points + 10
                print(f"Special Suit Score: {special_score}")
                if special_score > dealer.points and player.busted == False:
                    print("You win with the special suit condition!")
                elif special_score < dealer.points and player.busted == False:
                    print("Dealer wins!")
                elif special_score == dealer.points and player.busted == False:
                    print("It's a tie!")

            choice = input("Play again? (y/n): ")
            if choice.lower() == 'y':
                break
            if choice.lower() == 'n':
                print("Thank you for playing!")
                exit()