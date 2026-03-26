#include <iostream>
using namespace std;

const int ROWS = 5;
const int COLS = 5;
const int SIZE = 25;

void displaying_board(const char display_board[SIZE]){
    for (int r =0; r < ROWS; r++){
        for (int c =0; c < COLS; c++){
            int index = r * COLS + c;
            cout << display_board[index] << ' ';
        }
        cout << endl;
    }
    cout << endl;
}

// check if a cell contains a mine
bool check_mine(int row, int col, const char game_board[SIZE]){
    int index = row * COLS + col;
    return game_board[index] == '*';
}

// the operation when the player lose the game
void reveal_mines_on_loss(int row, int col, const char game_board[SIZE], char display_board[SIZE]){
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            int index = r * COLS + c;
            if (r == row && c == col)
                display_board[index] = '!';
            
            else if (game_board[index] == '*'){
                display_board[index] = '*';
            }
        }
    }
}

// counting the number of mines contained in adjacent cells of a cell (provided)
int count_mine(int row, int col, const char game_board[SIZE]){
    int mine_count = 0;
    for (int i = -1; i <= 1; i++){
        for (int j = -1; j <= 1; j++){
            if (i == 0 && j == 0){
                continue;
            }
            else{
                int cell_row = row + i;
                int cell_col = col + j;
                if (cell_row < 0 || cell_col < 0 || cell_row >= ROWS || cell_col >= COLS){
                    continue;
                }
                else {
                    int cell_ind = cell_row * COLS + cell_col;
                    if (game_board[cell_ind] == '*'){
                        mine_count++;
                    }
                }
            }
        }
    }
    return mine_count;
}

/* task 1: display the number of mines
row, col: the corresponding row and col of the clicked cell
display_board: the board for displaying information
num_mine: the number of mines in adjacent cells of a cell
*/
void show_number(int row, int col, char display_board[SIZE], int num_mine){
    // Your code begins here
     int index = row * COLS + col;
    
    display_board[index] = '0' + num_mine;
    // Your code ends here
}

/* task 2: conduct proper act when there is no mine in the adjacent cells of a cell (hint: exploring adjacent cells)
row, col: the corresponding row and col of the clicked cell
game_board: the game board for mine checking
display_board: the display board for displaying information
*/
void reveal_zero_neighbors(int row, int col, const char game_board[SIZE], char display_board[SIZE]){
    // Your code begins here
    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            // Skip the cell itself (i=0, j=0)
            if (i == 0 && j == 0) {
                continue;
            }

            //adj:adjacent
            int adj_row = row + i;
            int adj_col = col + j;

            if (adj_row >= 0 && adj_row < ROWS && adj_col >= 0 && adj_col < COLS) {
               
                if (!check_mine(adj_row, adj_col, game_board)) {
                    int adj_mine_count = count_mine(adj_row, adj_col, game_board);
                    show_number(adj_row, adj_col, display_board, adj_mine_count);
                }
            }
        }
    }

    // Your code ends here
}

/* task 3: check if the player wins the game
game_board: the game board for checking
display_board: the board for displaying information
*/
bool game_win(const char game_board[SIZE], const char display_board[SIZE]){
    // Your code begins here
    for (int i = 0; i < SIZE; i++) {
        // If a cell is unclicked ('-') AND not a mine → game not won
        if (display_board[i] == '-' && game_board[i] != '*') {
            return false;
        }
    }
    // If all unclicked cells are mines → game won
    return true;

    // Your code ends here
}

// show all mines when the player wins the game
void show_mine_win(const char game_board[SIZE], char display_board[SIZE]){
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            int index = r * COLS + c;
            if (game_board[index] == '*'){
                display_board[index] = '*';
            }
        }
    }
}

