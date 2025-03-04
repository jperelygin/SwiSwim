from telethon.sync import TelegramClient
from app.credentials import Credentials


class Scraper:
    def __init__(self):
        self.creds = Credentials()
        self.client = TelegramClient('anon', self.creds.get("TELEGRAM_API_KEY"),
                                     self.creds.get("TELEGRAM_API_HASH"))
        self.messages = set()

    async def scrape_messages(self, limit=None):
        self.client.start()
        messages = set()
        async for message in self.client.iter_messages(self.creds.get("TG_CHANNEL_NAME"), limit=limit):
            messages.add(message)
        await self.client.disconnect()
        return messages

    def scrape_all_messages(self):
        with self.client:
            self.messages = self.client.loop.run_until_complete(self.scrape_messages())
