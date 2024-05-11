import tkinter as tk
from tkinter import messagebox
import random

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.configure(bg="black")
        
        self.player_hand = []
        self.dealer_hand = []
        
        self.deck = self.create_deck()
        
        self.player_score = 0
        self.dealer_score = 0
        
        self.create_widgets()
    
    def create_deck(self):
        """Create a standard deck of 52 playing cards."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        deck = [(rank, suit) for suit in suits for rank in ranks]
        return deck

    def deal_card(self):
        """Deal a card from the deck."""
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    def calculate_hand_value(self, hand):
        """Calculate the value of a hand."""
        value = 0
        num_aces = 0
        for card in hand:
            rank = card[0]
            if rank.isdigit():
                value += int(rank)
            elif rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif rank == 'Ace':
                num_aces += 1
                value += 11
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value
    
    def create_widgets(self):
        self.player_frame = tk.LabelFrame(self.root, text="Player's Hand", padx=10, pady=10, font=("Arial", 16, "bold"), fg="white", bg="black")
        self.player_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.player_text = tk.Text(self.player_frame, height=5, width=30, font=("Arial", 14), fg="white", bg="black")
        self.player_text.pack()
        
        self.dealer_frame = tk.LabelFrame(self.root, text="Dealer's Hand", padx=10, pady=10, font=("Arial", 16, "bold"), fg="white", bg="black")
        self.dealer_frame.grid(row=0, column=1, padx=10, pady=10)
        
        self.dealer_text = tk.Text(self.dealer_frame, height=5, width=30, font=("Arial", 14), fg="white", bg="black")
        self.dealer_text.pack()
        
        self.button_frame = tk.Frame(self.root, bg="black")
        self.button_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit, width=15, font=("Arial", 14, "bold"), bg="green", fg="white")
        self.hit_button.pack(side=tk.LEFT, padx=5)
        
        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand, width=15, font=("Arial", 14, "bold"), bg="red", fg="white")
        self.stand_button.pack(side=tk.RIGHT, padx=5)
        
        self.start_game()

    def start_game(self):
        """Start a new game of Blackjack."""
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        
        self.update_player_hand()
        self.update_dealer_hand(show_first_card_only=True)
        
        self.check_blackjack()
    
    def hit(self):
        """Player chooses to hit."""
        self.player_hand.append(self.deal_card())
        self.update_player_hand()
        if self.calculate_hand_value(self.player_hand) > 21:
            messagebox.showinfo("Result", "Bust! You lose.")
            self.start_game()
    
    def stand(self):
        """Player chooses to stand."""
        self.update_dealer_hand(show_first_card_only=False)
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())
            self.update_dealer_hand(show_first_card_only=False)
        
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        if dealer_value > 21 or player_value > dealer_value:
            messagebox.showinfo("Result", "Congratulations! You win!")
        elif player_value == dealer_value:
            messagebox.showinfo("Result", "It's a tie!")
        else:
            messagebox.showinfo("Result", "Dealer wins.")
        self.start_game()
    
    def update_player_hand(self):
        """Update the display of the player's hand."""
        self.player_text.delete('1.0', tk.END)
        for card in self.player_hand:
            self.player_text.insert(tk.END, f"{card[0]} of {card[1]}\n")
        self.player_text.insert(tk.END, f"Total: {self.calculate_hand_value(self.player_hand)}")
    
    def update_dealer_hand(self, show_first_card_only=False):
        """Update the display of the dealer's hand."""
        self.dealer_text.delete('1.0', tk.END)
        if show_first_card_only:
            self.dealer_text.insert(tk.END, f"{self.dealer_hand[0][0]} of {self.dealer_hand[0][1]}\n")
            self.dealer_text.insert(tk.END, "Hidden Card\n")
        else:
            for card in self.dealer_hand:
                self.dealer_text.insert(tk.END, f"{card[0]} of {card[1]}\n")
            self.dealer_text.insert(tk.END, f"Total: {self.calculate_hand_value(self.dealer_hand)}")
    
    def check_blackjack(self):
        """Check if either player or dealer has a Blackjack."""
        player_blackjack = self.calculate_hand_value(self.player_hand) == 21
        dealer_blackjack = self.calculate_hand_value(self.dealer_hand) == 21
        if player_blackjack and not dealer_blackjack:
            messagebox.showinfo("Result", "Congratulations! You got Blackjack!")
            self.start_game()
        elif dealer_blackjack and not player_blackjack:
            messagebox.showinfo("Result", "Dealer got Blackjack. You lose.")
            self.start_game()
        elif player_blackjack and dealer_blackjack:
            messagebox.showinfo("Result", "It's a tie! Both you and the dealer got Blackjack.")
            self.start_game()

root = tk.Tk()
app = BlackjackGUI(root)

# Center the window on the screen
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.mainloop()
