// Helper routines for path calculation, printing, and recursive search.
//  i use formater for this task, so the code looks nice and clean, but the logic is all mine. i promise. - Jason
#ifndef HELPERS_H
#define HELPERS_H

#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>

#include "globals.cpp"

using namespace std;

/**
 * Helper function to read map from map file
 */
// mapName: name of the map file; map: 2D array to store the map; rows, cols: dimensions of the map (output)
bool readMapFromFile(const string &mapName, int map[MAX_MAP_SIZE][MAX_MAP_SIZE], int &rows, int &cols)
{
    string filename = mapName;
    if (filename.size() < 4 || filename.substr(filename.size() - 4) != ".txt")
    {
        filename += ".txt";
    }

    string filepath = filename;
    ifstream mapFile(filepath);
    if (!mapFile.is_open())
    {
        filepath = "given_testcases/" + filename; // fallback for old layout
        mapFile.open(filepath);
    }

    if (!mapFile.is_open())
    {
        cout << "Error: Cannot open " << filepath << endl;
        rows = 0;
        cols = 0;
        return false;
    }

    int fileRows, fileCols;
    mapFile >> fileRows >> fileCols;

    // Persist dimensions from file so callers do not rely on user input dimensions.
    rows = fileRows;
    cols = fileCols;

    if (rows > MAX_MAP_SIZE || cols > MAX_MAP_SIZE)
    {
        cout << "Error: Map dimensions exceed MAX_MAP_SIZE" << endl;
        mapFile.close();
        rows = 0;
        cols = 0;
        return false;
    }

    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            string token;
            mapFile >> token;
            if (token == string(1, WALL_SYMBOL))
            {
                map[i][j] = WALL_CELL;
            }
            else
            {
                map[i][j] = stoi(token);
            }
        }
    }

    mapFile.close();
    return true;
}

/**
 * Mark the path indices on an integer grid
 */
// indexMap: a 2D array to mark the indices of the path coordinates
void markPathIndex(int path[][2], int pathLength, int indexMap[][MAX_MAP_SIZE])
{
    // Initialize indexMap with -1.
    for (int i = 0; i < MAX_MAP_SIZE; i++)
    {
        for (int j = 0; j < MAX_MAP_SIZE; j++)
        {
            indexMap[i][j] = -1;
        }
    }

    // Mark indices for coordinates in the path.
    for (int i = 0; i < pathLength; i++)
    {
        int r = path[i][0];
        int c = path[i][1];
        if (r >= 0 && r < MAX_MAP_SIZE && c >= 0 && c < MAX_MAP_SIZE)
        {
            indexMap[r][c] = i;
        }
    }
}

/**
 * Get direction symbol for path visualization
 */
char directionSymbol(int path[][2], int pathLength, int index)
{
    if (index < 0 || index >= pathLength)
    {
        return '.';
    }
    if (index == pathLength - 1)
    {
        return 'E';
    }

    int dr = path[index + 1][0] - path[index][0];
    int dc = path[index + 1][1] - path[index][1];

    if (dr == -1 && dc == 0)
        return '^';
    if (dr == 1 && dc == 0)
        return 'v';
    if (dr == 0 && dc == -1)
        return '<';
    if (dr == 0 && dc == 1)
        return '>';

    return '*';
}

/**
 * Print the level 1 map with the path annotated
 */
// startR, startC: starting coordinates; targetR, targetC: exit coordinates
void printLevel1MapWithPath(int path[][2], int pathLength,
                            int map[][MAX_MAP_SIZE], int rows, int cols,
                            int startR, int startC, int targetR, int targetC)
{
    int indexMap[MAX_MAP_SIZE][MAX_MAP_SIZE];
    markPathIndex(path, pathLength, indexMap);

    cout << "\nPath annotated map:" << endl;
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            if (i == startR && j == startC)
            {
                cout << " S ";
            }
            else if (i == targetR && j == targetC)
            {
                cout << " E ";
            }
            else if (map[i][j] == WALL_CELL)
            {
                cout << " # ";
            }
            else if (indexMap[i][j] >= 0)
            {
                char sym = directionSymbol(path, pathLength, indexMap[i][j]);
                cout << " " << sym << " ";
            }
            else
            {
                cout << " . ";
            }
        }
        cout << endl;
    }
}

/**
 * Print the level 2 map with the path annotated
 */
