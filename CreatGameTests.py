import unittest, json, CreateGame, boto3

class TestStringMethods(unittest.TestCase):

    def test_handlerWithGameOver(self):
        #Pre-condition - HangmanGame table must be created and empty
        input = self.loadEvent("./test/resources/test-CreateGame-input-01.json")
        event = CreateGame.handler(input["input"], {})
        print(event)
        self.assertEqual(event["data"]["game"]["solution"], "prototypes")
        self.assertEqual(event["data"]["game"]["gameState"], "created")

    def loadEvent(self, jsonFilename):
        f = open(jsonFilename)
        input = json.load(f)
        f.close()
        return input


if __name__ == '__main__':
    unittest.main()