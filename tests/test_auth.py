import logging
import json
from app.db.models import Users


logger = logging.getLogger(__name__)

def user_registration(client, **kwargs):
    reg_data = {
        'username': 'test1',
        'email': 'jj@test.com',
        'password': '1ASDASDA!',
        'language': 'eng'
    }
    for k,v in kwargs.items():
        reg_data[k] = v
    return client.post('auth/register',
                       data=json.dumps(reg_data),
                       content_type='application/json')

def test_user_registration_success(client):
    response = user_registration(client)
    assert response.status_code == 201
    user = Users.query.filter_by(email='jj@test.com').first()
    assert user is not None
    assert user.username == 'test1'

def test_user_weak_password(client):
    response = user_registration(client,
                                 username='test2',
                                 password='AAA1',
                                 email='jj2@test.com')
    assert response.status_code == 400
    logger.debug(f"Response text: {response.text}, {response.request}")
    assert Users.query.filter_by(username='test2').first() is None

def test_user_no_numbers_password(client):
    response = user_registration(client,
                                 username='test2',
                                 password='AAA!@#ASDASD',
                                 email='jj2@test.com')
    assert response.status_code == 400
    logger.debug(f"Response text: {response.text}")
    assert Users.query.filter_by(username='test2').first() is None

def test_user_no_spec_chars_password(client):
    response = user_registration(client,
                                 username='test2',
                                 password='AAA123DASD',
                                 email='jj2@test.com')
    assert response.status_code == 400
    logger.debug(f"Response text: {response.text}")
    assert Users.query.filter_by(username='test2').first() is None

def test_user_wrong_characters_password(client):
    response = user_registration(client,
                                 username='test2',
                                 password='1ЫЫЫЫЫЫЫЫЫЫZ!_',
                                 email='jj2@test.com')
    assert response.status_code == 400
    logger.debug(f"Response text: {response.text}, {response.request}")
    assert Users.query.filter_by(username='test2').first() is None

def test_user_username_already_exists(client):
    response1 = user_registration(client, username='test3', email='jj3@test.com')
    assert response1.status_code == 201
    logger.debug(f"Response test: {response1.text}")
    response2 = user_registration(client, username='test3', email='jj3@test.com')
    assert response2.status_code == 400
    assert "Username is already registered" in response2.text
    assert Users.query.filter_by(username='test3').first() is not None

def test_user_email_not_valid(client):
    text = "Email is not in valid format"
    response = user_registration(client, username='test4', email='!32@test.com')
    assert response.status_code == 400
    assert text in response.text
    response = user_registration(client, username='test4', email='www.test.com')
    assert response.status_code == 400
    assert text in response.text
    response = user_registration(client, username='test4', email='gh32@test.co__m')
    assert response.status_code == 400
    assert text in response.text

def test_user_email_already_registered(client):
    response1 = user_registration(client, username='test5', email='jj5@test.com')
    assert response1.status_code == 201
    response2 = user_registration(client, username='test6', email='jj5@test.com')
    assert response2.status_code == 400
    assert Users.query.filter_by(email='jj5@test.com').first() is not None
    assert "Email is already registered" in response2.text

# TODO: Launch all tests from different IPs?
# def test_registration_limiter(client):
#     reg_data = {
#         'username': 'test7',
#         'email': 'jj7@test.com',
#         'password': '1ASDASDA!',
#         'language': 'eng'
#     }
#     headers = {
#         'X-Forwarded-For': '192.168.1.1',
#         'Content-Type': 'application/json'
#     }
#     for _ in range(6):
#         client.post('auth/register', data=reg_data, headers=headers)
#     response = client.post('auth/register', data=reg_data, headers=headers)
#     assert response.status_code == 429
#     logger.debug(response.text)
#     reg_data['username'] = 'test8'
#     reg_data['email'] = 'jj8@test.com'
#     headers['X-Forwarded-For'] = '192.168.1.2'
#     response = client.post('auth/register', data=reg_data, headers=headers)
#     assert response.status_code == 200


def test_user_login_successful(client):
    user_registration(client,
                      username='test10',
                      email='jj10@test.com',
                      password='AAAAAAAA1!')
    login_data = {
        'username': 'test10',
        'password': 'AAAAAAAA1!'
    }
    response = client.post('/auth/login',
                           data=json.dumps(login_data),
                           content_type='application/json')
    assert response.status_code == 200
    logger.debug(f'Response: {response.text}')
    assert response.json['user_id'] == Users.query.filter_by(email='jj10@test.com').first().id
    assert bool(response.json['access_token'])

def test_user_login_wrong_password(client):
    user_registration(client,
                      username='test11',
                      email='jj11@test.com',
                      password='AAAAAAAA1!')
    login_data = {
        'username': 'test11',
        'password': 'AAAAAAAA2!'
    }
    response = client.post('/auth/login',
                           data=json.dumps(login_data),
                           content_type='application/json')
    assert response.status_code == 401
    logger.debug(f'Response: {response.text}')
    assert "Invalid credentials" in response.text

def test_user_login_wrong_username(client):
    user_registration(client,
                      username='test12',
                      email='jj12@test.com',
                      password='AAAAAAAA1!')
    login_data = {
        'username': 'test1OOOOO',
        'password': 'AAAAAAAA1!'
    }
    response = client.post('/auth/login',
                           data=json.dumps(login_data),
                           content_type='application/json')
    assert response.status_code == 401
    logger.debug(f'Response: {response.text}')
    assert "Invalid credentials" in response.text