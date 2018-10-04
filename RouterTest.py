import Router, json, unittest


class TestIsAdminNumber(unittest.TestCase):
    def test_isAdminNumber_False(self):
        self.assertFalse(Router.isAdminNumber('+11234567890'))

    def test_isAdminNumber_True(self):
        self.assertTrue(Router.isAdminNumber('+13025109165'))


class TestLambdaHandler(unittest.TestCase):
    def test_handler_AdminNoAccess(self):
        input = self.loadEvent("./test/resources/test-Router-Admin-Fail.json")
        event_output = Router.handler(input['input'], None)

        self.assertEqual(event_output['data']['command']['type'], 'admin')
        self.assertEqual(event_output['data']['command']['operation'], 'game')
        self.assertEqual(event_output['data']['command']['arguments'][0], 'stop')
        self.assertIsInstance(event_output['data']['errors'], SystemError)
        self.assertEqual(event_output['data']['response']['sms'], 'You do not have permission to execute this command.')

    def test_lambda_AdminCreate(self):
        input = self.loadEvent("./test/resources/test-Router-Admin-Create.json")
        event_output = Router.handler(input['input'], None)

        self.assertEqual(event_output['data']['command']['type'], 'admin')
        self.assertEqual(event_output['data']['command']['operation'], 'game')
        self.assertEqual(event_output['data']['command']['arguments'][0], 'create')
        self.assertEqual(event_output['data']['command']['arguments'][1], 'epiphany')
        self.assertEqual(event_output['data']['errors'], {})

    def test_lambda_AdminStart(self):
        input = self.loadEvent("./test/resources/test-Router-Admin-Start.json")
        event_output = Router.handler(input['input'], None)

        self.assertEqual(event_output['data']['command']['type'], 'admin')
        self.assertEqual(event_output['data']['command']['operation'], 'game')
        self.assertEqual(event_output['data']['command']['arguments'][0], 'start')
        self.assertEqual(event_output['data']['errors'], {})

    def test_lambda_AdminStop(self):
        input = self.loadEvent("./test/resources/test-Router-Admin-Stop.json")
        event_output = Router.handler(input['input'], None)

        self.assertEqual(event_output['data']['command']['type'], 'admin')
        self.assertEqual(event_output['data']['command']['operation'], 'game')
        self.assertEqual(event_output['data']['command']['arguments'][0], 'stop')
        self.assertEqual(event_output['data']['errors'], {})

    def test_lambda_AdminStatus(self):
        input = self.loadEvent("./test/resources/test-Router-Admin-Status.json")
        event_output = Router.handler(input['input'], None)

        self.assertEqual(event_output['data']['command']['type'], 'admin')
        self.assertEqual(event_output['data']['command']['operation'], 'game')
        self.assertEqual(event_output['data']['command']['arguments'][0], 'status')
        self.assertEqual(event_output['data']['errors'], {})

    def test_lambda_PlayerRegister(self):
        input = self.loadEvent("./test/resources/test-Router-Player-Register.json")
        event_output = Router.handler(input['input'], None)

        self.assertEqual(event_output['data']['command']['type'], 'player')
        self.assertEqual(event_output['data']['command']['operation'], 'register')
        self.assertEqual(event_output['data']['command']['arguments'][0], 'nessy')
        self.assertEqual(event_output['data']['errors'], {})

    def test_lambda_PlayerStatus(self):
        input = self.loadEvent("./test/resources/test-Router-Player-Status.json")
        event_output = Router.handler(input['input'], None)

        self.assertEqual(event_output['data']['command']['type'], 'player')
        self.assertEqual(event_output['data']['command']['operation'], 'status')
        self.assertEqual(event_output['data']['errors'], {})

    def test_lambda_PlayerGuessLetter(self):
        input = self.loadEvent("./test/resources/test-Router-Player-GuessLetter.json")
        event_output = Router.handler(input['input'], None)

        self.assertEqual(event_output['data']['command']['type'], 'player')
        self.assertEqual(event_output['data']['command']['operation'], 'guess')
        self.assertEqual(event_output['data']['command']['arguments'], 'a')
        self.assertEqual(event_output['data']['errors'], {})

    def test_lambda_PlayerGuessWord(self):
        input = self.loadEvent("./test/resources/test-Router-Player-GuessWord.json")
        event_output = Router.handler(input['input'], None)
        print(event_output)

        self.assertEqual(event_output['data']['command']['type'], 'player')
        self.assertEqual(event_output['data']['command']['operation'], 'guess')
        self.assertEqual(event_output['data']['command']['arguments'], 'epiphany')
        self.assertEqual(event_output['data']['errors'], {})

    def loadEvent(self, jsonFilename):
        f = open(jsonFilename)
        input = json.load(f)
        f.close()
        return input


if __name__ == '__main__':
    unittest.main()
