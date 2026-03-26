import io
import os.path
import unittest

from map import Map
from game import Game
from tank import Direction, Tank


def decorator__two_message(before=None, after=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                Test42Hidden.addLog(before)
            result = func(*args, **kwargs)
            if after:
                Test42Hidden.addLog(after)
            return result

        return wrapper

    return decorator


def decorator__log_param(before=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                Test42Hidden.addLog(before, end="")
            Test42Hidden.addLog(args)
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def decorator__two_functions(before=None, after=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                before(*args, **kwargs)
            result = func(*args, **kwargs)
            if after:
                after(*args, **kwargs)
            return result

        return wrapper

    return decorator


class Test42Hidden(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = Game("maps/small.txt")

    def setUp(self):
        Test42Hidden.log = ""

    @classmethod
    def tearDownClass(cls):
        cls.game.window.destroy()

    @classmethod
    def addLog(cls, message, end="\n"):
        cls.log += f"{message}{end}"

    def test_reset__stop_all_directions_boundary_hidden(self):
        # Boundary test: ensure each tank receives exactly one stop_tank call per direction
        tank_calls = {}

        def make_stop_recorder(tank_id):
            def record(direction):
                tank_calls[tank_id][direction] = tank_calls[tank_id].get(direction, 0) + 1
            return record

        # Patch stop_tank for both tanks
        for tank in Test42Hidden.game.tanks:
            tank_calls[tank.tank_id] = {}
            original = tank.stop_tank
            recorder = make_stop_recorder(tank.tank_id)
            tank.stop_tank = decorator__two_functions(recorder)(original)

        Test42Hidden.game.reset_game()

        # Expected: each tank should have been stopped exactly once in all 4 directions
        expected = {Direction.N: 1, Direction.S: 1, Direction.W: 1, Direction.E: 1}

        for tid in (0, 1):
            self.assertEqual(tank_calls[tid], expected)

    def test_reset__order_hidden(self):
        Test42Hidden.game.bind_keys, or_bk = (
            decorator__two_message("GameTest.game.bind_keys()")(
                Test42Hidden.game.bind_keys
            ),
            Test42Hidden.game.bind_keys,
        )
        Test42Hidden.game.unbind_keys, or_uk = (
            decorator__two_message("GameTest.game.unbind_keys()")(
                Test42Hidden.game.unbind_keys
            ),
            Test42Hidden.game.unbind_keys,
        )
        Map.draw_on, omr_do = (
            decorator__two_message("draw_on()")(Map.draw_on),
            Map.draw_on,
        )
        Tank.draw_on, otr_do = (
            decorator__two_message("draw_on()")(Tank.draw_on),
            Tank.draw_on,
        )

        Test42Hidden.game.reset_game()

        self.assertEqual(
            Test42Hidden.log,
            "GameTest.game.unbind_keys()\nGameTest.game.bind_keys()\ndraw_on()\ndraw_on()\ndraw_on()\n",
        )

        Test42Hidden.game.bind_keys = or_bk
        Test42Hidden.game.unbind_keys = or_uk
        Map.draw_on = omr_do
        Tank.draw_on = otr_do

    def test_reset__new_tanks_hidden(self):
        Test42Hidden.game.map_file = "maps/test_4_2_hidden.txt"
        Test42Hidden.game.reset_game()

        self.assertEqual(len(Test42Hidden.game.tanks), 2)

        for tank_id in range(2):
            for i in range(3):
                if i == 2:
                    self.fail("Missing a tank")
                if Test42Hidden.game.tanks[i].tank_id == tank_id:
                    tank: Tank = Test42Hidden.game.tanks[i]
                    if tank_id == 0:
                        self.assertEqual(tank.x, 0.5)
                        self.assertEqual(tank.y, 2.5)
                    else:
                        self.assertEqual(tank.x, 2.5)
                        self.assertEqual(tank.y, 0.5)
                    break

        Test42Hidden.game.map_file = "maps/small.txt"


    def test_reset__tanks_reinitialized_positions_match_map(self):
        # Ensures new tanks after reset match the positions defined by the map
        Test42Hidden.game.map_file = "maps/test_4_2_hidden.txt"
        Test42Hidden.game.reset_game()

        expected_positions = list(Test42Hidden.game.map.tank_position_map.items())
        actual_positions = [(tank.tank_id, (tank.x, tank.y)) for tank in Test42Hidden.game.tanks]

        for tank_id, (expected_x, expected_y) in expected_positions:
            found = False
            for tid, (ax, ay) in actual_positions:
                if tid == tank_id:
                    self.assertAlmostEqual(ax, expected_x)
                    self.assertAlmostEqual(ay, expected_y)
                    found = True
            if not found:
                self.fail(f"Tank {tank_id} missing after reset.")


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test42Hidden."
    tests = list(filter(lambda _: _.startswith("test"), Test42Hidden.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test42Hidden)
    result = unittest.TextTestRunner(stream=temp_stream, verbosity=1).run(suite)
    match result.wasSuccessful(), test_num:
        case True, -1:
            print(f"All tests of {file_name} passed.")
        case False, -1:
            print(f"Some or all tests of {file_name} failed. Details:\n" + temp_stream.getvalue())
        case True, _:
            print(f"Test \"{tests[test_num]}\" passed.")
        case False, _:
            print(f"Test \"{tests[test_num]}\" failed. Details:\n" + temp_stream.getvalue())

if __name__ == "__main__":
    main()
