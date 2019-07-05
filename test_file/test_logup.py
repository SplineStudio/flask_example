import requests
import json
import unittest
import re


def CreateData():
 data = {"first_name": "alic",
                           "last_name": "Vegan",
                           "email": "egan@mail.com",
                           "password": "1234"}
 return data

def EgualEmail():
    data = CreateData()
    if data["email"]  == " " or re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$)", data["email"]) !=None:
        return True


def EqualPassword():
    data = CreateData()
    if data["password"] == " " or re.search(('[0-9]|[A-Z]|[a-z]'), data["password"]) !=None:
        return True

def EqualFirstName():
    data = CreateData()
    if data["first_name"]  != " ":
        return True

def EqualLastName():
    data = CreateData()
    if data["last_name"] != " ":
        return True


def postlogup():
    url = 'http://127.0.0.1:5000/api/signup'
    headers = {'Content-type': 'application/json',  # Определение типа данных
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}
    data = CreateData()
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    print(data)
    response = answer.json()
    code = response['code']
    print(response)
    return code


class BasicTests(unittest.TestCase):
    def test_logup(self):
        self.assertEqual(postlogup(),1)


    def test_name(self):
        self.assertEqual(EqualFirstName(), True)


    def test_last_name(self):
        self.assertEqual(EqualLastName(), True)


    def test_email(self):
        self.assertEqual(EgualEmail(),True)


    def test_password(self):
        self.assertEqual(EqualPassword(),True)


if __name__ == "__main__":
    unittest.main()