import unittest, json, CreateGame


class TestStringMethods(unittest.TestCase):

    def test_handlerWithGameOver(self):
        input = self.loadEvent("./test/resources/test-CreateGame-input-01.json")
        event = CreateGame.handler(input['input'], None)
        self.assertEqual(event['data']['game']['solution'], 'prototypes')
        self.assertEqual(event['data']['game']['state'], 'created')

    def loadEvent(self, jsonFilename):
        f = open(jsonFilename)
        input = json.load(f)
        f.close()
        return input


if __name__ == '__main__':
    unittest.main()