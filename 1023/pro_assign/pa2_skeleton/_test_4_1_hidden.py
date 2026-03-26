import io
import os.path
import unittest

from game import Game
from tank import Tank


def decorator__two_message(before=None, after=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                Test41Hidden.addLog(before)
            result = func(*args, **kwargs)
            if after:
                Test41Hidden.addLog(after)
            return result

        return wrapper

    return decorator


def decorator__log_param(before=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                Test41Hidden.addLog(before, end="")
            Test41Hidden.addLog(args)
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


class Test41Hidden(unittest.TestCase):
    tank0: Tank
    tank1: Tank

    @classmethod
    def setUpClass(cls):
        cls.game = Game(
            "maps/test.txt"
        ) 

    def setUp(self):
        Test41Hidden.log = ""
        Test41Hidden.game.scoreboard.score_tank_1 = 0
        Test41Hidden.game.scoreboard.score_tank_2 = 0

    @classmethod
    def tearDownClass(cls):
        cls.game.window.destroy()

    @classmethod
    def addLog(cls, message, end="\n"):
        cls.log += f"{message}{end}"

    @classmethod
    def setTank(cls):
        for tank in cls.game.tanks:
            if tank.tank_id == 0:
                cls.tank0 = tank
            elif tank.tank_id == 1:
                cls.tank1 = tank

    def test_destroy__increase_score_hidden(self):
        score_tank_1_hidden = 4
        score_tank_2_hidden = 5
        for _ in range(3):
            Test41Hidden.game.destroy_tank(0)
        for _ in range(score_tank_1_hidden):
            Test41Hidden.game.destroy_tank(1)
        for _ in range(score_tank_2_hidden - 3):
            Test41Hidden.game.destroy_tank(0)

        self.assertEqual(Test41Hidden.game.scoreboard.score_tank_1, score_tank_1_hidden)
        self.assertEqual(Test41Hidden.game.scoreboard.score_tank_2, score_tank_2_hidden)

    def test_destroy__update_score_hidden(self):

        def add_scores_to_log(*args, **kwargs):
            Test41Hidden.addLog(
                f"update_score() called with score_tank_1={Test41Hidden.game.scoreboard.score_tank_1} score_tank_2={Test41Hidden.game.scoreboard.score_tank_2}"
            )

        Test41Hidden.game.scoreboard.update_score, o_us = (
            decorator__two_functions(add_scores_to_log)(
                Test41Hidden.game.scoreboard.update_score
            ),
            Test41Hidden.game.scoreboard.update_score,
        )

        score_tank_1_hidden = 4
        score_tank_2_hidden = 3
        target_log = ""
        for i in range(2):
            Test41Hidden.game.destroy_tank(1)
            target_log += (
                f"update_score() called with score_tank_1={i+1} score_tank_2=0\n"
            )
        for i in range(score_tank_2_hidden):
            Test41Hidden.game.destroy_tank(0)
            target_log += (
                f"update_score() called with score_tank_1=2 score_tank_2={i + 1}\n"
            )
        for i in range(2, score_tank_1_hidden):
            Test41Hidden.game.destroy_tank(1)
            target_log += f"update_score() called with score_tank_1={i + 1} score_tank_2={score_tank_2_hidden}\n"

        self.assertEqual(Test41Hidden.log, target_log)

        Test41Hidden.game.scoreboard.update_score = o_us

    def test_destroy__update_score_kill_tank_and_reset_game_hidden(self):
        Test41Hidden.setTank()
        Test41Hidden.game.tanks = [Test41Hidden.tank1, Test41Hidden.tank0]

        Test41Hidden.game.scoreboard.update_score, ous = (
            decorator__two_message("update_score()")(
                Test41Hidden.game.scoreboard.update_score
            ),
            Test41Hidden.game.scoreboard.update_score,
        )
        Test41Hidden.game.reset_game, org = (
            lambda: Test41Hidden.addLog("reset_game()"),
            Test41Hidden.game.reset_game,
        )
        Test41Hidden.tank0.kill, ok0 = (
            decorator__two_message("tank0.kill()")(Test41Hidden.tank0.kill),
            Test41Hidden.tank0.kill,
        )
        Test41Hidden.tank1.kill, ok1 = (
            decorator__two_message("tank1.kill()")(Test41Hidden.tank1.kill),
            Test41Hidden.tank1.kill,
        )

        for _ in range(4):
            Test41Hidden.game.destroy_tank(1)
        for _ in range(3):
            Test41Hidden.game.destroy_tank(0)

        target_log = "update_score()\ntank1.kill()\nreset_game()\nupdate_score()\ntank1.kill()\nreset_game()\nupdate_score()\ntank1.kill()\nreset_game()\nupdate_score()\ntank1.kill()\nreset_game()\nupdate_score()\ntank0.kill()\nreset_game()\nupdate_score()\ntank0.kill()\nreset_game()\nupdate_score()\ntank0.kill()\nreset_game()\n"

        self.assertEqual(Test41Hidden.log, target_log)

        Test41Hidden.game.scoreboard.update_score = ous
        Test41Hidden.tank0.kill = ok0
        Test41Hidden.tank1.kill = ok1
        Test41Hidden.game.reset_game = org

    def test_destroy__update_score_kill_tank_and_reset_game_non_consecutive(self):
        Test41Hidden.setTank()
        Test41Hidden.game.tanks = [Test41Hidden.tank1, Test41Hidden.tank0]

        Test41Hidden.game.scoreboard.update_score, ous = (
            decorator__two_message("update_score()")(
                Test41Hidden.game.scoreboard.update_score
            ),
            Test41Hidden.game.scoreboard.update_score,
        )
        Test41Hidden.game.reset_game, org = (
            lambda: Test41Hidden.addLog("reset_game()"),
            Test41Hidden.game.reset_game,
        )
        Test41Hidden.tank0.kill, ok0 = (
            decorator__two_message("tank0.kill()")(Test41Hidden.tank0.kill),
            Test41Hidden.tank0.kill,
        )
        Test41Hidden.tank1.kill, ok1 = (
            decorator__two_message("tank1.kill()")(Test41Hidden.tank1.kill),
            Test41Hidden.tank1.kill,
        )

        for _ in range(10):
            Test41Hidden.game.destroy_tank(1)
            Test41Hidden.game.destroy_tank(0)
        Test41Hidden.game.destroy_tank(0)
        Test41Hidden.game.destroy_tank(1)
            

        target_log = "update_score()\ntank1.kill()\nreset_game()\nupdate_score()\ntank0.kill()\nreset_game()\n" * 10 + "update_score()\ntank0.kill()\nreset_game()\nupdate_score()\ntank1.kill()\nreset_game()\n"

        self.assertEqual(Test41Hidden.log, target_log)

        Test41Hidden.game.scoreboard.update_score = ous
        Test41Hidden.tank0.kill = ok0
        Test41Hidden.tank1.kill = ok1
        Test41Hidden.game.reset_game = org


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test41Hidden."
    tests = list(filter(lambda _: _.startswith("test"), Test41Hidden.__dict__.keys()))
    append_len = len(tests) // 10
    prompt = (
        f"{0:{append_len}}: All tests\n"
        + "\n".join([f"{i + 1:{append_len}}: {j}" for i, j in enumerate(tests)])
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test41Hidden)
    result = unittest.TextTestRunner(stream=temp_stream, verbosity=1).run(suite)
    match result.wasSuccessful(), test_num:
        case True, -1:
            print(f"All tests of {file_name} passed.")
        case False, -1:
            print(
                f"Some or all tests of {file_name} failed. Details:\n"
                + temp_stream.getvalue()
            )
        case True, _:
            print(f'Test "{tests[test_num]}" passed.')
        case False, _:
            print(
                f'Test "{tests[test_num]}" failed. Details:\n' + temp_stream.getvalue()
            )


if __name__ == "__main__":
    main()
