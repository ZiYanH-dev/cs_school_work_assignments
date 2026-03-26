import io
import os.path
import unittest
from tkinter import Tk

from map import Map


class Test22Hidden(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_collides_with_tank__engulf(self):
        # Object much larger than tank, completely containing it
        game_map = Map(5, 5)
        game_map.tank_position_map[0] = (2.5, 2.5)
        game_map.tank_position_map[1] = (1, 1)
        
        # Object center 2.5, 2.5, size 3x3
        # Tank is 1x1 at 2.5, 2.5
        res = game_map.collides_with_tank(2.5, 2.5, 3, 3)
        self.assertEqual(res, 0)

    def test_collides_with_tank__nearby_but_miss(self):
        # Two tanks. Object hits near one but misses both.
        game_map = Map(5, 5)
        game_map.tank_position_map[0] = (1.5, 1.5)
        game_map.tank_position_map[1] = (3.5, 1.5)
        
        # Object at 2.5, 1.5 with size 0.9
        # Tank 0 range x: [1.0, 2.0]
        # Tank 1 range x: [3.0, 4.0]
        # Object range x: [2.05, 2.95]
        # Misses both (2.0 < 2.05 and 2.95 < 3.0)
        res = game_map.collides_with_tank(2.5, 1.5, 0.9, 0.9)
        self.assertIsNone(res)

    def test_collides_with_tank__touching_edge(self):
        # Tank at 1.5, 1.5 (extends x: [1.0, 2.0])
        game_map = Map(5, 5)
        game_map.tank_position_map[0] = (4, 4)
        game_map.tank_position_map[1] = (1.5, 1.5)
        
        # Object at 0.5, 1.5 with width 1.0 (extends x: [0.0, 1.0])
        # Touching edge x=1.0. Should collide (inclusive).
        res = game_map.collides_with_tank(0.5, 1.5, 1.0, 1.0)
        self.assertEqual(res, 1)

    def test_collides_with_tank__no_collision(self):
        game_map = Map(10, 10)
        game_map.tank_position_map[0] = (5, 5)
        game_map.tank_position_map[1] = (8.5, 5.7)
        # No collision
        res = game_map.collides_with_tank(1.5, 1.5, 1, 1)
        self.assertIsNone(res)

    def test_collides_with_tank__collide(self):
        # Verify it returns correct ID for different tanks
        game_map = Map(5, 5)
        game_map.tank_position_map[0] = (1.5, 1.5)
        game_map.tank_position_map[1] = (3.5, 3.5)
        
        self.assertEqual(game_map.collides_with_tank(1.5, 1.5, 0.5, 0.5), 0)
        self.assertEqual(game_map.collides_with_tank(3.5, 3.5, 0.5, 0.5), 1)


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test22Hidden."
    tests = list(filter(lambda _: _.startswith("test"), Test22Hidden.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test22Hidden)
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

