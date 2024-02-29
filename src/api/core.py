import datetime

import telethon
from telethon.tl.types import MessageActionGroupCall

from src.api import database
from src.api.exceptions import AuthorizationError


class Tg:
    def __init__(self, api_id: int, api_hash: str, session_name: str, phone: str,
                 sms_code: str = None, sms_hash: str = None, secret_password: str = None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.phone = phone
        self.sms_code = sms_code
        self.sms_hash = sms_hash
        self.secret_password = secret_password
        self.client = telethon.TelegramClient(f'src/api/sessions/{session_name}', api_id, api_hash, system_version="4.16.30-vxCUSTOM")

    async def connect(self):
        if not self.client.is_connected():
            await self.client.connect()

    async def is_connection_alive(self):
        try:
            await self.client.get_me()
            return True
        except Exception as e:
            print('is_c_a', e)
            return False

    async def send_auth_code(self):
        response = await self.client.send_code_request(phone=self.phone)
        self.sms_hash = response.phone_code_hash

    async def authorize_by_sms(self, sms_code: str):
        self.sms_code = sms_code
        try:
            await self.client.sign_in(phone=self.phone, code=sms_code, phone_code_hash=self.sms_hash)
        except (telethon.errors.rpcerrorlist.SessionPasswordNeededError, Exception) as auth_error:
            return False

        return True

    async def authorize_by_password(self, secret_password: str):
        self.secret_password = secret_password
        try:
            await self.client.sign_in(phone=self.phone, code=self.sms_code, phone_code_hash=self.sms_hash)
        except telethon.errors.rpcerrorlist.SessionPasswordNeededError as auth_error:
            print(auth_error, 'ae')
            try:
                await self.client.sign_in(password=secret_password)
                auth = self.is_connection_alive()
                if not auth:
                    return False
            except Exception as e:
                print(e, 'ae2')
                return False

            return True

    async def get_updates(self):
        answer = {'calls': [], 'messages': []}
        all_groups = await self.client.get_dialogs(limit=50)

        last_message_ids = {d.id: 0 for d in all_groups if d.is_group}
        current_time = datetime.datetime.now(datetime.timezone.utc)

        for dialog in all_groups:
            if dialog.is_group:
                group_id = dialog.id
                new_messages = await self.client.get_messages(group_id, min_id=last_message_ids[group_id], limit=50)

                if new_messages:
                    for message in reversed(new_messages):
                        time_difference = current_time - message.date
                        if isinstance(message.action, MessageActionGroupCall) and not message.action.duration and \
                                time_difference < datetime.timedelta(minutes=3):

                            if database.is_call_exists(message.id, self.session_name):
                                continue
                            answer['calls'].append({'name': dialog.name})
                            database.create_call(message.id, self.session_name)
                            print(f"Звонок в {dialog.name}")
                    last_message_ids[group_id] = max(last_message_ids[group_id], message.id)
        return answer