void printLevel2MapWithPath(int map[][MAX_MAP_SIZE], int rows, int cols,
                            int path[][2], int pathLength,
                            int startR, int startC, int targetR, int targetC)
{
    int indexMap[MAX_MAP_SIZE][MAX_MAP_SIZE];
    markPathIndex(path, pathLength, indexMap);

    cout << "\nPath annotated map (survivor counts preserved):" << endl;
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            if (i == startR && j == startC)
            {
                cout << " S ";
            }
            else if (i == targetR && j == targetC)
            {
                cout << " D ";
            }
            else if (map[i][j] == WALL_CELL)
            {
                cout << " # ";
            }
            else if (indexMap[i][j] >= 0)
            {
                char sym = directionSymbol(path, pathLength, indexMap[i][j]);
                cout << " " << sym << " ";
            }
            else
            {
                cout << setw(2) << map[i][j] << " ";
            }
        }
        cout << endl;
    }
}

/**
 * Helper function to calculate bouncing position within boundaries
 */
int bouncePosition(int pos, int maxIndex)
{
    if (maxIndex <= 0)
        return 0;

    if (pos < 0)
    {
        pos = -pos;
    }

    int cycle = maxIndex * 2;
    pos = pos % cycle;

    if (pos <= maxIndex)
    {
        return pos;
    }
    return cycle - pos;
}

// Level 3 utility (non-TODO)
int calculateTimeCost(int num_rescued)
{
    return 1 + num_rescued / 4;
}

// Forward declarations for mutually recursive TODO functions.
int tryAllDirectionsMax(int map[][MAX_MAP_SIZE], int rows, int cols,
                        int targetRow, int targetCol,
                        int r, int c, bool visited[][MAX_MAP_SIZE],
                        int currentPath[][2], int currentPathLength,
                        int timeLeft,
                        int bestPath[][2], int &bestPathLength,
                        int dirIndex,
                        int &maxSurvivors, int currentSurvivors,
                        int unlockThreshold);

int rescueSurvivorsMax(int map[][MAX_MAP_SIZE], int rows, int cols,
                       int targetRow, int targetCol,
                       int r, int c, bool visited[][MAX_MAP_SIZE],
                       int currentPath[][2], int currentPathLength,
                       int timeLeft,
                       int bestPath[][2], int &bestPathLength,
                       int &maxSurvivors, int currentSurvivors,
                       int unlockThreshold);

bool tryAllDirectionsWithPenalty(int map[][MAX_MAP_SIZE], int rows, int cols,
                                 int targetRow, int targetCol,
                                 int r, int c, bool visited[][MAX_MAP_SIZE],
                                 int currentPath[][2], int currentPathLength,
                                 int timeLeft,
                                 int dirIndex,
                                 int outPath[][2], int &outPathLength,
                                 int currentSurvivors,
                                 int unlockThreshold,
                                 int &bestPathLength);

bool rescueSurvivorsWithPenalty(int map[][MAX_MAP_SIZE], int rows, int cols,
                                int targetRow, int targetCol,
                                int r, int c, bool visited[][MAX_MAP_SIZE],
                                int currentPath[][2], int currentPathLength,
                                int timeLeft,
                                int outPath[][2], int &outPathLength,
                                int currentSurvivors,
                                int unlockThreshold,
                                int &bestPathLength);

bool shortestPath(int map[][MAX_MAP_SIZE], int rows, int cols,
                  int path[][2], int &pathLength,
                  int targetRow, int targetCol,
                  int r, int c, bool visited[][MAX_MAP_SIZE],
                  int currentPath[][2], int currentPathLength);

bool shortestPathTryDirections(int map[][MAX_MAP_SIZE], int rows, int cols,
                               int path[][2], int &pathLength,
                               int targetRow, int targetCol,
                               int r, int c, bool visited[][MAX_MAP_SIZE],
                               int currentPath[][2], int currentPathLength,
                               int dirIndex);

/**
 * Phase A (Recursion Warm-up)
 * TODO A1: Print the path coordinates recursively.
 */
