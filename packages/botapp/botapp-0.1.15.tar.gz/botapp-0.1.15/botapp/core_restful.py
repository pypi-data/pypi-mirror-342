# botapp/restful.py

import requests
import re
from .decorators import task_restful


class BotAppRestful:
    def __init__(self, api_url='http://127.0.0.1:8888/api'):
        self.api_url = api_url.rstrip('/')
        self.bot_instance = None

    def set_bot(self, bot_name, bot_description, bot_version, bot_department):
        cleaned_name = re.sub(r'[^a-zA-Z0-9]', ' ', bot_name).strip().capitalize()
        bot_description = bot_description.strip().capitalize()
        bot_version = bot_version.strip()
        bot_department = bot_department.strip().upper()

        payload = {
            'name': cleaned_name,
            'description': bot_description,
            'version': bot_version,
            'department': bot_department,
            'is_active': True
        }

        # Check if bot exists
        r = requests.get(f"{self.api_url}/bots/", params={'search': cleaned_name})
        bots = r.json()
        match = next((b for b in bots if b['name'] == cleaned_name), None)

        if match:
            self.bot_instance = match
            # update if different
            updated_fields = {}
            for field in ['description', 'version', 'department']:
                if self.bot_instance[field] != payload[field]:
                    updated_fields[field] = payload[field]

            if updated_fields:
                requests.patch(f"{self.api_url}/bots/{self.bot_instance['id']}/", data=updated_fields)
        else:
            r = requests.post(f"{self.api_url}/bots/", data=payload)
            self.bot_instance = r.json()

    def _get_or_create_task(self, func):
        if self.bot_instance is None:
            raise Exception("Bot not set. Call set_bot() first.")

        # Check if task exists
        r = requests.get(f"{self.api_url}/tasks/", params={'bot': self.bot_instance['id'], 'name': func.__name__})
        tasks = r.json()
        match = next((t for t in tasks if t['name'] == func.__name__), None)

        if match:
            # update description if needed
            if match['description'] != (func.__doc__ or ''):
                requests.patch(f"{self.api_url}/tasks/{match['id']}/", data={'description': func.__doc__ or ''})
            return match
        else:
            payload = {
                'bot': self.bot_instance['id'],
                'name': func.__name__,
                'description': func.__doc__ or '',
            }
            r = requests.post(f"{self.api_url}/tasks/", data=payload)
            return r.json()

    def task(self, func):
        self._get_or_create_task(func)
        return task_restful(self, func)
