import tkinter as tk
from tkinter import messagebox
import winsound
import random

def play_sound(winner):
    if winner == "x":
        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
    else:
        winsound.PlaySound('clap.wav', winsound.SND_FILENAME)

def check_winner():
    global winner, x_score, o_score, match_count
    for combo in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            for i in combo:
                buttons[i].config(bg=random.choice(["#dc3838", "#99ccff", "#99ff99", "#ffff99","#0efbb7"
                                                    ]))
            play_sound(buttons[combo[0]]["text"])
            messagebox.showinfo("Tic-Tac-Toe", f"Player {buttons[combo[0]]["text"]} wins this match!")
            if buttons[combo[0]]["text"] == "x":
                x_score += 1
            else:
                o_score += 1
            match_count += 1
            update_score()
            check_final_winner()
            restart_game()
            return

    if all(button["text"] != "" for button in buttons):
        messagebox.showinfo("Tic-Tac-Toe", "It's a Tie!")
        match_count += 1
        check_final_winner()
        restart_game()

def button_click(index):
    global current_player
    if buttons[index]["text"] == "" and not winner:
        buttons[index]["text"] = current_player
        buttons[index].config(bg=random.choice(["#ffcccb", "#d0f0c0", "#add8e6", "#f0e68c"]))
        check_winner()
        toggle_player()

def toggle_player():
    global current_player
    current_player = "x" if current_player == "o" else "o"
    label.config(text=f"Player {current_player}'s turn")

def restart_game():
    global current_player, winner
    current_player = "x"
    winner = False
    for button in buttons:
        button.config(text="", bg="SystemButtonFace")
    label.config(text=f"Player {current_player}'s turn")

def update_score():
    score_label.config(text=f"Score - X: {x_score} / O: {o_score} (Match {match_count}/5)")

def check_final_winner():
    if match_count >= 5:
        if x_score >= 3:
            messagebox.showinfo("Tic-Tac-Toe", "Player X wins the series!")
        elif o_score >= 3:
            messagebox.showinfo("Tic-Tac-Toe", "Player O wins the series!")
        else:
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw series!")
        reset_series()

def reset_series():
    global x_score, o_score, match_count
    x_score = 0
    o_score = 0
    match_count = 0
    update_score()
    restart_game()

# Initialize the window
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.configure(bg="#f0f8ff")

# Create buttons
buttons = [tk.Button(root, text="", font=("Arial", 25), width=6, height=2, relief="raised", bd=5, command=lambda i=i: button_click(i)) for i in range(9)]

for i, button in enumerate(buttons):
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

# Initial variables
current_player = "x"
winner = False
x_score = 0
o_score = 0
match_count = 0

label = tk.Label(root, text=f"Player {current_player}'s turn", font=("Arial", 16), bg="#f0f8ff")
label.grid(row=3, column=0, columnspan=3)

score_label = tk.Label(root, text=f"Score - X: {x_score} / O: {o_score} (Match {match_count}/5)", font=("Arial", 14), bg="#f0f8ff")
score_label.grid(row=4, column=0, columnspan=3)

root.mainloop()