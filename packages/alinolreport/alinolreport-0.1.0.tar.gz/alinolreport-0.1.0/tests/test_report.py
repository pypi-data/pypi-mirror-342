import pytest
import asyncio
from alinolreport import Reporter
from telethon import TelegramClient

@pytest.mark.asyncio
async def test_reporter_initialization():
    async with TelegramClient('session', 123, 'api_hash') as client:
        reporter = Reporter(client)
        assert reporter.client == client

# برای تست‌های بیشتر، باید اکانت واقعی و IDهای معتبر اضافه کنید