import PlayerGuess
import json
import unittest


class TestStringMethods(unittest.TestCase):

    def test_playerGuessLetter(self):
        input = self.loadEvent("./test/resources/test-Router-Player-GuessLetter.json")
        event = PlayerGuess.handler(input["input"], {})
        print(event)
        #self.assertEqual(event["data"]["game"]["gameState"], "running")

    def test_playerGuessWorld(self):
        input = self.loadEvent("./test/resources/test-Router-Player-GuessWord.json")
        event = PlayerGuess.handler(input["input"], {})
        print(event)
        #self.assertEqual(event["data"]["game"]["gameState"], "running")

    def loadEvent(self, jsonFilename):
        f = open(jsonFilename)
        input = json.load(f)
        f.close()
        return input


if __name__ == '__main__':
    unittest.main()
