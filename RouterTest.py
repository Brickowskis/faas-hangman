import Router, json, unittest


class TestIsAdminNumber(unittest.TestCase):
    def test_isAdminNumber_False(self):
        self.assertFalse(Router.isAdminNumber('+11234567890'))

    def test_isAdminNumber_True(self):
        self.assertTrue(Router.isAdminNumber('+13025109165'))


class TestLambdaHandler(unittest.TestCase):
    def test_lambdaHandler_AdminNoAccess(self):
        input = self.loadEvent("./test/resources/test-Router-Admin-Fail.json")
        event_output = Router.lambda_handler(input['input'], None)
        print(event_output)
        self.assertEqual(event_output['data']['command']['type'], 'admin')
        self.assertEqual(event_output['data']['command']['operation'], 'game')
        self.assertEqual(event_output['data']['command']['arguments'][0], 'start')

    def loadEvent(self, jsonFilename):
        f = open(jsonFilename)
        input = json.load(f)
        f.close()
        return input


if __name__ == '__main__':
    unittest.main()