// path: 2D array storing path coordinates; pathLength: path length; index: current print index
void printPath(int path[][2], int pathLength, int index = 0)
{
    // Hint 1: Handle empty path.
    // Hint 2: Base case: index reaches pathLength.
    // Hint 3: Print current coordinate, then recurse to index + 1.
    // TODO: Implement this function

    // Follow the sample output format exactly:
    // (r,c) -> (r,c) -> ... with one space before and after ->.
    if (index >= pathLength)
    {
        return;
    }

    cout << "(" << path[index][0] << "," << path[index][1] << ")";
    if (index == pathLength - 1)
    {
        cout << endl;
        return;
    }

    cout << " -> ";
    printPath(path, pathLength, index + 1);
}

/**
 * Phase A (Recursion Warm-up)
 * TODO A2: Copy path coordinates recursively.
 */
// source: source path; copy: destination path; pathLength: length; index: current index
void copyPathRecursive(int source[][2], int copy[][2], int pathLength, int index = 0)
{
    // Hint 1: Base case: index reaches pathLength.
    // Hint 2: Copy one (row, col) pair each step.
    // Hint 3: Recurse with index + 1.
    // TODO: Implement this function
    if (index < pathLength)
    {
        copy[index][0] = source[index][0];
        copy[index][1] = source[index][1];
        copyPathRecursive(source, copy, pathLength, index + 1);
    }
}

/**
 * Phase A (Recursion Warm-up)
 * TODO A3: Recursively sum survivors along a path.
 */
int calculate_num_survivors(int map[][MAX_MAP_SIZE], int rows, int cols,
                            int path[][2], int pathLength, int index = 0)
{
    // Hint 1: Base case: index reaches pathLength.
    // Hint 2: Add current cell survivors and recurse to next index.
    // TODO: Implement this function
    if (index >= pathLength)
    {
        return 0;
    }
    int r = path[index][0];
    int c = path[index][1];
    int survivors = map[r][c];
    return survivors + calculate_num_survivors(map, rows, cols, path, pathLength, index + 1);
}

/**
 * Phase B (Level 1 Recursive Path Search)
 * TODO B1: Recursively find the shortest valid path to the exit.
 */
// TODO: Level 1: Shortest path finding using recursion
//
// @param map: The 2D array storing the map information
// @param rows: number of rows
// @param cols: number of columns
// @param path: output path if found
// @param pathLength: output path length
// @param targetRow: target row
// @param targetCol: target column
// @param r: current row
// @param c: current column
// @param visited: visited marks
// @param currentPath: path has been explored
// @param currentPathLength: length of current path
// @return: true if path found, false otherwise
bool shortestPath(int map[][MAX_MAP_SIZE], int rows, int cols,
                  int path[][2], int &pathLength,
                  int targetRow, int targetCol,
                  int r, int c, bool visited[][MAX_MAP_SIZE],
                  int currentPath[][2], int currentPathLength)
{
    // Hint 1: Prune invalid states first (bounds, wall, revisits, path overflow).
    // Hint 2: Record current state before exploring branches.
    // Hint 3: At target, update best path only if current path is shorter.
    // Hint 4: Explore all four directions (do not stop at first success).
    // Hint 5: Backtrack after branch exploration and return whether any route exists.
    // TODO: Implement this function

    if (r < 0 || r >= rows || c < 0 || c >= cols || map[r][c] == WALL_CELL || visited[r][c] || currentPathLength >= MAX_PATH_LENGTH)
    {
        return false;
    }

    visited[r][c] = true;
    currentPath[currentPathLength][0] = r;
    currentPath[currentPathLength][1] = c;

    if (r == targetRow && c == targetCol)
    {
        int fullLength = currentPathLength + 1;
        if (pathLength == 0 || fullLength < pathLength)
        {
            pathLength = fullLength;
            copyPathRecursive(currentPath, path, fullLength);
        }
        visited[r][c] = false; // backtrack before return
        return true;
    }

    //  helper 
    bool found = shortestPathTryDirections(
        map, rows, cols,
        path, pathLength,
        targetRow, targetCol,
        r, c, visited,
        currentPath, currentPathLength + 1, 0);

    visited[r][c] = false;
    return found;
}

/**
 * Phase B (Level 1 Recursive Path Search)
 * TODO B2: Recursively try all 4 directions for shortest-path search.
 * Note: This helper is separated from shortestPath to enforce recursive direction traversal.
 */
