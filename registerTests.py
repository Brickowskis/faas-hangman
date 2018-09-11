import register
import json
import unittest


class TestStringMethods(unittest.TestCase):

    def test_registerPlayer(self):
        input = self.loadEvent("./test/resources/test-RegisterPlayer-input-01.json")
        event = register.handler(input["input"], {})
        print(event)
        #self.assertEqual(event["data"]["game"]["gameState"], "running")

    def loadEvent(self, jsonFilename):
        f = open(jsonFilename)
        input = json.load(f)
        f.close()
        return input


if __name__ == '__main__':
    unittest.main()
