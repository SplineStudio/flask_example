import requests
import json
import unittest
import re


def CreateData():
    data = {"email": "vegan@mail.com", "password": "1234"}
    return data


def EgualEmail():
    data = CreateData()
    if data["email"] == " " or re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$)", data["email"]) != None:
        return True


def EqualPassword():
    data = CreateData()
    if data["password"] == " " or re.search(('[0-9]|[A-Z]|[a-z]'), data["password"]) != None:
        return True


def postlogup():
    url = 'http://127.0.0.1:5000/api/signin'
    headers = {'Content-type': 'application/json',  # Определение типа данных
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}
    data = CreateData()
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    response = answer.json()
    code = response['code']
    return response


def code():
    code = postlogup()
    return code['code']


def refresh_token():
    refresh_token = postlogup()
    print(refresh_token['refresh_token'])
    return refresh_token['refresh_token']


def access_token():
    access_token = postlogup()
    print(access_token['access_token'])
    return access_token['access_token']


refresh_token()
access_token()


class BasicTests(unittest.TestCase):
    def test_code(self):
        self.assertEqual(code(), 1)

    def test_email(self):
        self.assertEqual(EgualEmail(), True)

    def test_password(self):
        self.assertEqual(EqualPassword(), True)

    def test_token(self):
        self.assertEqual()


if __name__ == "__main__":
    unittest.main()