bool shortestPathTryDirections(int map[][MAX_MAP_SIZE], int rows, int cols,
                               int path[][2], int &pathLength,
                               int targetRow, int targetCol,
                               int r, int c, bool visited[][MAX_MAP_SIZE],
                               int currentPath[][2], int currentPathLength,
                               int dirIndex)
{
    // Hint 1: Base case when dirIndex >= 4.
    // Hint 2: Explore current direction via shortestPath(...), then recurse with dirIndex + 1.
    // Hint 3: Return whether any branch finds a valid route.
    // TODO: Implement this function

    if (dirIndex >= 4)
        return false;

    bool found = false;

    // check for each direction
    if (dirIndex == 0)
    {
        // UP
        found = shortestPath(map, rows, cols, path, pathLength, targetRow, targetCol, r - 1, c, visited, currentPath, currentPathLength);
    }
    else if (dirIndex == 1)
    {
        // DOWN
        found = shortestPath(map, rows, cols, path, pathLength, targetRow, targetCol, r + 1, c, visited, currentPath, currentPathLength);
    }
    else if (dirIndex == 2)
    {
        // LEFT
        found = shortestPath(map, rows, cols, path, pathLength, targetRow, targetCol, r, c - 1, visited, currentPath, currentPathLength);
    }
    else if (dirIndex == 3)
    {
        // RIGHT
        found = shortestPath(map, rows, cols, path, pathLength, targetRow, targetCol, r, c + 1, visited, currentPath, currentPathLength);
    }

    //  NEXT direction
    bool foundOther = shortestPathTryDirections(map, rows, cols, path, pathLength, targetRow, targetCol, r, c, visited, currentPath, currentPathLength, dirIndex + 1);

    return found|| foundOther;
}

/**
 * Phase C (Level 2 Penalty Tiles and Shortest Valid Path)
 * TODO C1: Recursive rescue with time/resource constraints and penalty tile mechanics.
 * Penalty tiles (negative values) reduce rescued survivors.
 */
bool rescueSurvivorsWithPenalty(int map[][MAX_MAP_SIZE], int rows, int cols,
                                int targetRow, int targetCol,
                                int r, int c, bool visited[][MAX_MAP_SIZE],
                                int currentPath[][2], int currentPathLength,
                                int timeLeft,
                                int outPath[][2], int &outPathLength,
                                int currentSurvivors,
                                int unlockThreshold,
                                int &bestPathLength)
{
    // Hint 1: Prune impossible states early (bounds, time, # cell, visited, max path).
    // Hint 2: Mark state and handle survivor collection/penalty (positive or negative values).
    // Hint 3: If we reach the target with enough survivors, check if we found a shorter path.
    // Hint 4: Recurse to all directions and backtrack visited on return.
    // TODO: Implement this function

    // bounds
    if (r < 0 || r >= rows || c < 0 || c >= cols)
        return false;

    // Wall, already visited, no time left, path too long
    if (map[r][c] == WALL_CELL || visited[r][c] || timeLeft <= 0 || currentPathLength >= MAX_PATH_LENGTH)
        return false;

    // current already longer than best found , no need to continue
    if (bestPathLength != 0 && currentPathLength >= bestPathLength)
        return false;

    visited[r][c] = true;
    currentPath[currentPathLength][0] = r;
    currentPath[currentPathLength][1] = c;

    // add current 
    int newSurvivors = currentSurvivors + map[r][c];

    if (r == targetRow && c == targetCol)
    {
        // ONLY success if we have enough survivors to unlock door
        if (newSurvivors >= unlockThreshold)
        {
            int fullLen = currentPathLength + 1;

            // Update only if this path shorter
            if (bestPathLength == 0 || fullLen < bestPathLength)
            {
                bestPathLength = fullLen;
                outPathLength = fullLen;
                copyPathRecursive(currentPath, outPath, fullLen);
            }

            // backtrack
            visited[r][c] = false;
            return true;
        }
        // not enough survivors 
        visited[r][c] = false;
        return false;
    }

    // Time cost, 1 per move , so timeLeft -1 for next step
    bool found = tryAllDirectionsWithPenalty(
        map, rows, cols,
        targetRow, targetCol,
        r, c, visited,
        currentPath, currentPathLength + 1,
        timeLeft - 1, 
        0,
        outPath, outPathLength,
        newSurvivors,
        unlockThreshold,
        bestPathLength);

    // BACKTRACK
    visited[r][c] = false;

    return found;
}

/**
 * Phase C (Level 2 Penalty Tiles and Shortest Valid Path)
 * TODO C2: Recursively try all four directions while tracking shortest valid path.
 */
