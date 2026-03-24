from flask import Flask, render_template, url_for, request, session
import random

app = Flask(__name__)
app.secret_key = "key_hello"

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("index.html")

# battleship board
def create_board():
    board = [["A", "B", "C", "D", "E", "F"],
                  ["1", "O", "O", "O", "O", "O"],
                  ["2", "O", "O", "O", "O", "O"],
                  ["3", "O", "O", "O", "O", "O"],
                  ["4", "O", "O", "O", "O", "O"],
                  ["5", "O", "O", "O", "O", "O"]]
    ships_placed = 0
    while ships_placed < 3:  # stop when 3 ships have been placed
        random_col = random.randint(1, 5)
        random_row = random.randint(1, 5)   # randomly generate a coord for a ship to be placed
        # ship will be shown with a Z
        board[random_col][random_row] = "Z"
        ships_placed += 1
    return board


@app.route("/battleship", methods=["POST", "GET"])
def battleship():

    # reset game
    if "board" not in session:
        session["board"] = create_board()
        session["ammo"] = 10
        session["hits"] = 0
        session["misses"] = 0
        session["message"] = "3 Enemy Ships Remaining!"
       
    while session["hits"] < 3 and session["ammo"] > 0:  # game continues until all ships are hit or ammo runs out
        if request.method == "POST":
            move = request.form.get("move").strip().upper()  # get and format move
            # validate move
            if len(move) == 2:
                row = ord(move[0]) - 65  # convert to number
                col = int(move[1]) - 1  # convert to number

                if 1 <= row <= 5 and 1 <= col <= 5:  # check if move within bounds
                    board = session["board"]
                    chosen_coord = board[row][col]

                    # Check if player hits target
                    if chosen_coord == "Z":
                        session["message"] = "HIT!"
                        session["hits"] += 1
                        board[col][row] = "H"   # Mark hit ships with H

                    elif chosen_coord == "O" or chosen_coord == "X":
                        session["message"] = "MISS!"
                        session["misses"] += 1
                        board[col][row] = "X"  # Mark missed spots with X
                        
                    elif chosen_coord == "H":
                        session["message"] = "You've already sunk this ship!"
                    session["ammo"] -= 1

                else:
                    session["message"] = "Invalid Move!"
            else:
                session["message"] = "Invalid Move!"

    return render_template("battleship.html", board=session["board"], ammo=session["ammo"], hits=session["hits"], misses=session["misses"], message=session["message"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)