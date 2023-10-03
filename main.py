from random import randint

game_data = {
    "blue": {
        "player_name": "blue",  # maybe have player name selection
        "pieces": [0, -1, 10, 1],  # field position -1 = home, 0-39 = board
        "start_field": 0,  # piece starts here after moving out of home
        "end_field": 39,  # piece shouldn't exceed this
        "finish": [0, 0, 0, 0],  # 0-1, 1 = in finish,
    },
    "yellow": {
        "player_name": "yellow",
        "pieces": [-1, 11, -1, -1],
        "start_field": 10,
        "end_field": 9,
        "finish": [0, 0, 0, 0],
    },
    "green": {
        "player_name": "green",
        "pieces": [-1, -1, 30, -1],
        "start_field": 20,
        "end_field": 19,
        "finish": [0, 0, 0, 0],
    },
    "red": {
        "player_name": "red",
        "pieces": [16, -1, -1, 28],
        "start_field": 30,
        "end_field": 29,
        "finish": [0, 0, 0, 0],
    },
}
board = [0] * 40
dice_number = 0
piece_in_home = 0  # 0 = no pieces in home, 1 = pieces in home, 2 = full home
# NOTE: possibly change piece_in_home to TRUE/FALSE maybe where TRUE can be both full home and partially full

player = "red"


def reset_game_data():
    new_game_data = {
        "blue": {
            "player_name": "blue",
            "pieces": [-1, -1, -1, -1],
            "start_field": 0,
            "end_field": 39,
            "finish": [0, 0, 0, 0],
        },
        "yellow": {
            "player_name": "yellow",
            "pieces": [-1, -1, -1, -1],
            "start_field": 10,
            "end_field": 9,
            "finish": [0, 0, 0, 0],
        },
        "green": {
            "player_name": "green",
            "pieces": [-1, -1, -1, -1],
            "start_field": 20,
            "end_field": 19,
            "finish": [0, 0, 0, 0],
        },
        "red": {
            "player_name": "red",
            "pieces": [-1, -1, -1, -1],
            "start_field": 30,
            "end_field": 29,
            "finish": [0, 0, 0, 0],
        },
    }
    return new_game_data


def color_text(player, text):
    color = ""

    if player == "red":
        color = "\033[91m"  # Red
    elif player == "blue":
        color = "\033[94m"  # Blue
    elif player == "yellow":
        color = "\033[93m"  # Yellow
    elif player == "green":
        color = "\033[92m"  # Green

    colored_text = f"{color}{text}\033[0m"  # reset to default color/white
    return colored_text


# print the board + extra fields
def print_board(extras=True):
    # replace 0 with player's letter and color it
    for player, player_data in game_data.items():
        for piece in player_data["pieces"]:
            if piece != -1:
                symbol = player[0].upper()  # get the player's letter and color it
                symbol += str(player_data["pieces"].index(piece) + 1)  # add piece index to symbol
                board[piece] = color_text(player, symbol)

    for cell in board:
        print(cell, end=" ")
        if cell == 0:  # match field numbers
            print(" ", end="")
    print()
    for i in range(1, 41):  # print field numbers for users
        if i < 10:
            print(i, end="  ")
        else:
            print(i, end=" ")

    if extras:
        print("\n" + print_extra_fields())


# prints pieces in home and finish; called in print_board()
def print_extra_fields():
    home = "In home: "
    finish = "In finish: "

    for player, player_data in game_data.items():
        if -1 in player_data["pieces"]:
            home += f"{color_text(player, player_data['pieces'].count(-1))} "
        else:
            home += f"{color_text(player, 0)} "

        if 1 in player_data["finish"]:
            finish += f"{color_text(player, player_data['finish'].count(1))} "
        else:
            finish += f"{color_text(player, 0)} "

    return f"{home}\n{finish}"


print_board(False)  # True for extra fields


def is_piece_on_same_field(target_field: int) -> bool:
    for pl in game_data.keys():
        for piece_pos in game_data[pl]["pieces"]:
            if piece_pos == target_field:
                return True
    return False


