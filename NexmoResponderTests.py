import unittest, json, NexmoResponder

class TestStringMethods(unittest.TestCase):

    def test_handlerSimpleSmsMessage(self):
        input = self.loadEvent("./test/resources/test-NexmoResponder-input-01.json")
        event = NexmoResponder.handler(input["input"], {})
        print(event)

    def test_handlerSmsMessageWithCRLF(self):
        input = self.loadEvent("./test/resources/test-NexmoResponder-input-02.json")
        event = NexmoResponder.handler(input["input"], {})
        print(event)

    def loadEvent(self, jsonFilename):
        f = open(jsonFilename)
        input = json.load(f)
        f.close()
        return input


if __name__ == '__main__':
    unittest.main()