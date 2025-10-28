# Import Random Module
import random

# Options and score
choices = ["rock", "paper", "scissors"]
player_score = 0
computer_score = 0

# Welcome to RPS
print("Welcome to Rock, Paper, Scissors!")

# While Loop
while True:
    player_choice = input("Enter your choice (rock, paper, or scissors) or 'quit' to exit: ").lower()

    if player_choice == 'quit':
        break

    if player_choice not in choices:
        print("Invalid choice. Please choose rock, paper, or scissors.")
        continue

    computer_choice = random.choice(choices)

    print(f"\nYou chose: {player_choice}")
    print(f"Computer chose: {computer_choice}")

    if player_choice == computer_choice:
        print("It's a tie!")
    elif (player_choice == "rock" and computer_choice == "scissors") or (player_choice == "paper" and computer_choice == "rock") or (player_choice == "scissors" and computer_choice == "paper"):
        print("You win!")
        player_score += 1
    else:
        print("You lose!")
        computer_score += 1

    print(f"Score: You {player_score} - Computer {computer_score}\n")

# End and Score Display
print("\nThanks for playing!")
print(f"Final Score: You {player_score} - Computer {computer_score}")
