# dhisana/email_io.py
import asyncio
import datetime
import email
import logging
from email.mime.text import MIMEText
from typing import List, Tuple

import aiosmtplib
import imaplib
import os

from dhisana.schemas.sales import MessageItem
from dhisana.utils.google_workspace_tools import QueryEmailContext, SendEmailContext

# --------------------------------------------------------------------------- #
#  Outbound -- SMTP
# --------------------------------------------------------------------------- #

async def send_email_via_smtp_async(
    ctx: SendEmailContext,
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
    *,
    use_starttls: bool = True,
) -> Tuple[int, bytes]:
    """
    Send a single e-mail over SMTP (TLS or SSL).

    Returns
    -------
    Tuple[int, bytes]
        The (code, message) returned by the SMTP server.
    """

    msg = MIMEText(ctx.body, _charset="utf-8")
    msg["From"] = f"{ctx.sender_name} <{ctx.sender_email}>"
    msg["To"] = ctx.recipient
    msg["Subject"] = ctx.subject

    smtp_kwargs = dict(
        hostname=smtp_server,
        port=smtp_port,
        username=username,
        password=password,
    )
    if use_starttls:
        smtp_kwargs["start_tls"] = True          # TLS upgrade on port 587
    else:
        smtp_kwargs["tls"] = True                # Implicit SSL on port 465

    try:
        code, response = await aiosmtplib.send(msg, **smtp_kwargs)
        logging.info("SMTP send OK – code %s", code)
        return code, response
    except Exception:
        logging.exception("SMTP send failed")
        raise

# --------------------------------------------------------------------------- #
#  Inbound -- IMAP
# --------------------------------------------------------------------------- #

def _imap_date(iso_dt: str) -> str:
    """2025-04-22T00:00:00Z → 22-Apr-2025 (IMAP format)."""
    dt = datetime.datetime.fromisoformat(iso_dt.replace("Z", "+00:00"))
    return dt.strftime("%d-%b-%Y")


def _parse_email_msg(raw_bytes: bytes) -> MessageItem:
    msg = email.message_from_bytes(raw_bytes)

    # Header helpers
    def hdr(h): return msg.get(h, "")

    sender_name, sender_email = email.utils.parseaddr(hdr("From"))
    receiver_name, receiver_email = email.utils.parseaddr(hdr("To"))

    try:
        sent_at = email.utils.parsedate_to_datetime(hdr("Date")).isoformat()
    except Exception:
        sent_at = ""

    # Grab first text/plain part
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in str(
                part.get("Content-Disposition", "")
            ):
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    return MessageItem(
        message_id=hdr("Message-ID"),
        thread_id=hdr("Message-ID") or "",
        sender_name=sender_name,
        sender_email=sender_email,
        receiver_name=receiver_name,
        receiver_email=receiver_email,
        iso_datetime=sent_at,
        subject=hdr("Subject"),
        body=body,
    )


async def list_emails_in_time_range_imap_async(
    ctx: QueryEmailContext,
    imap_server: str,
    imap_port: int,
    username: str,
    password: str,
    *,
    mailbox: str = "INBOX",
    use_ssl: bool = True,
) -> List[MessageItem]:
    """
    Return messages whose **Date** header lies in [start_time, end_time).
    """

    def _worker() -> List[MessageItem]:
        conn = imaplib.IMAP4_SSL(imap_server, imap_port) if use_ssl else imaplib.IMAP4(
            imap_server, imap_port
        )

        try:
            conn.login(username, password)
            conn.select(mailbox, readonly=True)

            since = _imap_date(ctx.start_time)
            before = _imap_date(ctx.end_time)

            criteria = ["SINCE", since, "BEFORE", before]
            if ctx.unread_only:
                criteria.insert(0, "UNSEEN")

            status, msg_nums = conn.search(None, *criteria)
            if status != "OK":
                logging.warning("IMAP search failed: %s %s", status, criteria)
                return []

            items: List[MessageItem] = []
            for num in msg_nums[0].split():
                _, data = conn.fetch(num, "(RFC822)")
                if data and data[0]:
                    items.append(_parse_email_msg(data[0][1]))
            return items

        finally:
            # Defensive close – some servers complain if you CLOSE after LOGOUT.
            try:
                conn.close()
            except Exception:
                pass
            conn.logout()

    return await asyncio.to_thread(_worker)