def kick_piece(other_player, target_field):
    piece_to_kick = game_data[other_player]["pieces"].index(target_field)  # cringe, cant just assign like that
    game_data[other_player]["pieces"][piece_to_kick] = -1
    print(f"Kicked {other_player}'s piece from field {target_field}.")


def select_piece_to_move(player):
    while True:
        try:
            piece_index = int(input(f"Enter the index of the piece you want to move (0-3) for {player}: "))
            if piece_index < 0 or piece_index > 3:
                print("Invalid piece index. Please enter a number between 0 and 3.")
            elif game_data[player]["pieces"][piece_index] == -1:
                print("This piece is in home. You can only select pieces on the board.")
            else:
                return piece_index
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# gets the field the player wants to move a piece to, does not check for pieces on target field itself
# TODO: return array of piece 'ID'/index and target field
def get_target_field(dice_number) -> list[int]:
    has_reroll = False
    piece_in_home = check_pieces_in_home()

    if dice_number == 6:
        print("rolled 6; has_reroll = True")
        has_reroll = True

    if piece_in_home == 2:  # home is full
        for piece in game_data[player]["pieces"]:
            if piece == -1:
                target_piece = piece
        return [target_piece, game_data[player]["start_field"]]

    elif piece_in_home == 1:  # has piece in home and on board
        if has_reroll:  # also means that
            while True:  # NOTE: maybe make finite loop
                choice = input("Do you want to move a piece from home or from the board? (h/b): ")
                if choice.lower() == "h":
                    target_piece = game_data[player]["pieces"].index(-1)
                    return [target_piece, game_data[player]["start_field"]]

                    # for piece in game_data[player]["pieces"]:
                    #     if piece == -1:
                    #         target_piece = piece
                    return [target_piece, game_data[player]["start_field"]]

                elif choice.lower() == "b":
                    # TODO: piece selection
                    pass
                else:
                    print("Invalid choice. Please enter 'h' or 'b'.")
        else:
            # TODO: piece selection
            pass

    else:
        # TODO: piece selection
        pass

    # idk what uh
    if has_reroll:
        execute_turn()


def check_pieces_in_home():  # returns 0 | 1 | 2
    if all(piece == -1 for piece in game_data[player]["pieces"]):
        print("Player has only -1 values in home. Must move pieces in home. retries FULL since full home")
        return 2
    elif -1 in game_data[player]["pieces"]:
        print("Player has piece(s) in home. Can choose which piece to move. retries 0, single roll")
        return 1
    else:
        print("Player has no pieces in home. Must move pieces on board. retries 0, single roll")
        return 0


def roll_dice():
    retries = 3

    if piece_in_home == 0 or piece_in_home == 1:  # only single roll if home not full
        retries = 1

    while retries >= 1:
        dice_number = randint(1, 6)
        print(dice_number, end=" ")

        retries -= 1

    return dice_number


print(f"\n{player}'s turn:")


def move_piece(target_piece, target_field):
    if is_piece_on_same_field(target_field):
        print("Target field occupied by one or more pieces.")
        for other_player in game_data.keys():
            if other_player != player:
                if target_field in game_data[other_player]["pieces"]:
                    print("Target field occupied by a piece from another player. Kicking it.")
                    kick_piece(other_player, target_field)

    print(f"previous field: {game_data[player]['pieces']}")
    game_data[player]["pieces"][target_piece] = target_field
    print(f"moved piece {target_piece} to field {target_field}; current: {game_data[player]['pieces']}")


def execute_turn():
    dice_number = roll_dice()
    # TODO: roll dice should just switch to next player if player did not get 6 and all pieces are in home
    target_piece_field = get_target_field(dice_number)  # returns array [piece_index, target_field]
    print(f"field that the piece wants to go on: {target_piece_field}")
    move_piece(target_piece_field[0], target_piece_field[1])
    print_board(False)


execute_turn()
