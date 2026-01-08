import asyncio
import json
import os
import aio_pika
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import CredentialsDB
from .schemas import AccountCreatedEvent

RABBIT_URL = os.getenv("RABBIT_URL")
EXCHANGE_NAME = "accounts_topic"

def save_credentials(evt: AccountCreatedEvent) -> None:
    db: Session = SessionLocal()
    try:
        existing = db.query(CredentialsDB).filter_by(account_id=evt.account_id).first()

        if existing:
            existing.account_no = evt.account_no
            existing.email = str(evt.email)
            existing.password = evt.password  
        else:
            db.add(
                CredentialsDB(
                    account_id=evt.account_id,
                    account_no=evt.account_no,
                    email=str(evt.email),
                    password=evt.password,
                )
            )

        db.commit()
    finally:
        db.close()

async def main():
    conn = await aio_pika.connect_robust(RABBIT_URL)
    ch = await conn.channel()

    ex = await ch.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True)

    queue = await ch.declare_queue("auth_credentials_queue", durable=True)
    await queue.bind(ex, routing_key="accounts.created")

    print("Listening for account events (routing key: 'accounts.created')...")

    async with queue.iterator() as q:
        async for msg in q:
            async with msg.process():
                data = json.loads(msg.body)
                evt = AccountCreatedEvent.model_validate(data)
                save_credentials(evt)
                print("Stored credentials for:", evt.account_no, evt.email)


if __name__ == "__main__":
    asyncio.run(main())