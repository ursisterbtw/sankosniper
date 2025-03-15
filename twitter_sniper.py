import asyncio
import csv
import json
import logging
import os
import random
from datetime import datetime

import httpx
import pyotp
from dotenv import load_dotenv
from termcolor import colored
from tweety import Twitter
from web3 import Web3

# testing 12/14 3:30am

load_dotenv()

accounts = [
    {
        "username": os.environ.get("TWIT1"),
        "password": os.environ.get("TWIT1_PASSWORD"),
        "otp_key": os.environ.get("TWIT1_OTP_KEY"),
    },
    {
        "username": os.environ.get("TWIT2"),
        "password": os.environ.get("TWIT2_PASSWORD"),
        "otp_key": os.environ.get("TWIT2_OTP_KEY"),
    },
]
try:
    twi = Twitter("session")
except Exception:
    os.remove("session.tw_session")
    twi = Twitter("session")

account = random.choice(accounts)
print(f'Using: {account["username"]}')

totp = pyotp.TOTP(account["otp_key"])
otp = totp.now()

twi.sign_in(account["username"], account["password"], extra=otp)

streamer_follower_data = {}

api_url = "https://sanko.tv/api/streams/activity"
contract_address = "0x06f1afa00990A69cA03F82D4c1A3a64A45F45fCb"
referrer = "0x0000000000000000000000000000000000000000"

alchemy_api_key = os.environ.get("ALCHEMY_API_KEY")
my_address = os.environ.get("DEGENSCAPER_ADDRESS")
private_key = os.environ.get("DEGENSCAPER_PK")

w3 = Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{alchemy_api_key}"))

with open("abi.json", "r") as file:
    data = json.load(file)
    contract_abi = data["abi"]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

LEGENDARY_SET = {
    "CL207",
    "cobie",
    "EricCryptoman",
    "SappySealsNFT",
    "koreanjewcrypto",
    "SizeChad",
    "veH0rny",
    "0xSisyphus",
    "Banks",
    "Cheguevoblin",
    "bitcoinpanda69",
    "Tradermayne",
    "Mongraal",
    "CryptoGodJohn",
    "chiefingza",
    "inversebrah",
    "0xHedge32",
    "Brentsketit",
    "CryptoDonAlt",
    "wabdoteth",
    "0xLawliette",
    "bigdickbull69",
    "hentaiavenger66",
    "gainzy222",
    "AWice",
    "HsakaTrades",
    "FaZeAdapt",
    "FaZeRug",
    "Pancakesbrah",
    "degenharambe",
    "yugoviking",
    "Pentosh1",
    "loomdart",
    "BobLaxative",
    "thevickiejay",
    "Vince_Van_Dough",
    "IamNomad",
    "littlestpwince",
}

