import unittest
from pyonigame.helper import DictObject
from pyonigame.ui import PygameObserver
from pyonigame.view import Subject
from pyonigame import Game


class TestIntegration(unittest.TestCase):

    def setUp(self):
        # before each test
        pass

    def tearDown(self):
        # after each test
        pass

    def test_integration(self):
        try:
            settings = DictObject({
                    "caption": "My Game!",
                    "display": {
                        "mode": "dimension",
                        "dimension": {
                            "width": 2560,
                            "height": 1440
                        },
                        "fps": 120,
                        "vsync": True
                    }
                })
            game = Game(None, PygameObserver(settings))
        except Exception:
            game = None

        self.assertIsNotNone(game)


if __name__ == "__main__":
    unittest.main()