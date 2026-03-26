import io
import os.path
import unittest
from tkinter import Tk
import numpy as np

from map import Map, Tile


class Test21Hidden(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_collides__large_object_outside(self):
        # Object larger than map, so it must be outside
        # Map 2x2
        game_map = Map(2, 2)
        # Center at (1, 1), size 4x4 -> x spans -1 to 3.
        # Boundary checks should catch this.
        res = game_map.collides(1, 1, 4, 4)
        self.assertIsNone(res)

    def test_collides__mixed_obstacles(self):
        # 2x2 map:
        # ROCK BOMB
        # .    .
        game_map = Map(2, 2)
        game_map.map[0][0] = Tile.ROCK
        game_map.map[0][1] = Tile.BOMB
        
        # Object overlaps both top tiles
        # Center (1, 0.5), width 1.5, height 0.5
        # x: 1-0.75=0.25 to 1+0.75=1.75. Covers part of col 0 and col 1.
        # y: 0.5-0.25=0.25 to 0.5+0.25=0.75. Covers part of row 0.
        res = game_map.collides(1, 0.5, 1.5, 0.5)
        
        # Should find both
        expected = {
            (0, 0): Tile.ROCK,
            (1, 0): Tile.BOMB
        }
        self.assertEqual(res, expected)

    def test_collides__boundary_precedence_complex(self):
        # Object overlaps a rock BUT is also partially out of bounds.
        # Should return None (boundary check takes precedence).
        game_map = Map(3, 3)
        game_map.map[0][0] = Tile.ROCK
        
        # Object at (-0.1, 0.5) with size 1
        # x: -0.6 to 0.4 (Outside because x1 < 0)
        # y: 0 to 1 (Overlaps (0,0))
        res = game_map.collides(-0.1, 0.5, 1, 1)
        self.assertIsNone(res)

    def test_collides__long_thin_object(self):
        # Long thin object crossing multiple tiles
        game_map = Map(5, 1)
        game_map.map[0][1] = Tile.ROCK
        game_map.map[0][3] = Tile.BOMB
        
        # Crosses whole map horizontally
        # Center (2.5, 0.5), width 4.8, height 0.1
        # x: 0.01 to 4.99
        # y: 0.45 to 0.55
        res = game_map.collides(2.5, 0.5, 4.98, 0.1)
        expected = {
            (1, 0): Tile.ROCK,
            (3, 0): Tile.BOMB
        }
        self.assertEqual(res, expected)

    def test_collides__exact_fit_inside(self):
        # Object fitting exactly inside the map [0, cols]x[0, rows]
        # Should be None (invalid).
        game_map = Map(2, 2)
        res = game_map.collides(1, 1, 2, 2) # x: 0 to 2, y: 0 to 2
        self.assertEqual(res, None)


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test21Hidden."
    tests = list(filter(lambda _: _.startswith("test"), Test21Hidden.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test21Hidden)
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