bool tryAllDirectionsWithPenalty(int map[][MAX_MAP_SIZE], int rows, int cols,
                                 int targetRow, int targetCol,
                                 int r, int c, bool visited[][MAX_MAP_SIZE],
                                 int currentPath[][2], int currentPathLength,
                                 int timeLeft,
                                 int dirIndex,
                                 int outPath[][2], int &outPathLength,
                                 int currentSurvivors,
                                 int unlockThreshold,
                                 int &bestPathLength)
{
    // Hint 1: Base case for direction recursion is dirIndex >= 4.
    // Hint 2: Check bounds and recurse into rescueSurvivorsWithPenalty for this branch.
    // Hint 3: Continue exploring all directions to ensure we find the shortest path.
    // Even if we found a valid path, we need to check other branches for potentially shorter ones.
    // TODO: Implement this function

    if (dirIndex >= 4)
        return false;

    if (bestPathLength != 0 && currentPathLength >= bestPathLength)
        return false;

    bool found = false;

    // TRY ONE 
    if (dirIndex == 0)
    {
        // UP
        found = rescueSurvivorsWithPenalty(
            map, rows, cols, targetRow, targetCol,
            r - 1, c, visited,
            currentPath, currentPathLength,
            timeLeft,
            outPath, outPathLength,
            currentSurvivors,
            unlockThreshold,
            bestPathLength);
    }
    else if (dirIndex == 1)
    {
        // DOWN
        found = rescueSurvivorsWithPenalty(
            map, rows, cols, targetRow, targetCol,
            r + 1, c, visited,
            currentPath, currentPathLength,
            timeLeft,
            outPath, outPathLength,
            currentSurvivors,
            unlockThreshold,
            bestPathLength);
    }
    else if (dirIndex == 2)
    {
        // LEFT
        found = rescueSurvivorsWithPenalty(
            map, rows, cols, targetRow, targetCol,
            r, c - 1, visited,
            currentPath, currentPathLength,
            timeLeft,
            outPath, outPathLength,
            currentSurvivors,
            unlockThreshold,
            bestPathLength);
    }
    else if (dirIndex == 3)
    {
        // RIGHT
        found = rescueSurvivorsWithPenalty(
            map, rows, cols, targetRow, targetCol,
            r, c + 1, visited,
            currentPath, currentPathLength,
            timeLeft,
            outPath, outPathLength,
            currentSurvivors,
            unlockThreshold,
            bestPathLength);
    }

    bool foundOther = tryAllDirectionsWithPenalty(
        map, rows, cols, targetRow, targetCol,
        r, c, visited,
        currentPath, currentPathLength,
        timeLeft,
        dirIndex + 1,
        outPath, outPathLength,
        currentSurvivors,
        unlockThreshold,
        bestPathLength);

    return found || foundOther;
}

/**
 * Phase D (Level 3 Maximum Rescue)
 * TODO D1: Recursive rescue with dynamic time cost, threshold check, and best-path update.
 * Note: Kept separate from tryAllDirectionsMax intentionally for recursion decomposition learning.
 */
int rescueSurvivorsMax(int map[][MAX_MAP_SIZE], int rows, int cols,
                       int targetRow, int targetCol,
                       int r, int c, bool visited[][MAX_MAP_SIZE],
                       int currentPath[][2], int currentPathLength,
                       int timeLeft,
                       int bestPath[][2], int &bestPathLength,
                       int &maxSurvivors, int currentSurvivors,
                       int unlockThreshold)
{
    // Hint 1: Prune invalid states first (bounds, time, # cell, visited, path overflow).
    // Hint 2: Record current node, then update rescued survivors.
    // Hint 3: Enforce unlock threshold only when reaching the shelter door.
    // Hint 4: Delegate branch exploration to tryAllDirectionsMax, then backtrack.
    // TODO: Implement this function

   
    // classic check
    if (r < 0 || r >= rows || c < 0 || c >= cols)
        return UNREACHABLE;
    if (map[r][c] == WALL_CELL || visited[r][c])
        return UNREACHABLE;
    if (timeLeft <= 0 || currentPathLength >= MAX_PATH_LENGTH)
        return UNREACHABLE;

    // RECORD CURRENT CELL AND UPDATE SURVIVORS
    visited[r][c] = true;
    currentPath[currentPathLength][0] = r;
    currentPath[currentPathLength][1] = c;
    int newSurvivors = currentSurvivors + map[r][c];

    // IF REACHED TARGET , THEN CHECK THRESHOLD
    if (r == targetRow && c == targetCol) {
        // Only valid if we meet the unlock requirement
        if (newSurvivors >= unlockThreshold) {
            // Update 
            if (newSurvivors > maxSurvivors) {
                maxSurvivors = newSurvivors;
                bestPathLength = currentPathLength + 1;
                copyPathRecursive(currentPath, bestPath, bestPathLength);
            }
            // backtrack before return
            visited[r][c] = false;
            return newSurvivors;
        }

        // not enough survivors
        visited[r][c] = false;
        return UNREACHABLE;
    }

    // DIRECTION HELPER
    int result = tryAllDirectionsMax(
        map, rows, cols,
        targetRow, targetCol,
        r, c, visited,
        currentPath, currentPathLength + 1,
        timeLeft,
        bestPath, bestPathLength,
        0,
        maxSurvivors,
        newSurvivors,
        unlockThreshold
    );

    // BACKTRACK
    visited[r][c] = false;

    return result;

}

