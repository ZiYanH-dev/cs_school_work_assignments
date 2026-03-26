import io
import os
import unittest
from unittest.mock import MagicMock

from map import Tile, Map
from game import Game
from tank import Tank


def decorator__two_message(before=None, after=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                TestComprehensive.addLog(before)
            result = func(*args, **kwargs)
            if after:
                TestComprehensive.addLog(after)
            return result

        return wrapper

    return decorator


def decorator__log_param(before=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                TestComprehensive.addLog(before, end="")
            TestComprehensive.addLog(args)
            return func(*args, **kwargs)

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


class TestComprehensive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = Game("maps/test_reset_hidden.txt")

    def setUp(self):
        TestComprehensive.log = ""

    @classmethod
    def tearDownClass(cls):
        cls.game.window.destroy()

    @classmethod
    def addLog(cls, message, end="\n"):
        cls.log += f"{message}{end}"

    def test_create_map_parsing_and_diff(self):
        TestComprehensive.game.map_file = "maps/test_create_hidden.txt"
        TestComprehensive.game.reset_game()
        game_map = TestComprehensive.game.map

        # rows / cols
        self.assertEqual(game_map.rows, 3)
        self.assertEqual(game_map.cols, 3)

        # tile check
        for i in range(3):
            for j in range(3):
                self.assertEqual(game_map.map[i][j], Tile.ROCK if i == 1 == j else Tile.EMPTY)

        # tank positions
        self.assertEqual(game_map.tank_position_map[0], (0.5, 0.5))
        self.assertEqual(game_map.tank_position_map[1], (2.5, 2.5))

        game_map.prev_map = None
        diff1 = game_map.map_diff()
        self.assertTrue(diff1.all())

        # change one tile
        game_map.map[1][1] = Tile.EMPTY
        diff2 = game_map.map_diff()
        
        for i in range(3):
            for j in range(3):
                self.assertEqual(diff2[i][j], i == 1 == j)

        # no change → all False
        diff3 = game_map.map_diff()
        self.assertFalse(diff3.any())

        TestComprehensive.game.map_file = "maps/test_reset_hidden.txt"
        TestComprehensive.game.reset_game()

    def test_collision_system(self):
        TestComprehensive.game.map_file = "maps/test_collision_hidden.txt"
        TestComprehensive.game.reset_game()
        game_map = TestComprehensive.game.map

        # no collision
        empty = game_map.collides(1.5, 2.5, 1, 1)
        self.assertEqual(empty, {})

        # boundary (outside map)
        boundary = game_map.collides(-1, 1.5, 1, 1)
        self.assertIsNone(boundary)

        # hit rock at (1,0)
        hit = game_map.collides(1.5, 0.5, 1, 0.99)
        self.assertEqual(len(hit), 1)
        self.assertIn((1, 0), hit)
        self.assertEqual(hit[(1, 0)], Tile.ROCK)

        # tank collision
        tank_hit_0 = game_map.collides_with_tank(0.5, 1.5, 0.99, 1)
        self.assertEqual(tank_hit_0, 0)

        # out of bounds
        self.assertIsNone(game_map.collides_with_tank(10, 10, 1, 1))

        TestComprehensive.game.map_file = "maps/test_reset_hidden.txt"
        TestComprehensive.game.reset_game()

    def test_trigger_bomb_chain(self):
        TestComprehensive.game.map_file = "maps/test_bomb_hidden.txt"
        TestComprehensive.game.reset_game()
        game_map = TestComprehensive.game.map

        canvas = MagicMock()
        explode = MagicMock()

        # trigger bomb at (0,0)
        game_map.trigger_bomb(canvas, 0, 0, explode)

        # all bombs in the 2×2 cluster cleared
        self.assertEqual(game_map.map[0][0], Tile.EMPTY)
        self.assertEqual(game_map.map[0][1], Tile.EMPTY)
        self.assertEqual(game_map.map[1][0], Tile.EMPTY)
        self.assertEqual(game_map.map[1][1], Tile.EMPTY)

        explode.assert_called()

        TestComprehensive.game.map_file = "maps/test_reset_hidden.txt"
        TestComprehensive.game.reset_game()

    def test_destroy_tank_behaviour(self):
        game = TestComprehensive.game

        tank0_killed = {}
        tank1_killed = {}

        def kill0():
            tank0_killed["killed"] = True

        def kill1():
            tank1_killed["killed"] = True

        for tank in game.tanks:
            if tank.tank_id == 0:
                tank.kill, ok0 = (decorator__two_functions(kill0)(tank.kill), tank.kill)
            else:
                tank.kill, ok1 = (decorator__two_functions(kill1)(tank.kill), tank.kill)

        game.reset_game, org = (
            decorator__two_message("reset_game()")(game.reset_game),
            game.reset_game,
        )

        TestComprehensive.log = ""
        game.destroy_tank(0)

        self.assertEqual(game.scoreboard.score_tank_1, 0)
        self.assertEqual(game.scoreboard.score_tank_2, 1)

        self.assertEqual(tank0_killed, {"killed": True})
        self.assertEqual(tank1_killed, {})

        self.assertEqual(TestComprehensive.log, "reset_game()\n")

        game.reset_game = org
        for tank in game.tanks:
            if tank.tank_id == 0:
                tank.kill = ok0
            else:
                tank.kill = ok1

    def test_reset_game_reinitializes_everything(self):
        game = TestComprehensive.game

        game.unbind_keys, ouk = (
            decorator__two_message("unbind_keys()")(game.unbind_keys),
            game.unbind_keys,
        )
        game.bind_keys, okb = (
            decorator__two_message("bind_keys()")(game.bind_keys),
            game.bind_keys,
        )

        Map.draw_on, omdo = (
            decorator__two_message("Map.draw_on()")(Map.draw_on),
            Map.draw_on,
        )

        Tank.draw_on, otdo = (
            decorator__two_message("Tank.draw_on()")(Tank.draw_on),
            Tank.draw_on,
        )

        TestComprehensive.log = ""
        game.reset_game()

        log = TestComprehensive.log.splitlines()

        self.assertEqual(log[0], "unbind_keys()")
        self.assertEqual(log[1], "bind_keys()")

        self.assertGreater(game.map.rows, 0)
        self.assertGreater(game.map.cols, 0)

        self.assertEqual(len(game.tanks), 2)

        ids = sorted([t.tank_id for t in game.tanks])
        self.assertEqual(ids, [0, 1])

        self.assertIn("Map.draw_on()", log)

        tank_draw_count = log.count("Tank.draw_on()")
        self.assertEqual(tank_draw_count, 2)

        game.unbind_keys = ouk
        game.bind_keys = okb
        Map.draw_on = omdo
        Tank.draw_on = otdo


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}TestComprehensive."
    tests = [k for k in TestComprehensive.__dict__.keys() if k.startswith("test")]
    append_len = len(tests) // 10

    prompt = (
        f"{0:{append_len}}: All tests\n"
        + "\n".join(f"{i+1:{append_len}}: {t}" for i, t in enumerate(tests))
        + "\nEnter a test number: "
    )

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
        suite = unittest.TestLoader().loadTestsFromTestCase(TestComprehensive)

    result = unittest.TextTestRunner(stream=temp_stream, verbosity=1).run(suite)

    if result.wasSuccessful():
        if test_num == -1:
            print(f"All tests of {file_name} passed.")
        else:
            print(f'Test "{tests[test_num]}" passed.')
    else:
        if test_num == -1:
            print(f"Some or all tests of {file_name} failed.\n{temp_stream.getvalue()}")
        else:
            print(f'Test "{tests[test_num]}" failed.\n{temp_stream.getvalue()}')


if __name__ == "__main__":
    main()