BULLSEYE_SET = {
    "bryptokenneth3",
    "PepenardoStudio",
    "Darkfarms1",
    "ScrillaVentura",
    "CC2Ventures",
    "ashrobinqt",
    "PudgyGaming",
    "tittyrespecter",
    "maverick23NFT",
    "Nate_Rivers",
    "TitanXBT",
    "Luckytradess",
    "sayinshallah",
    "Temperrr",
    "Swagg",
    "TheBoiSantana",
    "CryptoGorillaYT",
    "JakeSucky",
    "MINHxDYNASTY",
    "pedrigavifrenki",
    "FaZe_Rain",
    "NICKMERCS",
    "RealJonahBlake",
    "erafps",
    "The_Bogfather",
    "winnyeth",
    "yaraela",
    "SkylineETH",
    "cheatcoiner",
    "process_grey",
    "Fitchinverse",
    "skotizhoe",
    "d_gilz",
    "dailybrd",
    "briiTwitch",
    "nsfwbrii",
    "toadswiback",
    "ParallelTCG",
    "orangie",
    "whatslukedoing",
    "morphPOGdot23",
    "Dew_HQ",
    "litocoen",
    "CharlotteFang77",
    "ParallelTCGpod",
    "Jorraptor",
    "sentientGirlx",
    "prtyDAO",
    "CryptoHayes",
    "ByzGeneral",
    "NFTwap",
    "0xMikeThree",
    "boldleonidas",
    "batzdu",
    "SmokeyTheBera",
    "berachain",
    "smartestmoney_",
    "cburniske",
    "0xfoobar",
    "icebagz_",
    "OverDogsPodcast",
    "FU_STUDIOS",
    "opunshizun",
    "traderpow",
    "jyxdi",
    "functi0nZer0",
    "EvgenyGaevoy",
    "emgurevich",
    "BoringSleuth",
    "DegenerateNews",
    "CryptoFinally",
    "icebergy_",
    "TungstenDAO",
    "NotablePepes",
    "RugRadio",
    "farokh",
    "FLAMINGODAO",
    "FAKERARES_XCP",
    "jackbutcher",
    "visualizevalue",
    "checksvv",
    "opepenedition",
    "funghibull",
    "shillrxyz",
    "samanthacavet",
    "Scearpo",
    "remiliacorp333",
    "MiladyMaker333",
    "RemiQuarterly",
    "YayoCorp",
    "BonklerNFT",
    "RemilioBaby",
    "barneyxbt",
    "0xMerp",
    "moritz_web3",
    "PopPunkOnChain",
    "PopPunkLLC",
    "VoxyTwitch",
    "Slysssa",
    "TrumpSC",
    "TL_Bunnyhoppor",
    "LambySeriesGG",
    "trading_vapor",
    "izebel_eth",
    "0xHoney",
    "trippyxbt",
    "serbobross",
    "g3_wtf",
    "notsofast",
    "blockchaingod69",
    "playcambria",
    "DeFiMinty",
    "MariaShen",
    "0xNFTdart",
    "TheCryptoDog",
    "outpxce",
    "fxnction",
    "wronguser000",
    "watchking69",
    "UniswapVillain",
    "voldemortxbt",
    "IcedKnife",
    "waleswoosh",
    "shahh",
    "Zeneca",
    "NFT_GOD",
    "0xfetty",
    "KookCapitalLLC",
    "TheShamdoo",
    "CirrusNFT",
    "notEezzy",
    "ClaireSilver12",
    "scott_lew_is",
    "SpottieWiFi",
    "njoo",
    "steamboy33",
    "daphtheSHAFT",
    "hoshiboyzen",
    "2pmflow",
    "locationtba",
    "DemAzuki",
    "ZAGABOND",
    "emilyrosemcg",
    "whizwang",
    "febtea",
    "0xCygaar",
    "Josephdelong",
    "statelayer",
    "0xMontBlanc",
    "Sayuki0x",
    "RMM_RMM_",
    "Tree_of_Alpha",
    "News_Of_Alpha",
    "CryptoCred",
    "breakoutprop",
    "ColdBloodShill",
    "_WOO_X",
    "TheFlowHorse",
    "Rebirthdao",
    "Synquote",
    "jimtalbot",
    "RookieXBT",
    "magnetmoneyshow",
    "magnetmoney",
    "pierre_crypt0",
    "satsdart",
    "WOOnetwork",
    "ledgerstatus",
    "flip_xyz",
    "mattomattik",
    "uponlytv",
    "SalsaTekila",
    "Awawat_Trades",
    "Crypto_Chase",
    "crypto_iso",
    "Crypto_McKenna",
    "LSDinmycoffee",
    "TheHavenCrypto",
    "tradinglord",
    "kollectiv_io",
    "HighStakesCap",
    "ThinkingUSD",
    "insilicotrading",
    "KeyboardMonkey3",
    "evincowinerydao",
    "rebootgg_",
    "rektradio_",
    "rollbitcom",
    "Rewkang",
    "mechanismcap",
    "PleasrDAO",
    "saliencexbt",
    "snailnews_",
    "LinXBT",
    "Cryptoyieldinfo",
    "Imperator_0x",
    "Crypto_Joe10",
    "Rug_ai",
    "jeffwilser",
    "NYTimes",
    "CoinDesk",
    "ExplorersClub",
    "RunnerXBT",
    "wormholecrypto",
    "Kr3py",
    "VibezDao",
    "Dupe_fi",
    "Dmitriysz",
    "deltaxbt",
    "idexio",
    "Route2FI",
    "silentdao_",
    "alistairmilne",
    "sobylife",
    "arbitrum",
    "xai_games",
    "finalformxp",
    "mynaswap",
    "MatriXBT",
    "nolackingcap",
    "tbr90",
    "Yale",
    "Google",
    "CERN",
    "carolinecapital",
    "cz_binance",
    "binance",
    "VitalikButerin",
    "BrettHarrison88",
    "Architect_xyz",
    "AlamedaTrabucco",
    "KinkyBedBugs",
    "RUGenerous",
    "EducationSimpl",
    "cyluswatson",
    "d1pp3r__",
    "_TreeNFT",
    "Dumpster_DAO",
    "0xOlivia",
    "dcdao_",
    "alexandrabotez",
    "OpTic",
    "Crypto_Ed_NL",
    "CozomoMedici",
    "kdean",
    "gbmedici",
    "TheBlock__",
    "TheBlockPro__",
    "theblockupdates",
    "cryptomanran",
    "limfx88",
    "UniofOxford",
    "Poyo_Satou",
    "forecastooor",
    "Evan_ss6",
    "LeiskeKevin",
    "0xAmey",
    "supermariokartD",
    "FreddieRaynolds",
    "Crypto_Noddy",
    "stanfordpvp",
    "news_of_alpha",
    "nir_III",
    "yup_io",
    "traderhounds",
    "GraysonJAllen",
    "justinsuntron",
    "TRONDAO",
    "BitTorrent",
    "htx_global",
    "Blockanalia",
    "laurashin",
    "unchained_pod",
    "unchainedcrypto",
    "novogratz",
    "COMPASSPathway",
    "SpaceX",
    "REFORM",
    "HudsonRiverPark",
    "nat9crypto",
    "passytee",
}

