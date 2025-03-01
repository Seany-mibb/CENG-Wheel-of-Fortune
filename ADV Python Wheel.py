import random
import turtle
import time
import math

class WheelHangman:
    def __init__(self):
        self.phrases = ["HELLO I AM CURRENTLY A PART OF CENG", "I LIKE CHESS"]
        self.phrase = random.choice(self.phrases)  # Randomly choose a phrase from the list
        self.guessed_letters = set()  # Using a set() because it doesn't append elements that're already in the set
        self.total_money = 0
        self.wheel_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]  # Values on the wheel
        
        self.screen = turtle.Screen()
        self.screen.title("Wheel Hangman")
        self.screen.tracer(0)  # Disable automatic screen updates to control when they happen
        
        self.writer = turtle.Turtle()
        self.writer.hideturtle()  # Hide the turtle since we only want to use it to draw text
        self.writer.penup()
        
        self.wheel = turtle.Turtle()
        self.wheel.speed(0)
        self.draw_wheel()  # Draw the wheel on the screen
        
        self.pointer = turtle.Turtle()
        self.pointer.shape("triangle")
        self.pointer.color("red")
        self.pointer.penup()
        self.pointer.goto(0, 120)  # Position the pointer on the wheel
        
    def draw_wheel(self):
        self.wheel.penup()
        self.wheel.goto(0, -100)
        self.wheel.pendown()
        self.wheel.circle(100)  # Draw the circular wheel

        # One extra iteration to ensure there is not side that is not created yet 
        for i in range(11):
            angle = i * 36  # 360 degrees divided by 10 sections on the wheel
            x = 100 * math.cos(math.radians(angle))  # Calculate x position of each section
            y = 100 * math.sin(math.radians(angle))  # Calculate y position of each section
            self.wheel.penup()
            self.wheel.goto(0, 0)
            self.wheel.pendown()
            self.wheel.goto(x, y)
    
    def spin_wheel(self):
        spins = random.randint(10, 30)  # Random number of spins for the wheel
        final_value = None
        for _ in range(spins):
            self.pointer.right(36)  # Rotate the pointer by 36 degrees (1/10th of a full circle)
            final_value = random.choice(self.wheel_values)  # Randomly pick a value from the wheel
            self.draw_text(f"Wheel stopped at: {final_value}", 0, 200)  # Show the wheel's stopping value
            self.screen.update()
            time.sleep(0.1)  # Adds delay to simulate a spinning wheel
        time.sleep(1)  # Slight pause before returning the final value
        return final_value

    def display_phrase(self):
        # Show the current state of the phrase with underscores for unguessed letters
        return ' '.join(letter if letter in self.guessed_letters else '_' for letter in self.phrase)

    def draw_text(self, text, x, y):
        self.writer.clear()  # Clearing any previous text on the interface
        self.writer.goto(x, y)
        self.writer.write(text, align="center", font=("Arial", 13, "normal"))  # Draw new text on screen

    def play_game(self):
        # Automatically add spaces to guessed letters
        for letter in self.phrase:
            if letter == " ":
                self.guessed_letters.add(" ")

        while set(self.phrase) - self.guessed_letters:  # Continuing until all letters are guessed aka. when the set difference is empty
            self.draw_text("Phrase: " + self.display_phrase(), 0, 200)
            self.screen.update()
            time.sleep(1)
            
            guess = self.screen.textinput("Guess a character", "Enter a character:")
            if guess and len(guess) == 1:
                guess = guess.upper()  # Convert the guess to uppercase
            
            if guess == " ":
                self.draw_text("You guessed a space! No points awarded.", 0, -200)
                self.screen.update()
                time.sleep(3)  # Waiting before continuing
                continue  # Skip the rest of the loop and ask for another guess
            
            if guess and guess in self.phrase and guess not in self.guessed_letters:  # Check if guess is correct and not already guessed
                occurrences = self.phrase.count(guess)  # Count how many times the guessed letter appears
                self.guessed_letters.add(guess)  # Add the letter to the guessed set
                
                wheel_value = self.spin_wheel()  # Spin the wheel for the money value
                round_money = occurrences * wheel_value  # Calculate money earned for this guess
                self.total_money += round_money  # Add the money to the total
                self.draw_text(f"Correct! '{guess}' appears {occurrences} times. You earned ${round_money}.", 0, -200)

            else:
                self.draw_text("Invalid, Incorrect or already guessed!", 0, -200)
            
            self.screen.update()
            time.sleep(3)  # Waiting before continuing
        
        # Game over, display the result
        self.draw_text(f"You won! The phrase was: {self.phrase}\nTotal money: ${self.total_money}", 0, -200)
        self.screen.update()
        self.screen.mainloop()  # Keep the window open after the game ends

if __name__ == "__main__":
    game = WheelHangman()
    game.play_game()
