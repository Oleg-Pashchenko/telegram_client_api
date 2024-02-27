import requests

host = 'http://telegram.api.olegpash.tech'
# host = 'http://0.0.0.0:5003'


def send_sms_code(app_id: int, tg_hash: str):
    return requests.post(f'{host}/send-telegram-code/',
                         json={
                             'api_id': app_id,
                             'api_hash': tg_hash,
                             'phone': '89870739395'
                         }).json()  # не отправил смс код


def send_answer_to_sms_code(session_name, sms_code):
    return requests.post(f'{host}/auth/',
                         json={
                             'session_name': session_name,
                             'sms_code': sms_code
                         }).json()


def send_answer_to_sms_code_with_2fa(session_name, secret_password):
    print(session_name, secret_password)
    return requests.post(f'{host}/auth-with-2fa/',
                         json={
                             'session_name': session_name,
                             'secret_password': secret_password
                         }).json()


def get_updates(session_name: str):
    return requests.post(f'{host}/get-updates/',
                         json={
                             'session_name': session_name
                         }).json()


def test():
    api_id = 2724818
    api_hash = '6c677b0f0e2af14a53cbf0c0eafe5886'
    session_name = send_sms_code(api_id, api_hash)['answer']
    sms_code = input('Введите смс код: ')
    auth_status = send_answer_to_sms_code(session_name['session_name'], sms_code)
    print(auth_status)
    if not auth_status['status']:
        secret_password = input('Введите секретный пароль: ')
        status = send_answer_to_sms_code_with_2fa(session_name['session_name'], secret_password)
        print(session_name)
        if status['status']:
            print('Авторизация пройдена!')
        else:
            print(status)


# auth_status = send_answer_to_sms_code('8383929', '37668')
# print(auth_status)
# auth_status = send_answer_to_sms_code_with_2fa('8383929', 'gelo23122003A!')
# print(auth_status)
# test()
while True:
    print(get_updates('1514241'))
# test()