# assumes supply 1,2,3 have been bought
LEGENDARY_BUY_PARAMS = {
    3: {"amount": 7, "eth": "0.01925"},
    4: {"amount": 6, "eth": "0.01863125"},
    5: {"amount": 5, "eth": "0.01753125"},
    6: {"amount": 4, "eth": "0.0158125"},
    7: {"amount": 3, "eth": "0.0133375"},
    8: {"amount": 2, "eth": "0.00996875"},
    9: {"amount": 1, "eth": "0.00556875"},
}

# assumes supply 1,2,3 have been bought
BULLSEYE_BUY_PARAMS = {
    3: {"amount": 5, "eth": "0.00928125"},
    4: {"amount": 4, "eth": "0.0086625"},
    5: {"amount": 3, "eth": "0.0075625"},
    6: {"amount": 2, "eth": "0.00584375"},
    7: {"amount": 1, "eth": "0.00336875"},
}

# assumes supply 1,2,3 have been bought
TARGET_BUY_PARAMS = {
    3: {"amount": 3, "eth": "0.0034375"},
    4: {"amount": 2, "eth": "0.00281875"},
    5: {"amount": 1, "eth": "0.00171875"},
}

# buys are based on available supply
SMOL_BUY_PARAMS = {
    3: {"amount": 2, "eth": "0.0017875"},
}


def get_timestamp():
    timestamp = datetime.now().strftime("%H:%M:%S")
    return colored(timestamp, "yellow")


def log_transaction(status, arbiscan_link):
    with open("TH_txn_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status,
                arbiscan_link,
            ]
        )


