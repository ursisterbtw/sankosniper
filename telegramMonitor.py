import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

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


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = httpx.post(url, json=payload)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Error sending message to Telegram: {e}")


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
                                # Ensure we don't go below the first index
                                supply_index = max(supply - i - 1, 0)
                                total_eth_value += costs_at_supply[supply_index]

                        # Include the total ETH value of held passes in the message
                        current_held = held_passes[streamer_username]
                        current_supply = streamer_supply.get(streamer_username, 0)
                        message = f"@{trader_username} is now holding {current_held} @{streamer_username} passes, worth {total_eth_value:.8f} ETH - Supply : {current_supply}"

                        send_telegram_message(message)

        await asyncio.sleep(15)


async def main():
    seen_hashes = await initialize_seen_hashes()
    await monitor_transactions(seen_hashes)


if __name__ == "__main__":
    asyncio.run(main())
