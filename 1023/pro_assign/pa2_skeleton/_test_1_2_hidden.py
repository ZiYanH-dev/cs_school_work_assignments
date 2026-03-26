import io
import os.path
import unittest
from tkinter import Tk
import numpy as np

from map import Map, Tile


class Test12Hidden(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_map_diff__multiple_changes(self):
        # Test changing multiple dispersed tiles
        game_map = Map(4, 4)
        # Initial call to set prev_map
        game_map.map_diff()
        
        # Change multiple tiles
        game_map.map[0][0] = Tile.ROCK
        game_map.map[1][1] = Tile.BOMB
        game_map.map[3][3] = Tile.ROCK
        
        diff = game_map.map_diff()
        
        expected = np.zeros((4, 4), dtype=bool)
        expected[0][0] = True
        expected[1][1] = True
        expected[3][3] = True
        
        np.testing.assert_array_equal(diff, expected)

    def test_map_diff__full_change(self):
        # Test changing every single tile
        game_map = Map(2, 2)
        game_map.map_diff() # Initialize prev_map
        
        # Change all
        game_map.map[:] = Tile.ROCK
        
        diff = game_map.map_diff()
        expected = np.full((2, 2), True)
        
        np.testing.assert_array_equal(diff, expected)

    def test_map_diff__sequential_updates(self):
        # Test a sequence of updates
        game_map = Map(3, 3)
        game_map.map_diff() # Init
        
        # Step 1: Change one tile
        game_map.map[0][0] = Tile.ROCK
        diff1 = game_map.map_diff()
        self.assertTrue(diff1[0][0])
        self.assertFalse(diff1[0][1])
        
        # Step 2: Revert that change (should still be a diff from *previous* state)
        game_map.map[0][0] = Tile.EMPTY
        diff2 = game_map.map_diff()
        self.assertTrue(diff2[0][0]) # Changed back
        self.assertFalse(diff1[0][1])
        
        # Step 3: No change
        diff3 = game_map.map_diff()
        self.assertFalse(np.any(diff3))

    def test_map_diff__rectangular_shape(self):
        # Test with non-square map
        # 2 rows, 5 cols
        game_map = Map(5, 2)
        game_map.map_diff()
        
        game_map.map[1][4] = Tile.BOMB
        diff = game_map.map_diff()
        
        self.assertEqual(diff.shape, (2, 5))
        self.assertTrue(diff[1][4])
        self.assertFalse(diff[0][0])

    def test_map_diff__2x1_shape(self):
        # Boundary: 2x1 map
        game_map = Map(2, 1)
        diff_init = game_map.map_diff()
        self.assertTrue(diff_init[0][0])
        self.assertTrue(diff_init[0][1])
        
        game_map.map[0][0] = Tile.ROCK
        diff_change = game_map.map_diff()
        self.assertTrue(diff_change[0][0])
        self.assertFalse(diff_change[0][1])
        
        diff_no_change = game_map.map_diff()
        self.assertFalse(diff_no_change[0][0])
        self.assertFalse(diff_no_change[0][1])


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test12Hidden."
    tests = list(filter(lambda _: _.startswith("test"), Test12Hidden.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test12Hidden)
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