/**
 * Phase D (Level 3 Maximum Rescue)
 * TODO D2: Try all four directions and combine branch results.
 * Note: Kept separate from rescueSurvivorsMax intentionally for recursion decomposition learning.
 */
int tryAllDirectionsMax(int map[][MAX_MAP_SIZE], int rows, int cols,
                        int targetRow, int targetCol,
                        int r, int c, bool visited[][MAX_MAP_SIZE],
                        int currentPath[][2], int currentPathLength,
                        int timeLeft,
                        int bestPath[][2], int &bestPathLength,
                        int dirIndex,
                        int &maxSurvivors, int currentSurvivors,
                        int unlockThreshold)
{
    // Hint 1: Direction-recursion base case is when all 4 directions are attempted.
    // Hint 2: Dynamic time cost depends on currently rescued survivors.
    // Hint 3: Recurse current direction, then recurse next direction index.
    // Hint 4: Combine both branch results; preserve the best reachable total.
    // TODO: Implement this function

    // base 
    if (dirIndex >= 4)
        return UNREACHABLE;

    // TIME COST
    int timeCost = 1 + currentSurvivors / 4;
    int newTime = timeLeft - timeCost;
    int currentResult = UNREACHABLE;
    
    if (dirIndex == 0) {
        //  up
        currentResult = rescueSurvivorsMax(
            map, rows, cols, targetRow, targetCol,
            r - 1, c, visited,
            currentPath, currentPathLength,
            newTime,
            bestPath, bestPathLength,
            maxSurvivors, currentSurvivors,
            unlockThreshold
        );
    }
    else if (dirIndex == 1) {
        // down
        currentResult = rescueSurvivorsMax(
            map, rows, cols, targetRow, targetCol,
            r + 1, c, visited,
            currentPath, currentPathLength,
            newTime,
            bestPath, bestPathLength,
            maxSurvivors, currentSurvivors,
            unlockThreshold
        );
    }
    else if (dirIndex == 2) {
        // left
        currentResult = rescueSurvivorsMax(
            map, rows, cols, targetRow, targetCol,
            r, c - 1, visited,
            currentPath, currentPathLength,
            newTime,
            bestPath, bestPathLength,
            maxSurvivors, currentSurvivors,
            unlockThreshold
        );
    }
    else if (dirIndex == 3) {
        //right
        currentResult = rescueSurvivorsMax(
            map, rows, cols, targetRow, targetCol,
            r, c + 1, visited,
            currentPath, currentPathLength,
            newTime,
            bestPath, bestPathLength,
            maxSurvivors, currentSurvivors,
            unlockThreshold
        );
    }

    //  NEXT DIRECTION
    int nextResult = tryAllDirectionsMax(
        map, rows, cols, targetRow, targetCol,
        r, c, visited,
        currentPath, currentPathLength,
        timeLeft,
        bestPath, bestPathLength,
        dirIndex + 1,
        maxSurvivors, currentSurvivors,
        unlockThreshold
    );


    // RETURN THE MAX SURVIVOR COUNT!!!!
    if (currentResult == UNREACHABLE) return nextResult;
    if (nextResult == UNREACHABLE) return currentResult;

    return max(currentResult, nextResult);

}

#endif // HELPERS_H
