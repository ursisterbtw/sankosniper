import json
import os

from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
load_dotenv()

# Load the contract ABI
with open("abi.json", "r") as file:
    data = json.load(file)
    contract_abi = data["abi"]

# Initialize Web3
alchemy_api_key = os.getenv("ALCHEMY_API_KEY")
w3 = Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{alchemy_api_key}"))

# Contract setup
contract_address = "0x06f1afa00990A69cA03F82D4c1A3a64A45F45fCb"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Addresses
referrer = "0xE3983FeA05c4F4a7Bf7DC37c04f55Cb610B4C3BD"
my_address = os.getenv("DEGENSCAPER_ADDRESS")
private_key = os.getenv("DEGENSCAPER_PK")

STREAMER_ADDRESSES = [
    "0x9f8da9561c9b247ee3fddb6713c5ab8b19f21a36",
]


def sell_one_pass_if_supply_sufficient(streamer_addresses):
    checksummed_my_address = Web3.to_checksum_address(my_address)

    for streamer_address in streamer_addresses:
        checksummed_streamer_address = Web3.to_checksum_address(streamer_address)

        # Fetch the total supply of passes for the streamer
        supply = contract.functions.passesSupply(checksummed_streamer_address).call()

        # Check if supply is greater than or equal to 6
        if supply >= 6:
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
                        "gas": 1600000,
                        "gasPrice": w3.to_wei("3", "gwei"),
                        "nonce": w3.eth.get_transaction_count(checksummed_my_address),
                    }
                )
                signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
                txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                print(
                    f"Sold 1 pass for streamer {checksummed_streamer_address} with sufficient supply. Transaction hash: {txn_hash.hex()}"
                )
            else:
                print(
                    f"No unlocked passes to sell for streamer {checksummed_streamer_address}."
                )
        else:
            print(
                f"Supply for streamer {checksummed_streamer_address} is not sufficient for selling."
            )


if __name__ == "__main__":
    sell_one_pass_if_supply_sufficient(STREAMER_ADDRESSES)
