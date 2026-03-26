import io
import os.path
import unittest
from tkinter import Tk, Canvas
import numpy as np

from map import Map, Tile


class Test3Hidden(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_trigger_bomb__corner_chain(self):
        # Chain starting from corner (0,0) triggering diagonal neighbors
        game_map = Map(5, 5)
        # Path: (0,0) -> (1,1) -> (2,2)
        game_map.map[0][0] = Tile.BOMB
        game_map.map[1][1] = Tile.BOMB
        game_map.map[2][2] = Tile.BOMB
        # Rocks adjacent to (0,0) should be destroyed
        game_map.map[0][1] = Tile.ROCK
        game_map.map[1][0] = Tile.ROCK
        
        canvas = Canvas(Test3Hidden.tk, width=game_map.width, height=game_map.height)
        
        triggered = set()
        def cb(c, r):
            triggered.add((c, r))

        game_map.trigger_bomb(canvas, 0, 0, cb)
        
        # Check bombs triggered
        # (0,0) explodes -> hits (1,1) [and rocks]
        # (1,1) explodes -> hits (2,2)
        self.assertEqual(triggered, {(0, 0), (1, 1), (2, 2)})
        
        # Check map state
        # All bombs gone
        self.assertEqual(game_map.map[0][0], Tile.EMPTY)
        self.assertEqual(game_map.map[1][1], Tile.EMPTY)
        self.assertEqual(game_map.map[2][2], Tile.EMPTY)
        # Rocks destroyed
        self.assertEqual(game_map.map[0][1], Tile.EMPTY)
        self.assertEqual(game_map.map[1][0], Tile.EMPTY)

    def test_trigger_bomb__disconnected(self):
        # Bomb triggers, but another bomb is too far (just outside 3x3)
        game_map = Map(5, 5)
        game_map.map[0][0] = Tile.BOMB
        # (0, 2) is col 2. (0,0) explosion reaches col 0+1=1.
        # So (0, 2) is safe.
        game_map.map[0][2] = Tile.BOMB 
        
        canvas = Canvas(Test3Hidden.tk, width=game_map.width, height=game_map.height)
        
        triggered = set()
        def cb(c, r):
            triggered.add((c, r))
            
        game_map.trigger_bomb(canvas, 0, 0, cb)
        
        self.assertEqual(triggered, {(0, 0)})
        self.assertEqual(game_map.map[0][0], Tile.EMPTY)
        self.assertEqual(game_map.map[0][2], Tile.BOMB) # Intact

    def test_trigger_bomb__ring_reaction(self):
        # Center bomb triggers a ring of bombs surrounding it
        game_map = Map(3, 3)
        targets = set()
        # Fill block with bombs
        for r in range(3):
            for c in range(3):
                targets.add((c, r))
                game_map.map[r][c] = Tile.BOMB
                
        canvas = Canvas(Test3Hidden.tk, width=game_map.width, height=game_map.height)
        
        count = 0
        triggered = set()
        def cb(c, r):
            nonlocal count
            count += 1
            triggered.add((c, r))
            
        game_map.trigger_bomb(canvas, 1, 1, cb)
        
        self.assertEqual(count, 9) # All 9 bombs triggered
        self.assertEqual(targets, triggered) # All 9 bombs triggered
        self.assertTrue(np.all(game_map.map == Tile.EMPTY))

    def test_trigger_bomb__rock_barrier(self):
        # Rocks get destroyed. Verify all rocks in 3x3 range are cleared.
        game_map = Map(3, 3)
        game_map.map[0][0] = Tile.ROCK
        game_map.map[0][1] = Tile.ROCK
        game_map.map[0][2] = Tile.ROCK
        game_map.map[1][0] = Tile.ROCK
        game_map.map[1][1] = Tile.BOMB
        game_map.map[1][2] = Tile.ROCK
        game_map.map[2][0] = Tile.ROCK
        game_map.map[2][1] = Tile.ROCK
        game_map.map[2][2] = Tile.ROCK
        
        canvas = Canvas(Test3Hidden.tk, width=game_map.width, height=game_map.height)
        game_map.trigger_bomb(canvas, 1, 1, lambda c, r: None)
        
        self.assertTrue(np.all(game_map.map == Tile.EMPTY))
        
    def test_trigger_bomb__diagonal(self):
        game_map = Map(100, 100)
        for i in range(100):
            game_map.map[i][i] = Tile.BOMB
            if i < 99:
                game_map.map[i][i+1] = Tile.ROCK
                game_map.map[i+1][i] = Tile.ROCK
            
        count = 0
        triggered = set()
        def cb(c, r):
            nonlocal count
            count += 1
            triggered.add((c, r))
        
        canvas = Canvas(Test3Hidden.tk, width=game_map.width, height=game_map.height)
        game_map.trigger_bomb(canvas, 0, 0, cb)
        
        self.assertEqual(count, 100)
        for i in range(100):
            self.assertIn((i, i), triggered)
        self.assertTrue(np.all(game_map.map == Tile.EMPTY))
        
    def test_trigger_bomb__reverse_diagonal(self):
        game_map = Map(50, 50)
        for i in range(50):
            game_map.map[i][49-i] = Tile.BOMB
            if i < 49:
                game_map.map[i][48-i] = Tile.ROCK
                game_map.map[i+1][49-i] = Tile.ROCK
            
        count = 0
        triggered = set()
        def cb(c, r):
            nonlocal count
            count += 1
            triggered.add((c, r))
        
        canvas = Canvas(Test3Hidden.tk, width=game_map.width, height=game_map.height)
        game_map.trigger_bomb(canvas, 49, 0, cb)
        
        self.assertEqual(count, 50)
        for i in range(50):
            self.assertIn((i, 49-i), triggered)
        self.assertTrue(np.all(game_map.map == Tile.EMPTY))
        
    def test_trigger_bomb__one_row_miss_another(self):
        game_map = Map(100, 3)
        for i in range(100):
            game_map.map[0][i] = Tile.BOMB
            game_map.map[2][i] = Tile.BOMB
            
        count = 0
        triggered = set()
        def cb(c, r):
            nonlocal count
            count += 1
            triggered.add((c, r))
        
        canvas = Canvas(Test3Hidden.tk, width=game_map.width, height=game_map.height)
        game_map.trigger_bomb(canvas, 99, 2, cb)
        
        self.assertEqual(count, 100)
        for i in range(100):
            self.assertIn((i, 2), triggered)
        self.assertTrue(np.all(game_map.map[0, :] == Tile.BOMB))
        self.assertTrue(np.all(game_map.map[1:, :] == Tile.EMPTY))
        

def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test3Hidden."
    tests = list(filter(lambda _: _.startswith("test"), Test3Hidden.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test3Hidden)
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

