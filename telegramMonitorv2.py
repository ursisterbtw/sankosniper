import os
import asyncio
import httpx
import json
import datetime
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("abi.json", "r") as file:
    data = json.load(file)
    contract_abi = data["abi"]

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
API_URL = "https://sanko.tv/api/streams/activity"
MONITORED_USERNAMES = {"ursisterbtw", "degenscaper"}

monitored_streamers = set()

costs_at_supply = [
    0,
    0.00006875,
    0.000275,
    0.00061875,
    0.0011,
    0.00171875,
    0.002475,
    0.00336875,
    0.0044,
    0.00556875,
    0.006875,
    0.00831875,
    0.0099,
    0.01161875,
    0.013475,
    0.01546875,
    0.0176,
    0.01986875,
    0.022275,
    0.02481875,
    0.0275,
    0.03031875,
    0.033275,
    0.03636875,
    0.0396,
    0.04296875,
    0.046475,
    0.05011875,
    0.0539,
    0.05781875,
    0.061875
    # Add more costs if needed
]

alchemy_api_key = os.environ.get("ALCHEMY_API_KEY")
w3 = Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{alchemy_api_key}"))
contract_address = "0x06f1afa00990A69cA03F82D4c1A3a64A45F45fCb"
account_details = {
    "ursisterbtw": {
        "address": os.environ.get("URSISTERBTW_ADDRESS"),
        "private_key": os.environ.get("URSISTERBTW_PK"),
    },
    "degenscaper": {
        "address": os.environ.get("DEGENSCAPER_ADDRESS"),
        "private_key": os.environ.get("DEGENSCAPER_PK"),
    },
}
referrer = "0x0000000000000000000000000000000000000000"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def send_telegram_message(message, chat_id=TELEGRAM_CHAT_ID):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        response = httpx.post(url, json=payload)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Error sending message to Telegram: {e}")


def sell_passes(user, streamer_address, amount_to_sell):
    account = account_details.get(user)
    if not account:
        return "Invalid user"

    checksummed_streamer_address = Web3.toChecksumAddress(streamer_address)
    checksummed_my_address = Web3.toChecksumAddress(account["address"])

    packed_args = contract.functions.packArgs(
        {"amount": amount_to_sell, "addy": referrer}
    ).call()

    transaction = contract.functions.sellPasses(
        checksummed_streamer_address, packed_args
    ).buildTransaction(
        {
            "chainId": 42161,
            "gas": 1600000,
            "gasPrice": w3.toWei("3", "gwei"),
            "nonce": w3.eth.getTransactionCount(checksummed_my_address),
        }
    )

    signed_txn = w3.eth.account.signTransaction(transaction, account["private_key"])
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash.hex()


async def fetch_data():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API_URL)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error fetching data from Sanko API: {e}")
            return None


async def initialize_seen_hashes():
    seen_hashes = set()
    data = await fetch_data()
    if data:
        for item in data:
            txn_hash = item.get("transactionHash", "")
            seen_hashes.add(txn_hash)
    return seen_hashes


async def monitor_transactions(seen_hashes):
    streamer_supply = {}
    held_passes = {}

    while True:
        data = await fetch_data()
        if data:
            for item in data:
                txn_hash = item.get("transactionHash", "")
                if txn_hash not in seen_hashes:
                    seen_hashes.add(txn_hash)
                    trader_username = (
                        item.get("trader", {}).get("twitterUsername", "").lower()
                    )
                    streamer_username = (
                        item.get("streamer", {}).get("twitterUsername", "").lower()
                    )
                    streamer_address = item.get("streamer", {}).get("address", "")
                    eth_amount_str = item.get("ethAmount", "0")
                    eth_amount = float(eth_amount_str) / 10**18
                    pass_amount = int(item.get("passAmount", "0"))
                    supply = int(item.get("supply", 0))

                    streamer_supply[streamer_username] = supply

                    action = "bought" if item.get("isBuy", False) else "sold"
                    if trader_username in MONITORED_USERNAMES:
                        if action == "bought":
                            held_passes[streamer_username] = (
                                held_passes.get(streamer_username, 0) + pass_amount
                            )
                        elif action == "sold":
                            held_passes[streamer_username] = max(
                                held_passes.get(streamer_username, 0) - pass_amount, 0
                            )

                        if streamer_username in held_passes:
                            held_pass_count = held_passes[streamer_username]
                            total_eth_value = 0
                            for i in range(held_pass_count):
                                supply_index = max(supply - i - 1, 0)
                                total_eth_value += costs_at_supply[supply_index]

                        current_held = held_passes[streamer_username]
                        current_supply = streamer_supply.get(streamer_username, 0)
                        message = f"@{trader_username} is now holding {current_held} @{streamer_username} passes, worth {total_eth_value:.8f} ETH - Supply : {current_supply}\nStreamer Address : {streamer_address}"
                        send_telegram_message(message)

        await asyncio.sleep(15)


last_update_id = 0
script_start_time = int(datetime.datetime.now().timestamp())


async def fetch_telegram_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last_update_id + 1}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if data["result"]:
            for update in data["result"]:
                if update.get("message", {}).get("date", 0) > script_start_time:
                    last_update_id = update["update_id"]
                    yield update


async def handle_telegram_commands():
    while True:
        async for update in fetch_telegram_updates():
            message = update.get("message", {})
            text = message.get("text", "")
            chat_id = message.get("chat", {}).get("id")

            if text.startswith("/sellfromursisterbtw") or text.startswith(
                "/sellfromdegenscaper"
            ):
                try:
                    command, streamer_address, amount_str = text.split()
                    amount = int(amount_str)

                    if command == "/sellfromursisterbtw":
                        user = "ursisterbtw"
                    elif command == "/sellfromdegenscaper":
                        user = "degenscaper"

                    txn_hash = sell_passes(user, streamer_address, amount)
                    send_telegram_message(f"Transaction submitted: {txn_hash}", chat_id)
                except Exception as e:
                    send_telegram_message(
                        f"Error processing command: {str(e)}", chat_id
                    )

        await asyncio.sleep(2)


async def main():
    seen_hashes = await initialize_seen_hashes()
    monitor_task = asyncio.create_task(monitor_transactions(seen_hashes))
    telegram_task = asyncio.create_task(handle_telegram_commands())
    await asyncio.gather(monitor_task, telegram_task)


if __name__ == "__main__":
    asyncio.run(main())
