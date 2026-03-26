#include <iostream>
using namespace std;

const int ROWS = 5;
const int COLS = 5;

void print_grid(const char grid[ROWS][COLS]){
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            cout << grid[r][c] << ' ';
        }
        cout << endl;
    }
    cout << endl;
}

/* TODO: Implement check_connection function (starting from a given cell `(row, col)`, recursively marks all connected cells with the same character (`current_symbol`) with the given `current_id` in the `region_id` array.)
 * Inputs:
 *  - row, col: coordinates of the cell to check
 *  - region_id: 2D array to update with region IDs
 *  - current_id: ID number assigned to the current region(cell)
 *  - grid: 2D array containing the user’s input map
 *  - current_symbol: symbol representing the region being explored
*/
void check_connection(int row, int col, int region_id[ROWS][COLS], int current_id, const char grid[ROWS][COLS], char current_symbol){
    /* Your code starts here */

    if (row>=ROWS || col>=COLS ||row<0 ||col<0)
        return;
        
    // avoid duplicate search
    if (region_id[row][col] != -1)
        return;

    if (current_symbol!=grid[row][col])
        return;
    
    region_id[row][col]=current_id;
    check_connection(row+1,col,region_id,current_id,grid,current_symbol);
    check_connection(row-1,col,region_id,current_id,grid,current_symbol);
    check_connection(row,col+1,region_id,current_id,grid,current_symbol);
    check_connection(row,col-1,region_id,current_id,grid,current_symbol);

    /* Your code ends here */
}



int main() {

    //Ask for grid of the map
    char grid[ROWS][COLS];
    cout << "Please enter the grid of this map: " << endl;
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            cin >> grid[r][c];
        }
    }

    print_grid(grid);
    
    //initializing the regions
    int region_id[ROWS][COLS];
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            region_id[r][c] = -1;
        }
    }


    //check the connection of the of a region
    int region_count = 0;
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            if (region_id[r][c] == -1){
                check_connection(r, c, region_id, region_count, grid, grid[r][c]);
                region_count++;
            }
        }
    }
    
    cout << "Here is the region by id: " << endl;
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            cout << region_id[r][c] << ' ';
        }
        cout << endl;
    }
    cout << endl;

}