int main() {
    // The set of game boards (1D arrays)
    const char board0[SIZE] = {'-', '-', '-', '-', '-', '-', '-', '*', '-', '-', '*', '-', '*', '-', '*', '-', '*', '-', '-', '-', '*', '-', '-', '*', '-'};
    const char board1[SIZE] = {'*', '-', '-', '-', '-', '-', '*', '*', '-', '-', '-', '-', '-', '-', '*', '*', '*', '-', '-', '*', '-', '-', '*', '*', '*'};
    const char board2[SIZE] = {'*', '-', '*', '-', '*', '-', '-', '-', '-', '-', '*', '-', '-', '-', '*', '-', '-', '-', '-', '-', '*', '-', '*', '-', '*'};
    const char board3[SIZE] = {'*', '*', '*', '*', '*', '*', '-', '-', '-', '*', '*', '-', '-', '-', '*', '*', '-', '-', '-', '*', '*', '*', '*', '*', '*'};
    const char board4[SIZE] = {'*', '-', '-', '-', '*', '*', '-', '-', '-', '*', '*', '*', '*', '*', '*', '*', '-', '-', '-', '*', '*', '-', '-', '-', '*'};
    const char board5[SIZE] = {'-', '-', '*', '*', '-', '*', '-', '-', '-', '-', '*', '-', '-', '-', '-', '-', '-', '-', '-', '*', '-', '*', '-', '-', '-'};

    int game_board_selection;
    cout << "Please enter the game board you want to select: ";
    cin >> game_board_selection;
    cout << game_board_selection << endl;
    if (game_board_selection < 0 || game_board_selection > 5) {
        game_board_selection = 0;
    }

    char game_board[SIZE];
    switch (game_board_selection) {
        case 0:
            for (int i = 0; i < SIZE; i++) {
                game_board[i] = board0[i];
            }
            break;
        case 1:
            for (int i = 0; i < SIZE; i++) {
                game_board[i] = board1[i];
            }
            break;
        case 2:
            for (int i = 0; i < SIZE; i++) {
                game_board[i] = board2[i];
            }
            break;
        case 3:
            for (int i = 0; i < SIZE; i++) {
                game_board[i] = board3[i];
            }
            break;
        case 4:
            for (int i = 0; i < SIZE; i++) {
                game_board[i] = board4[i];
            }
            break;
        case 5:
            for (int i = 0; i < SIZE; i++) {
                game_board[i] = board5[i];
            }
            break;
        default:
            for (int i = 0; i < SIZE; i++) {
                game_board[i] = board0[i];
            }
            break;
    }
    // the set of board for display
    char display_board[SIZE] = {
        '-', '-', '-', '-', '-', 
        '-', '-', '-', '-', '-', 
        '-', '-', '-', '-', '-', 
        '-', '-', '-', '-', '-', 
          '-', '-', '-', '-', '-'};
    // declaration of some variable before starting the game loop
    int input_row;
    int input_col;
    // game loop. Stop when the player wins the game or there is no more inputs
    while (!game_win(game_board, display_board)){
        cout << "Please the row and col you want to explore (e.g., 2 3 means row 2 column 3): ";
        cin >> input_row >> input_col;
        cout << input_row << ' ' << input_col << endl;
        // validate coordinates
        if (input_row < 0 || input_row >= ROWS || input_col < 0 || input_col >= COLS) {
            cout << "Invalid coordinates. Please enter row and col in range [0, 4]." << endl;
            continue;
        }
        // check if there is a mine at the selected cell
        bool is_mine = check_mine(input_row, input_col, game_board);
        if (is_mine){
            cout << "OOPPSSS... wish you a lucky game next time!" << endl;
            reveal_mines_on_loss(input_row, input_col, game_board, display_board);
            displaying_board(display_board);
            break;
        }
        // displaying the correct information when the cell doesn't contain mine
        else {
            cout << "Smart move~~" << endl;
            int num_mine = count_mine(input_row, input_col, game_board);
            show_number(input_row, input_col, display_board, num_mine);
            if (num_mine == 0){
                reveal_zero_neighbors(input_row, input_col, game_board, display_board);
                displaying_board(display_board);
            }
            else {
                displaying_board(display_board);
            }
        }
    }
    // if the player wins the game, display the corresponding information
    if (game_win(game_board, display_board)){
        cout << "Congrats! You win the game! :))" <<endl;
        show_mine_win(game_board, display_board);
        displaying_board(display_board);
    }
}
