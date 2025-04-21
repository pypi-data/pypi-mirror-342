from telethon import TelegramClient
from telethon.tl.functions.contacts import ReportSpamRequest
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import InputPeerChannel, InputPeerChat
import asyncio

class Reporter:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def report_channel(self, channel_id: int, reason: str = "spam"):
        """Report a channel for a specific reason (default: spam)."""
        try:
            peer = await self.client.get_input_entity(channel_id)
            if isinstance(peer, InputPeerChannel):
                await self.client(ReportRequest(
                    peer=peer,
                    reason=self._get_reason(reason),
                    message="Reported via alinolreport"
                ))
                return True
            else:
                raise ValueError("Provided ID is not a channel.")
        except Exception as e:
            print(f"Error reporting channel: {e}")
            return False

    async def report_group(self, group_id: int, reason: str = "spam"):
        """Report a group for a specific reason (default: spam)."""
        try:
            peer = await self.client.get_input_entity(group_id)
            if isinstance(peer, InputPeerChat):
                await self.client(ReportRequest(
                    peer=peer,
                    reason=self._get_reason(reason),
                    message="Reported via alinolreport"
                ))
                return True
            else:
                raise ValueError("Provided ID is not a group.")
        except Exception as e:
            print(f"Error reporting group: {e}")
            return False

    async def report_spam(self, user_id: int):
        """Report a user as spam."""
        try:
            peer = await self.client.get_input_entity(user_id)
            await self.client(ReportSpamRequest(peer=peer))
            return True
        except Exception as e:
            print(f"Error reporting spam: {e}")
            return False

    def _get_reason(self, reason: str):
        from telethon.tl.types import ReportReasonSpam, ReportReasonViolence, ReportReasonPornography, ReportReasonOther
        reasons = {
            "spam": ReportReasonSpam(),
            "violence": ReportReasonViolence(),
            "pornography": ReportReasonPornography(),
            "other": ReportReasonOther()
        }
        return reasons.get(reason.lower(), ReportReasonSpam())