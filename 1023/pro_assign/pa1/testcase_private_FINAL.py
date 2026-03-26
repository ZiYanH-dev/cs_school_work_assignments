
#
# in zinc yaml, need normalise scores
#
# from game.py import *
# task 1: init_gameboard()
# task 2: default_random_number_generator()
# task 3: is_valid_move()
# task 4: move_left()
# task 5: move_right()
# task 6: move_down()
# task 7: rotate()
# task 8: gravity_and_merge()
# task 9: rotate()

PRINT_INPUT_PARAMETERS_ONLY = False
PRINT_OUTPUT_PARAMETERS_ONLY = False
import random
random.seed(50)

from copy import deepcopy
#from game import *
from game import *

cases = []
func = ["init_gameboard",
        "default_random_number_generator",
        "is_valid_move",
        "move_left",
        "move_right",
        "move_down",
        "rotate",
        "gravity_and_merge: merge",
        "gravity_and_merge: gravity",
        "get_game_status",
        "rotate",
        "gravity_and_merge: merge",
        "gravity_and_merge: merge",
        "gravity_and_merge: merge",
        "gravity_and_merge: merge",
        "gravity_and_merge: merge",
        "gravity_and_merge: merge",
        "get_game_status",
        "get_game_status",
        "get_game_status"
]
cases.append("COMP1023 PA1")
for f in func:
    cases.append(f)