async def purchase_passes(streamer_address, amount, price):
    checksummed_streamer_address = Web3.toChecksumAddress(streamer_address)
    total_eth_to_send = w3.toWei(str(price), "ether")
    packed_args = contract.functions.packArgs(
        {"amount": amount, "addy": referrer}
    ).call()
    transaction = contract.functions.buyPasses(
        checksummed_streamer_address, packed_args
    ).buildTransaction(
        {
            "chainId": 42161,
            "gas": 2200069,
            "maxPriorityFeePerGas": w3.toWei("4", "gwei"),
            "maxFeePerGas": w3.toWei("4", "gwei"),
            "nonce": w3.eth.getTransactionCount(my_address),
            "value": total_eth_to_send,
        }
    )
    signed_txn = w3.eth.account.signTransaction(transaction, private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(get_timestamp(), end=" - ")
    print(
        f"sniping {amount} passes for {checksummed_streamer_address} - txn hash: {txn_hash.hex()}"
    )

    loop = asyncio.get_running_loop()
    receipt = await loop.run_in_executor(
        None, w3.eth.waitForTransactionReceipt, txn_hash
    )

    arbiscan_link = f"https://arbiscan.io/tx/{txn_hash}"
    if receipt.status:
        print(get_timestamp(), end=" - ")
        print(colored(f"txn {txn_hash.hex()} was successful!", "green"))
        log_transaction("Hit", arbiscan_link)
        return True
    else:
        print(get_timestamp(), end=" - ")
        print(colored(f"txn {txn_hash.hex()} failed!", "red"))
        log_transaction("Miss", arbiscan_link)
        return False


async def fetch_data():
    retry_count = 0
    max_retries = 5
    retry_delay = 52 / 7
    timeout_duration = 30.02 / 7

    async with httpx.AsyncClient(timeout=timeout_duration) as client:
        while retry_count < max_retries:
            try:
                response = await client.get(api_url)
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                logging.error(f"HTTP status error at {datetime.now()}: {e}")
                print(get_timestamp(), end=" - ")
                print(f"HTTP status error, retrying in {retry_delay} seconds...")

            except httpx.TimeoutException:
                logging.error(f"Timeout error at {datetime.now()}")
                print(get_timestamp(), end=" - ")
                print(f"Timeout error, retrying in {retry_delay} seconds...")

            except httpx.RequestError as e:
                logging.error(f"Request error at {datetime.now()}: {e}")
                print(get_timestamp(), end=" - ")
                print(f"Request error, retrying in {retry_delay} seconds...")

            await asyncio.sleep(retry_delay)
            retry_count += 1

        print(get_timestamp(), end=" - ")
        print("Max retries reached. Skipping data fetch for this cycle.")
        return None


def filter_data(data, seen_hashes):
    new_transactions = [
        item for item in data if item["transactionHash"] not in seen_hashes
    ]
    seen_hashes.update(item["transactionHash"] for item in new_transactions)
    return new_transactions


async def display_transactions(transactions):
    global streamer_follower_data

    for item in transactions:
        eth_amount = int(item["ethAmount"]) / 10**18
        streamer_address = item["streamer"]["privyAddress"]
        streamer_username = item["streamer"]["twitterUsername"]
        trader_username = item["trader"]["twitterUsername"]
        is_buy = item["isBuy"]
        supply = int(item.get("supply", 0))
        pass_amount = item.get("passAmount", 0)

        action = "bought" if is_buy else "sold"
        action_color = "green" if is_buy else "red"

        timestamp = datetime.now().strftime("%H:%M:%S")
        colored_timestamp = colored(timestamp, "yellow")
        colored_action = colored(action, action_color)
        print(
            f"{colored_timestamp} - {trader_username} {colored_action} {pass_amount} {streamer_username} passes for {eth_amount} ETH"
        )

        if is_buy and trader_username == streamer_username and streamer_username not in streamer_follower_data:
            user_data = twi.get_user_info(streamer_username)
            follower_count = user_data.followers_count
            print(f"{streamer_username} has {follower_count} followers.")
            streamer_follower_data[streamer_username] = follower_count

        buy_params = None
        if streamer_username in LEGENDARY_SET and supply in LEGENDARY_BUY_PARAMS:
            buy_params = LEGENDARY_BUY_PARAMS[supply]
        elif streamer_username in BULLSEYE_SET and supply in BULLSEYE_BUY_PARAMS:
            buy_params = BULLSEYE_BUY_PARAMS[supply]
        elif streamer_username in TARGET_SET and supply in TARGET_BUY_PARAMS:
            buy_params = TARGET_BUY_PARAMS[supply]

        elif streamer_username in streamer_follower_data:
            follower_count = streamer_follower_data[streamer_username]
            if follower_count > 25000:
                buy_params = BULLSEYE_BUY_PARAMS.get(supply)
            elif follower_count > 1000:
                buy_params = TARGET_BUY_PARAMS.get(supply)
            elif follower_count > 500:
                buy_params = SMOL_BUY_PARAMS.get(supply)

        if buy_params:
            success = await purchase_passes(
                streamer_address, buy_params["amount"], buy_params["eth"]
            )
            if success:
                print(
                    f"!! Hit {buy_params['amount']} {streamer_username} passes for {buy_params['eth']} ETH !!"
                )
            else:
                print(f"!! Missed on {streamer_username} !!")


async def initialize_seen_hashes():
    data = await fetch_data()
    return {item["transactionHash"] for item in data} if data else set()


async def main():
    seen_hashes = await initialize_seen_hashes()
    while True:
        print(f"{get_timestamp()} - Scanning for targets to snipe...", end="\r")

        data = await fetch_data()
        if data:
            filtered = filter_data(data, seen_hashes)
            await display_transactions(reversed(filtered))

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
