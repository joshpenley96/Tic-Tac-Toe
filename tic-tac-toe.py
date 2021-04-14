from copy import deepcopy


board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
reset_board = deepcopy(board)



#function called to make the board visible
def see_board(board):
        return print("\n\n\n"
                "              |     |        \n"
                "          ", board[0][0], " | ", board[0][1], " | ", board[0][2], "    \n"
                "         _____|_____|_____   \n"
                "              |     |        \n"
                "          ", board[1][0], " | ", board[1][1], " | ", board[1][2], "    \n"
                "         _____|_____|_____   \n"
                "              |     |        \n"
                "          ", board[2][0], " | ", board[2][1], " | ", board[2][2], "    \n"
                "              |     | \n\n\n")



#function that asks the user which symbol they want to play as
def user_symbol():
        user_sym = input("\n\nWould you like to play as 'X' or 'O'? (type 'X' or 'O', then press Enter)... ")
        if user_sym.upper() == "X":
                return True
        elif user_sym.upper() == "O":
                return False
        elif user_sym == "q":
                qut = input("\n\nAre you sure you want to leave Steve hangin? (y/n)... ")
                if qut == "y":
                        quit()
                else:
                        return user_symbol()
        else:
                print("\nPlease choose 'X' or 'O'.\n")
                return user_symbol()

        
#function called at game beginning asking the user if they would like to go first.
def go_first():
        first = input("\n\nWould you like to go first? (type 'y' for yes, or 'n' for no.)... ")
        if first == "y":
                return True
        elif first == "n":
                return False
        elif first == "q":
                qut = input("\n\nAre you sure you want to leave Steve hangin? (y/n)... ")
                if qut == "y":
                        quit()
                else:
                        return go_first()
        else:
                print("\nPlease enter 'y' or 'n'.\n")
                return go_first()


#function called to tell which moves are available.
def available_moves(input_board):
        moves = []
        for row in input_board:
                for col in row:
                        if type(col) == int:
                                moves.append(col)
        return moves


#function that updates the board with each selection
def select_space(input_board, space, symbol):
        if space not in range(1,10):
                return False
        row = int((space-1)/3)
        col = (space-1)%3
        if input_board[row][col] != "X" and input_board[row][col] != "O":
                input_board[row][col] = symbol
                return True
        else:
                return False


#function called when it is time for the user to choose a space
def user_choose_space(input_board, symbol):
        space = input("\n\nIt is your turn. Where would you like to go?... ")
        if space == "q":
                qut = input("\n\nAre you sure you want to quit on Steve? (y/n)... ")
                if qut == "y":
                        quit()
                else:
                        return user_choose_space(input_board, symbol)
        try:
                space_int = int(space)
        except:
                print("\nPlease enter a number that correlates with an available space, then press Enter.\n")
                return user_choose_space(input_board, symbol) 
        if int(space) in available_moves(input_board):
                        select_space(input_board, int(space), symbol)
                        return
        else:
                print("\nPlease enter a number that correlates with an available space, then press Enter.\n")
                return user_choose_space(input_board, symbol)


#function called if a player has won
def winner(input_board, symbol):
        for row in input_board:
                if row.count(symbol) == 3:
                        return True
        for i in range(3):
                if input_board[0][i] == symbol and input_board[1][i] == symbol and input_board[2][i] == symbol:
                        return True
        if input_board[0][0] == symbol and input_board[1][1] == symbol and input_board[2][2] == symbol:
                return True
        if input_board[0][2] == symbol and input_board[1][1] == symbol and input_board[2][0] == symbol:
                return True
        return False


#function called when game is over
def game_over(input_board):
        return winner(input_board, "X") or winner(input_board, "O") or len(available_moves(input_board)) == 0


#function that communicates to Steve the end game of each decision
def end_game(board):
        if game_over(board) and winner(board, "X"):
                return 1
        elif game_over(board) and winner(board, "O"):
                return -1
        else:
                return 0

        
#function called when it is Steve's turn to choose a space. This function is a modified form of a minimax function.
def steves_choice(input_board, is_maximizing):
        if game_over(input_board):
                return [end_game(input_board), ""]
        best_move = ""
        if is_maximizing == True:
                best_value = -float("Inf")
                symbol = "X"
        else:
                best_value = float("Inf")
                symbol = "O"
        for move in available_moves(input_board):
                new_board = deepcopy(input_board)
                select_space(new_board, move, symbol)
                hypothetical_value = steves_choice(new_board, not is_maximizing)[0]
                if is_maximizing == True and hypothetical_value > best_value:
                        best_value = hypothetical_value
                        best_move = move
                if is_maximizing == False and hypothetical_value < best_value:
                        best_value = hypothetical_value
                        best_move = move
        return [best_value, best_move]



                               
#gameplay function
def tic_tac_toe(board):
        see_board(board)
        if user_symbol():
                user = "X"
                steve = "O"
                maximizing = False
        else:
                user = "O"
                steve = "X"
                maximizing = True
        if go_first():
                user_choose_space(board, user)
                see_board(board)
        while game_over(board) == False:
                print("\n\n\nIt's Steve's turn... \n\n\n")
                select_space(board, steves_choice(board, maximizing)[1], steve)
                see_board(board)
                if game_over(board):
                        break
                user_choose_space(board, user)
                see_board(board)
        if winner(board, user):
                print("\n\nCongratulations!!! You beat Steve, which is impossible, so this comment will never be read. \n\n")
        elif winner(board, steve):
                print("\n\nSorry, Steve won. Don't worry, it happens to everyone. Better luck next time! \n\n")
        else:
                print("\n\nThe game has ended in a tie, and Steve is unsatisfied. You should be proud though, Steve is really good. \n\n")
        play_again = input("\n\nWould you like to play again? (y/n)... ")
        if play_again == "y":
                tic_tac_toe(reset_board)
        else:
                print("\n\nPeace out! \n\n")
                exit()
                
        


      

print("\n\nCongratulations! you've made it to the final level of tic-tac-toe. \nYou will now face Steve. Steve is a world-renowned AI tic-tac-toe champion who has never lost a game. \nGood Luck!\n\nYou can type the letter 'q' to quit at anytime, but be warned, Steve doesn't like sore losers.")
tic_tac_toe(board)



