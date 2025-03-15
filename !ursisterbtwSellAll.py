import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("abi.json", "r") as file:
    data = json.load(file)
    contract_abi = data["abi"]

alchemy_api_key = os.environ.get("ALCHEMY_API_KEY")

w3 = Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{alchemy_api_key}"))


api_url = "https://sanko.tv/api/streams/activity"
contract_address = "0x06f1afa00990A69cA03F82D4c1A3a64A45F45fCb"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

referrer = "0xE3983FeA05c4F4a7Bf7DC37c04f55Cb610B4C3BD"
my_address = os.environ.get("URSISTERBTW_ADDRESS")
private_key = os.environ.get("URSISTERBTW_PK")

STREAMER_ADDRESS = "0xd44729e92c51e9f400f867702809949edc0846d0"


def sell_all_passes(streamer_address):
    checksummed_streamer_address = Web3.toChecksumAddress(streamer_address)
    checksummed_my_address = Web3.toChecksumAddress(my_address)

    unlocked_passes, _, _ = contract.functions.passesBalance(
        checksummed_streamer_address, checksummed_my_address
    ).call()

    if unlocked_passes > 0:
        packed_args = contract.functions.packArgs(
            {"amount": unlocked_passes, "addy": referrer}
        ).call()

        transaction = contract.functions.sellPasses(
            checksummed_streamer_address, packed_args
        ).buildTransaction(
            {
                "chainId": 42161,
                "gas": 1600000,
                "gasPrice": w3.toWei("3", "gwei"),
                "nonce": w3.eth.getTransactionCount(my_address),
            }
        )
        signed_txn = w3.eth.account.signTransaction(transaction, private_key)
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(
            f"Sold {unlocked_passes} passes for streamer {checksummed_streamer_address}. Transaction hash: {txn_hash.hex()}"
        )
    else:
        print("No unlocked passes to sell for the given streamer.")


if __name__ == "__main__":
    sell_all_passes(STREAMER_ADDRESS)