def run_test(testcase):

    match testcase:
        case 1:
            answer = [[0] * 6 for _ in range(20)]
            msg = "Game board test. After game_board initialisation, re-assign game_board[5][5]=1 and game_board[0][2] = 2."
            try:
                output = init_gameboard()
                output_original = deepcopy(output)
                answer_original = deepcopy(answer)
                output[5][5] = 1
                output[0][2] = 2
                answer[5][5] = 1
                answer[0][2] = 2
                if PRINT_OUTPUT_PARAMETERS_ONLY:
                    print(f"{msg}, {cases[int(testcase)]}(). Correct output: {answer}")
                if output_original == answer_original:
                    try:
                        if output == answer:
                            print(msg,"Correct.")
                        else:
                            print(f"{msg} Wrong. Output from program is:\n{output_original}. After reassigning output[5][5] = 1 and output[0][2] = 2, game board becomes {output}.\nCorrect answer should be: \n{answer}.")    
                    except Exception as e:
                        print(f"{cases[int(testcase)]}() Runtime error: {e} when reassigning variables in gameboard.")        
                else:
                    print(f"{msg} Wrong. Output from program is:\n{output}. \nCorrect answer should be: \n{answer}.")
            except Exception as e:
                print(f"{cases[int(testcase)]}() Runtime error: {e}.")
        
        case 2:
            possible = [1, 3, 7, 15, 31, 63, 127, 255]
            number_of_tests = 1000
            numbers = []
            msg = "Random number generator test."
            # assume all possible numbers are generated at least once in correct implementation
            try:
                for i in range(number_of_tests):
                    numbers.append(default_random_number_generator())
                if PRINT_OUTPUT_PARAMETERS_ONLY:
                    print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nOutput: {numbers}")
                if set(numbers) != set(possible) and len(set(numbers)) < len(set(possible)):
                    print(f"{msg} Wrong. {number_of_tests} numbers generated from function are: {numbers}. Certain number(s) is/are missing if using proper random number generator.")
                elif set(numbers) != set(possible):
                    print(f"{msg} Wrong. {number_of_tests} numbers generated from function are: {numbers}. The correct set of numbers is: {possible}.")
                else:
                    counter = []
                    for p in possible:
                        counter.append(numbers.count(p))
                    small_occurence = counter[0] + counter[1] + counter[2] + counter[3]
                    large_occurence = counter[4] + counter[5] + counter[6] + counter[7]
                    counter_error = False
                    for i in range(len(counter)):
                            if counter[i] > number_of_tests * 0.4:
                                counter_error = True
                                break
                    if counter_error:
                        print(f"Wrong. Certain numbers appear to have too high occurrences. Possible random number generator incorrect implementation.. Count of occurences of each of the possible numbers are: {counter}")

                    elif small_occurence > large_occurence:
                        print(msg,"Correct.")
                    else:
                        print(f"Wrong. Count of occurences of each of the possible numbers are: {counter} and average of the occurences of the smaller four numbers are not more than the average of the larger four numbers.")
            except Exception as e:
                print(f"{cases[int(testcase)]}() Runtime error: {e}.")

        case 3:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [0,0]
            rotation = 0    # 0 to 3
            try:
                tests.append([game_board,shape,location,rotation, is_valid_move(game_board,shape,location,rotation), True, "Top side ok test."])
                number_of_tests += 1
                
                rotation = 1
                tests.append([game_board,shape,location,rotation,is_valid_move(game_board,shape,location,rotation),False,"Top side exceeded test."])
                number_of_tests += 1

                rotation = 0
                location = [0,2]
                tests.append([game_board,shape,location,rotation,is_valid_move(game_board,shape,location,rotation),True,"Right side ok test."])
                number_of_tests += 1

                location = [0,3]
                tests.append([game_board,shape,location,rotation,is_valid_move(game_board,shape,location,rotation),False,"Right side exceeded test."])
                number_of_tests += 1

                location = [0,0]
                tests.append([game_board,shape,location,rotation,is_valid_move(game_board,shape,location,rotation),True,"Left side ok test."])
                number_of_tests += 1

                location = [0,-1]
                tests.append([game_board,shape,location,rotation,is_valid_move(game_board,shape,location,rotation),False,"Left side exceeded test."])
                number_of_tests += 1

                location = [19,0]
                tests.append([game_board,shape,location,rotation,is_valid_move(game_board,shape,location,rotation),True,"Bottom side ok test."])
                number_of_tests += 1

                rotation = 1
                tests.append([game_board,shape,location,rotation,is_valid_move(game_board,shape,location,rotation),False,"Bottom side exceeded test."])
                number_of_tests += 1

                for i in range(5,20): 
                    for j in range(6):
                        game_board[i][j] = 1
                #print(game_board, len(game_board))

                location = [3,2]
                tests.append([game_board,shape,location,rotation,is_valid_move(game_board,shape,location,rotation),True,"Block not overlap test."])
                number_of_tests += 1

                location = [4,2]
                tests.append([game_board,shape,location,rotation,is_valid_move(game_board,shape,location,rotation),False,"Block overlap test."])
                number_of_tests += 1
                
                for i in range(number_of_tests):
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6], "Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
                    # print(tests[i][1:])
            except Exception as e:
                print(f"{cases[int(testcase)]}() Runtime error: {e}.")

        case 4:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [0,1]
            rotation = 0    # 0 to 3

            try:
                tests.append([game_board,shape,location,rotation, move_left(game_board,shape,location,rotation), ([0,0],0), "Move left ok test."])
                number_of_tests += 1
                
                location = [0,0]
                tests.append([game_board,shape,location,rotation, move_left(game_board,shape,location,rotation), ([0,0],0), "Move left not ok test."])
                number_of_tests += 1

                for i in range(number_of_tests):
                    #print(tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6], "Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                print(f"{cases[int(testcase)]}() Runtime error: {e}.")

        case 5:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [0,1]
            rotation = 0    # 0 to 3
            
            try:
                tests.append([game_board,shape,location,rotation, move_right(game_board,shape,location,rotation), ([0,2],0), "Move right ok test."])
                number_of_tests += 1
                
                location = [0,2]
                tests.append([game_board,shape,location,rotation, move_right(game_board,shape,location,rotation), ([0,2],0), "Move right not ok test."])
                number_of_tests += 1
                
                for i in range(number_of_tests):
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")    
                    if tests[i][4] == tests[i][5]:
                            print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                print(f"{cases[int(testcase)]} Runtime error: {e}.")

        case 6:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [18,1]
            rotation = 0    # 0 to 3

            try:
                tests.append([game_board,shape,location,rotation, move_down(game_board,shape,location,rotation), ([19,1],0), "Move down ok test."])
                number_of_tests += 1
                
                location = [19,1]
                tests.append([game_board,shape,location,rotation, move_down(game_board,shape,location,rotation), ([19,1],0), "Move down not ok test."])
                number_of_tests += 1
                
                for i in range(number_of_tests):
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                print(f"{cases[int(testcase)]} Runtime error: {e}.")

        case 7:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3

            try:
                tests.append([game_board,shape,location,rotation, rotate(game_board,shape,location,rotation), ([2,1],1), "Rotate ok test."])
                number_of_tests += 1
                
                location = [0,1]
                rotation = 0
                tests.append([game_board,shape,location,rotation, rotate(game_board,shape,location,rotation), ([0,1],0), "Rotate not ok test."])
                number_of_tests += 1
                
                for i in range(number_of_tests):
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[{int(testcase)}]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                print(f"{cases[int(testcase)]} Runtime error: {e}.")

        case 8:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3

            try:
                correct_game_board = deepcopy(game_board)
                for i in range(19,19-4,-1):
                    game_board[i][2] = 255
                correct_game_board[19][2] = 1023
                original_game_board = deepcopy(game_board)

                gravity_and_merge(game_board)
                tests.append([original_game_board,shape,location,rotation, game_board, correct_game_board, cases[8]+" test."])
                number_of_tests += 1

                for i in range(number_of_tests):
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")

            except Exception as e:
                print(f"{cases[int(testcase)]} Runtime error: {e}.")

        case 9:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3

            try:
                correct_game_board = deepcopy(game_board)
                for i in range(4):
                    game_board[2][i] = 63 
                    correct_game_board[19][i] = 63
                original_game_board = deepcopy(game_board)
                gravity_and_merge(game_board)
                tests.append([original_game_board,shape,location,rotation, game_board, correct_game_board, cases[9]+" test."])
                number_of_tests += 1
                for i in range(number_of_tests):
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")

            except Exception as e:
                print(f"{cases[int(testcase)]} Runtime error: {e}.")
        case 10:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3

            try:
                empty_game_board = deepcopy(game_board)
                for i in range(4):
                    game_board[4][i] = 63 
                tests.append([game_board,shape,location,rotation, get_game_status(game_board), "Lose", cases[int(testcase)]+" test. Lose."])
                number_of_tests += 1

                game_board = deepcopy(empty_game_board)
                for i in range(4):
                    game_board[19][i] = 63 
                tests.append([game_board,shape,location,rotation, get_game_status(game_board), "Playing", cases[int(testcase)]+" test. Playing."])
                number_of_tests += 1

                game_board = deepcopy(empty_game_board)
                game_board[19][5] = 1023
                tests.append([game_board,shape,location,rotation, get_game_status(game_board), "Win", cases[int(testcase)]+" test. Win."])
                number_of_tests += 1
                for i in range(number_of_tests):
                    #print(i,tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print(f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")            
        case 11:
            shapes = [
                # shape 0: ****
                [
                    [(0, 0), (0, 1), (0, 2), (0, 3)],
                    [(1, 1), (0, 1), (-1, 1), (-2, 1)],
                    [(0, 3), (0, 2), (0, 1), (0, 0)],
                    [(-2, 1), (-1, 1), (0, 1), (1, 1)],
                ],
                # shape 1
                # **
                # **
                [
                    [(0, 0), (0, 1), (1, 0), (1, 1)],
                    [(0, 1), (1, 1), (0, 0), (1, 0)],
                    [(1, 1), (1, 0), (0, 1), (0, 0)],
                    [(1, 0), (0, 0), (1, 1), (0, 1)],
                ],
                # shape 2
                # *
                # ***
                [
                    [(0, 0), (1, 0), (1, 1), (1, 2)],
                    [(1, 0), (1, 1), (0, 1), (-1, 1)],
                    [(1, 2), (0, 2), (0, 1), (0, 0)],
                    [(-1, 2), (-1, 1), (0, 1), (1, 1)],
                ],
                # shape 3
                #   *
                # ***
                [
                    [(1, 0), (1, 1), (1, 2), (0, 2)],
                    [(1, 1), (0, 1), (-1, 1), (-1, 0)],
                    [(0, 2), (0, 1), (0, 0), (1, 0)],
                    [(-1, 1), (0, 1), (1, 1), (1, 2)],
                ],
                # shape 4
                #  **
                # **
                [
                    [(1, 0), (1, 1), (0, 1), (0, 2)],
                    [(1, 1), (0, 1), (0, 0), (-1, 0)],
                    [(0, 2), (0, 1), (1, 1), (1, 0)],
                    [(-1, 0), (0, 0), (0, 1), (1, 1)],
                ],
                # shape 5
                # **
                #  **
                [
                    [(0, 0), (0, 1), (1, 1), (1, 2)],
                    [(1, 1), (0, 1), (0, 2), (-1, 2)],
                    [(1, 2), (1, 1), (0, 1), (0, 0)],
                    [(-1, 2), (0, 2), (0, 1), (1, 1)],
                ],
                # shape 6
                #  *
                # ***
                [
                    [(0, 1), (1, 0), (1, 1), (1, 2)],
                    [(0, 0), (1, 1), (0, 1), (-1, 1)],
                    [(1, 1), (0, 2), (0, 1), (0, 0)],
                    [(0, 2), (-1, 1), (0, 1), (1, 1)],
                ],
            ]

            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3

            try:
                rotation = 3
                tests.append([game_board,shape,location,rotation, rotate(game_board,shape,location,rotation), ([2,
                1],0), "Rotate modulo 4 ok test."])
                number_of_tests += 1
                
                location = [2,4]
                rotation = 3
                tests.append([game_board,shape,location,rotation, rotate(game_board,shape,location,rotation), ([2,4],3), "Rotate modulo 4 not ok test."])
                number_of_tests += 1

                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                print (f"{cases[int(testcase)]} Runtime error: {e}.")
        case 12:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3

            try:
                correct_game_board = deepcopy(game_board)
                for i in range (19,19-2,-1):
                    game_board[i][3] = 1
                correct_game_board[19][3] = 3
                original_game_board = deepcopy(game_board)
                gravity_and_merge(game_board)
                tests.append([original_game_board,shape,location,rotation, game_board, correct_game_board, "Gravity and merge test."])
                number_of_tests += 1
                #print(game_board)
                #print (f"game_board:{game_board}")
                #print (f"correct: {correct_game_board}")
                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[(int(testcase))]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")            
        case 13:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3

            try:
                game_board = [[0] * 6 for _ in range(20)]
                correct_game_board = deepcopy(game_board)
                for i in range (19,19-3,-1):
                    game_board[i][4] = 3
                correct_game_board[19][4] = 7
                correct_game_board[18][4] = 3
                original_game_board = deepcopy(game_board)
                gravity_and_merge(game_board)
                tests.append([original_game_board,shape,location,rotation, game_board, correct_game_board, "Gravity and merge test."])
                number_of_tests += 1
                #print(game_board)
                #print (f"game_board:{game_board}")
                #print (f"correct: {correct_game_board}")
                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[(int(testcase))]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")
        case 14:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3
            try:
                game_board = [[0] * 6 for _ in range(20)]
                correct_game_board = deepcopy(game_board)
                for i in range (19,19-2,-1):
                    game_board[i][5] = 7
                correct_game_board[19][5] = 15
                for i in range (19,19-3,-1):
                    game_board[i][0] = 31
                correct_game_board[19][0] = 63
                correct_game_board[18][0] = 31
                for i in range (19,19-4,-1):
                    game_board[i][1] = 127
                correct_game_board[19][1] = 511
                before_game_board = deepcopy(game_board)
                gravity_and_merge(game_board)
                tests.append([before_game_board,shape,location,rotation, game_board, correct_game_board, "Gravity and merge test."])
                number_of_tests += 1
                #print(game_board)
                #print (f"game_board:{game_board}")
                #print (f"correct: {correct_game_board}")
                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[(int(testcase))]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")
        case 15:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3
            try:
                game_board = [[0] * 6 for _ in range(20)]
                correct_game_board = deepcopy(game_board)
                possible = [1, 3, 7, 15, 31, 63, 127, 255] 
                for i in range (18,18-len(possible),-1):
                    game_board[i][5] = possible[i-19]
                game_board[10][5] = 1
                game_board[19][5] = 511
                correct_game_board[19][5] = 1023
                #print (f"game_board: {game_board}")
                #print (f"correct game_board: {correct_game_board}")
                before_game_board = deepcopy(game_board)
                gravity_and_merge(game_board)
                tests.append([before_game_board,shape,location,rotation, game_board, correct_game_board, "Gravity and merge test."])
                number_of_tests += 1
                #print(game_board)
                #print (f"game_board:{game_board}")
                #print (f"correct: {correct_game_board}")
                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[(int(testcase))]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")
        case 16:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3
            try:
                game_board = [[0] * 6 for _ in range(20)]
                correct_game_board = deepcopy(game_board)
                possible = [1, 3, 7, 15, 31, 63, 127, 255] 
                for i in range (6):
                    game_board[0][i] = possible[i]
                    correct_game_board[19][i] = possible[i]
                #rint (f"game_board: {game_board}")
                #rint (f"correct game_board: {correct_game_board}")
                before_game_board = deepcopy(game_board)
                gravity_and_merge(game_board)
                tests.append([before_game_board,shape,location,rotation, game_board, correct_game_board, "Gravity and merge test."])
                number_of_tests += 1
                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[(int(testcase))]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")
        case 17:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3
            try:
                game_board = [[0] * 6 for _ in range(20)]
                correct_game_board = deepcopy(game_board)
                possible = [1, 3, 7, 15, 31, 63, 127, 255] 
                for i in range (6):
                    game_board[0][i] = possible[-i-1]
                    correct_game_board[19][i] = possible[-i-1]
                #print (f"game_board: {game_board}")
                #print (f"correct game_board: {correct_game_board}")
                before_game_board = deepcopy(game_board)
                gravity_and_merge(game_board)
                tests.append([before_game_board,shape,location,rotation, game_board, correct_game_board, "Gravity and merge test."])
                number_of_tests += 1
                #print(game_board)
                #print (f"game_board:{game_board}")
                #print (f"correct: {correct_game_board}")
                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[(int(testcase))]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")
        case 18:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3
            try:
                empty_game_board = deepcopy(game_board)
                for i in range (4):
                    game_board[i+4][2] = 63 
                for i in range(6):
                     game_board[19][i] = 1023
                tests.append([game_board,shape,location,rotation, get_game_status(game_board), "Lose", cases[int(testcase)]+" test. Lose."])
                number_of_tests += 1
                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")        
        case 19:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3
            try:
                empty_game_board = deepcopy(game_board)
                possible = [1, 3, 7, 15, 31, 63, 127, 255] 
                k = 0
                for i in range (19-5):
                    for j in range (6):
                        game_board[i+5][j] = possible[k % len(possible)]
                        k += 1
                #print (f"game_board:{game_board}")
                tests.append([game_board,shape,location,rotation, get_game_status(game_board), "Playing", cases[int(testcase)]+" test. Playing."])
                number_of_tests += 1
                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")        
        case 20:
            number_of_tests = 0
            tests = []
            game_board = [[0] * 6 for _ in range(20)]
            shape = 0       # 0 to 6
            location = [2,1]
            rotation = 0    # 0 to 3
            try:
                empty_game_board = deepcopy(game_board)
                for i in range (6):
                    game_board[17][i] = 1023
                    game_board[18][i] = 63
                    game_board[19][i] = 127
                #print (f"game_board:{game_board}")
                tests.append([game_board,shape,location,rotation, get_game_status(game_board), "Win", cases[int(testcase)]+" test. Win."])
                number_of_tests += 1
                for i in range(number_of_tests):
                    #print (tests[i][1:])
                    if PRINT_INPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} input parameters are game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}")
                    if PRINT_OUTPUT_PARAMETERS_ONLY:
                        print (f"Testcase {int(testcase)} testing function {cases[int(testcase)]}.\nTest {i} correct output: {tests[i][5]}")
                    if tests[i][4] == tests[i][5]:
                        print(tests[i][6],"Correct.")
                    else:
                        if not PRINT_INPUT_PARAMETERS_ONLY:
                            print(f"{tests[i][6]} Wrong. game_board: {tests[i][0]}, shape: {tests[i][1]}, location: {tests[i][2]}, rotation: {tests[i][3]}, function output: {tests[i][4]}. Correct answer: {tests[i][5]}")
            except Exception as e:
                            print (f"{cases[int(testcase)]} Runtime error: {e}.")        


if __name__ == "__main__":
    #testcase = int(input())
    #run_test(testcase)
    


    for testcase in range(1,20+1):
        print (f"testcase {testcase}:")
        run_test(testcase)
