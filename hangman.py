# Import Required Modules
import random
import os
# Clear Screen before game starts : cls for windows and clear for mac
os.system('cls')
# list of secret words
word_list = ['robotics', 'python', 'art', 'math', 'leadership', 'volunteer', 'computer science', 'windows']
# Randomly select a secret word from the word list
secret_word = random.choice(word_list)
# Initialize variables to track guesses and attempts
correct_guesses = set()
incorrect_guesses = set()
attempts_left = 10
# Display Welcome to Hangman Game
print("Hello, Python Hangman Game")
# Function to display current game state
def display_game_state():
    # Display secret word with guessed letters revealed
    displayed_word = "".join([letter if letter in correct_guesses else "_" for letter in secret_word])
    print("Word: {}".format(displayed_word))
    print("Incorrect Guesses: {}".format(' '.join(incorrect_guesses)))
    print("Attempts Left: {}".format(attempts_left))

# Main game loop
while True:
    display_game_state()
    guess = input("Enter your guess: ").lower()

    # Check if the guess is in the secret word
    if guess in secret_word:
        correct_guesses.add(guess)
        # Check for win condition
        if set(secret_word).issubset(correct_guesses):
            print("Congratulations! You've guessed the word!")
            break
    else:
        incorrect_guesses.add(guess)
        attempts_left -= 1
        if attempts_left == 0:
            print("Game Over! You've run out of all attempts")
            print("The secret word was: {}".format(secret_word))
            break