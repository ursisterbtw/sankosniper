import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("abi.json", "r") as file:
    data = json.load(file)
    contract_abi = data["abi"]

alchemy_api_key = os.getenv("ALCHEMY_API_KEY")

w3 = Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{alchemy_api_key}"))

contract_address = "0x06f1afa00990A69cA03F82D4c1A3a64A45F45fCb"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

referrer = "0xE3983FeA05c4F4a7Bf7DC37c04f55Cb610B4C3BD"
my_address = os.getenv("URSISTERBTW_ADDRESS")
private_key = os.getenv("URSISTERBTW_PK")

STREAMER_ADDRESSES = [
    "XYZXYZXYZ",
    "XYZXYZXYZ",
    "XYZXYZXYZ",
    "XYZXYZXYZ",
]


def sell_one_pass(streamer_addresses):
    checksummed_my_address = Web3.to_checksum_address(my_address)

    for streamer_address in streamer_addresses:
        checksummed_streamer_address = Web3.to_checksum_address(streamer_address)

        unlocked_passes, _, _ = contract.functions.passesBalance(
            checksummed_streamer_address, checksummed_my_address
        ).call()

        if unlocked_passes > 0:
            packed_args = contract.functions.packArgs(
                {"amount": 1, "addy": referrer}
            ).call()

            transaction = contract.functions.sellPasses(
                checksummed_streamer_address, packed_args
            ).build_transaction(
                {
                    "chainId": 42161,
                    "gas": 500000,
                    "gasPrice": w3.to_wei("0.1", "gwei"),
                    "nonce": w3.eth.get_transaction_count(my_address),
                }
            )
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
            txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(
                f"Sold 1 pass for streamer {checksummed_streamer_address}. Transaction hash: {txn_hash.hex()}"
            )
        else:
            print(f"No unlocked passes to sell for streamer {checksummed_streamer_address}.")


if __name__ == "__main__":
    sell_one_pass(STREAMER_ADDRESSES)
