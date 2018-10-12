import unittest, json, GameStop

class TestStringMethods(unittest.TestCase):

    def test_handlerWithGameOver(self):
        #Pre-condition - HangmanGame table must be created and empty
        input = self.loadEvent("./test/resources/test-StopGame-input-01.json")
        event = GameStop.handler(input["input"], {})
        print(event)
        self.assertEqual(event["data"]["game"]["gameState"], "over")

    def loadEvent(self, jsonFilename):
        f = open(jsonFilename)
        input = json.load(f)
        f.close()
        return input


if __name__ == '__main__':
    unittest.main()