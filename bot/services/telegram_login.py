from pyrogram import Client

api_id = 123456  # put in config later
api_hash = "YOUR_API_HASH"

user_clients = {}
login_sessions = {}


async def start_login(user_id: int, phone: str):
    client = Client(
        f"sessions/{user_id}",
        api_id=api_id,
        api_hash=api_hash,
    )

    await client.connect()

    sent = await client.send_code(phone)

    login_sessions[user_id] = {
        "client": client,
        "phone": phone,
        "phone_code_hash": sent.phone_code_hash,
    }


async def verify_code(user_id: int, code: str):
    data = login_sessions.get(user_id)

    if not data:
        return False

    client = data["client"]

    try:
        await client.sign_in(
            phone_number=data["phone"],
            phone_code_hash=data["phone_code_hash"],
            phone_code=code,
        )

        user_clients[user_id] = client
        del login_sessions[user_id]

        return True

    except Exception:
        return False


def get_client(user_id: int):
    return user_clients.get(user_id)
