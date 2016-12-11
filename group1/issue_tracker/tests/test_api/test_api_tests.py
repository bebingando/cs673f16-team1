import requests
import json
import unittest


class RESTAPITests(unittest.TestCase):
    """Test for REST API. Can only be run on live server"""

    @classmethod
    def setUpClass(cls):
        """Used by all Tests. Gets Token for 'test' user and creates header with it to pass to all tests"""
        cls.request = requests
        cls.base_url = 'http://127.0.0.1:8000'
        data = {'username': 'test', 'password': 'testpw'}
        response = cls.request.post(cls.base_url + '/api-token-auth/', data)
        json_response = json.dumps(response.json())
        key = json.loads(json_response)
        cls.token = key['token']
        cls.header = {'Authorization': 'Token ' + cls.token}

    def test_addComment(self):
        """Adds comment via post and checks that data matches"""
        data = {'comment': 'API Test Comment.', 'issue_id': self.base_url + '/issue_tracker/api/issue/1/'}
        response = self.request.post(self.base_url + '/issue_tracker/api/comments/', data, headers=self.header)
        json_response = json.dumps(response.json())
        json_data = json.loads(json_response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['comment'], 'API Test Comment.')

    def test_comments(self):
        """Checks that comments endpoint is reachable"""
        response = self.request.get(self.base_url + '/issue_tracker/api/comments/', headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_comments_noToken(self):
        """Checks that comments endpoint is not reachable without Token"""
        response = self.request.get(self.base_url + '/issue_tracker/api/comments/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_issues(self):
        """Checks that issues endpoint is reachable"""
        response = self.request.get(self.base_url + '/issue_tracker/api/issues/1', headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_issues_noToken(self):
        """Checks that issues endpoint is not reachable without Token"""
        response = self.request.get(self.base_url + '/issue_tracker/api/issues/1')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_issue(self):
        """Checks that issue endpoint is reachable"""
        response = self.request.get(self.base_url + '/issue_tracker/api/issue/1', headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_issue_noToken(self):
        """Checks that issue endpoint is not reachable without Token"""
        response = self.request.get(self.base_url + '/issue_tracker/api/issue/1')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    # def test_modifyMultipleIssueFields(self):
    #     """Edits multiple fields on an issue"""
    #     response = self.request.get(self.base_url + '/issue_tracker/api/ModifyMultipleIssueFields/1',
    #                                 headers=self.header)
    #     self.assertEqual(response.status_code, 200)
    #     json_response = json.dumps(response.json())
    #     json_data = json.loads(json_response)
    #     if json_data['status'] == 'Open-Accepted':
    #         status = 'Open-New'
    #     else:
    #         status = 'Open-Accepted'
    #     if json_data['priority'] == 'High':
    #         priority = 'Medium'
    #     else:
    #         priority = 'High'
    #     data = {'priority': priority,
    #             'status': status}
    #     response2 = self.request.patch(self.base_url + '/issue_tracker/api/ModifyMultipleIssueFields/1', json=data,
    #                                    headers=self.header)
    #     self.assertEqual(response2.status_code, 200)
    #     json_response2 = json.dumps(response2.json())
    #     json_data2 = json.loads(json_response2)
    #     self.assertEqual(json_data2['status'], status)
    #     self.assertEqual(json_data2['priority'], priority)

    def test_status(self):
        """Checks that status endpoint is reachable"""
        response = self.request.get(self.base_url + '/issue_tracker/api/status/1', headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_status_noToken(self):
        """Checks that status endpoint is not reachable without Token"""
        response = self.request.get(self.base_url + '/issue_tracker/api/status/1')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_priority(self):
        """Checks that priority endpoint is reachable"""
        response = self.request.get(self.base_url + '/issue_tracker/api/priority/1', headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_priority_noToken(self):
        """Checks that priority endpoint is not reachable without Token"""
        response = self.request.get(self.base_url + '/issue_tracker/api/priority/1')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
