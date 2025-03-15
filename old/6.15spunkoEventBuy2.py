import os
import asyncio
import json
from web3 import Web3, HTTPProvider
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from datetime import datetime
from termcolor import colored
from dotenv import load_dotenv


load_dotenv()

# Enhanced HTTPProvider with custom session and increased timeout
session = Session()
retries = Retry(connect=5, read=2, redirect=5)
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

provider = HTTPProvider(
    "https://arb-mainnet.g.alchemy.com/v2/eshIdwvkXVb_JQsaCNBWrOdmT2ZPpX_X",
    session=session,
    request_kwargs={"timeout": 20},
)

w3 = Web3(provider)

contract_address = "0x06f1afa00990A69cA03F82D4c1A3a64A45F45fCb"
with open("abi.json", "r") as file:
    data = json.load(file)
    contract_abi = data["abi"]
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

referrer = "0xE3983FeA05c4F4a7Bf7DC37c04f55Cb610B4C3BD"
my_address = os.getenv("URSISTERBTW_ADDRESS")
private_key = os.getenv("URSISTERBTW_PK")


def get_timestamp():
    return colored(datetime.now().strftime("%H:%M:%S"), "yellow")


async def purchase_passes(streamer_address, amount, price):
    checksummed_streamer_address = Web3.to_checksum_address(streamer_address)
    total_eth_to_send = w3.to_wei(str(price), "ether")
    packed_args = contract.functions.packArgs(
        {"amount": amount, "addy": referrer}
    ).call()
    transaction = contract.functions.buyPasses(
        checksummed_streamer_address, packed_args
    ).build_transaction(
        {
            "chainId": 42161,
            "gas": 500000,
            "maxPriorityFeePerGas": w3.to_wei("0.11", "gwei"),
            "maxFeePerGas": w3.to_wei("0.16", "gwei"),
            "nonce": w3.eth.get_transaction_count(my_address),
            "value": total_eth_to_send,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(get_timestamp(), end=" - ")
    print(
        f"Sniping {amount} passes for {checksummed_streamer_address} - txn hash: {txn_hash.hex()}"
    )

    loop = asyncio.get_running_loop()
    receipt = await loop.run_in_executor(
        None, w3.eth.wait_for_transaction_receipt, txn_hash
    )

    if receipt.status:
        print(get_timestamp(), end=" - ")
        print(colored(f"Txn {txn_hash.hex()} hit!", "green"))
        return True
    else:
        print(get_timestamp(), end=" - ")
        print(colored(f"Txn {txn_hash.hex()} missed!", "red"))
        return False


async def handle_trade_event(event):
    trader = event.args.trader
    streamer = event.args.streamer
    eth_amount = event.args.ethAmount / 10**18

    if trader == streamer and eth_amount == 0.0:
        print(get_timestamp(), end=" - ")
        print(f"Self buy detected for {trader}!")
        await purchase_passes(trader, 2, "0.00035078125")


async def log_loop(event_filter, poll_interval):
    while True:
        print(f"{get_timestamp()} - Ready to snipe, scanning for targets...", end="\r")
        for event in event_filter.get_new_entries():
            await handle_trade_event(event)
        await asyncio.sleep(poll_interval)


async def main():
    trade_event_filter = contract.events.Trade.create_filter(fromBlock="latest")
    await log_loop(trade_event_filter, 1)


if __name__ == "__main__":
    asyncio.run(main())
