import io
import os.path
import unittest
from tkinter import Tk

from map import Tile, create_map


class Test11Hidden(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_read_from__size_4_4_modified(self):
        # Modified size and positions
        game_map = create_map("0 . . .\n" ". # . .\n" ". . @ .\n" "1 . . .\n")
        self.assertEqual(game_map.cols, 4)
        self.assertEqual(game_map.rows, 4)
        self.assertEqual(game_map.map[1][1], Tile.ROCK)
        self.assertEqual(game_map.map[2][2], Tile.BOMB)
        self.assertEqual(game_map.tank_position_map[0], (0.5, 0.5))
        self.assertEqual(game_map.tank_position_map[1], (0.5, 3.5))

    def test_read_from__size_2_1(self):
        # Boundary: Single tile map
        game_map = create_map("0\n" "1\n")
        self.assertEqual(game_map.cols, 1)
        self.assertEqual(game_map.rows, 2)
        self.assertEqual(game_map.map[0][0], Tile.EMPTY)
        self.assertEqual(game_map.map[1][0], Tile.EMPTY)
        self.assertEqual(game_map.tank_position_map[0], (0.5, 0.5))
        self.assertEqual(game_map.tank_position_map[1], (0.5, 1.5))

    def test_read_from__size_1_5(self):
        # Boundary: 1 row multiple columns
        game_map = create_map("0 . # @ 1\n")
        self.assertEqual(game_map.cols, 5)
        self.assertEqual(game_map.rows, 1)
        self.assertEqual(game_map.map[0][2], Tile.ROCK)
        self.assertEqual(game_map.map[0][3], Tile.BOMB)
        self.assertEqual(game_map.tank_position_map[1], (4.5, 0.5))

    def test_read_from__size_5_1(self):
        # Boundary: Multiple rows 1 column
        game_map = create_map("0\n.\n#\n@\n1\n")
        self.assertEqual(game_map.cols, 1)
        self.assertEqual(game_map.rows, 5)
        self.assertEqual(game_map.map[2][0], Tile.ROCK)
        self.assertEqual(game_map.map[3][0], Tile.BOMB)
        self.assertEqual(game_map.tank_position_map[0], (0.5, 0.5))
        self.assertEqual(game_map.tank_position_map[1], (0.5, 4.5))

    def test_read_from__tank_edges(self):
        # Boundary: Tanks at different corners
        # 0 at top-right, 1 at bottom-left
        game_map = create_map(". 0\n1 .\n")
        self.assertEqual(game_map.cols, 2)
        self.assertEqual(game_map.rows, 2)
        self.assertEqual(game_map.tank_position_map[0], (1.5, 0.5))
        self.assertEqual(game_map.tank_position_map[1], (0.5, 1.5))

    def test_read_from__complex_content(self):
        # Mixed content
        map_str = (
            "# @ # @\n"
            "@ # @ #\n"
            "0 . . 1\n"
        )
        game_map = create_map(map_str)
        self.assertEqual(game_map.cols, 4)
        self.assertEqual(game_map.rows, 3)
        self.assertEqual(game_map.map[0][0], Tile.ROCK)
        self.assertEqual(game_map.map[0][1], Tile.BOMB)
        self.assertEqual(game_map.map[1][0], Tile.BOMB)
        self.assertEqual(game_map.map[1][1], Tile.ROCK)
        self.assertEqual(game_map.tank_position_map[0], (0.5, 2.5))
        self.assertEqual(game_map.tank_position_map[1], (3.5, 2.5))


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test11Hidden."
    tests = list(filter(lambda _: _.startswith("test"), Test11Hidden.__dict__.keys()))
    append_len = len(tests) // 10
    prompt = f"{0:{append_len}}: All tests\n" + "\n".join([f"{i + 1:{append_len}}: {j}" for i, j in enumerate(tests)]) + "\nEnter a test number: "

    test_num = None
    while test_num is None:
        try:
            if interactive:
                test_num = int(input(prompt)) - 1
            else:
                test_num = -1
            if test_num < -1 or test_num >= len(tests):
                raise ValueError
        except ValueError:
            print("Invalid input.")
            test_num = None

    temp_stream = io.StringIO()
    if test_num != -1:
        suite = unittest.TestLoader().loadTestsFromName(name + tests[test_num])
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test11Hidden)
    result = unittest.TextTestRunner(stream=temp_stream, verbosity=1).run(suite)
    match result.wasSuccessful(), test_num:
        case True, -1:
            print(f"All tests of {file_name} passed.")
        case False, -1:
            print(f"Some or all tests of {file_name} failed. Details:\n" + temp_stream.getvalue())
        case True, n:
            print(f"Test \"{tests[n]}\" passed.")
        case False, n:
            print(f"Test \"{tests[n]}\" failed. Details:\n" + temp_stream.getvalue())

if __name__ == "__main__":
    main()

