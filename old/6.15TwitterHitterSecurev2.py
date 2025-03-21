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

# testing 12/20

load_dotenv()

accounts = [
    {
        "username": os.getenv("TWIT1"),
        "password": os.getenv("TWIT1_PASSWORD"),
        "otp_key": os.getenv("TWIT1_OTP_KEY"),
    },
    {
        "username": os.getenv("TWIT2"),
        "password": os.getenv("TWIT2_PASSWORD"),
        "otp_key": os.getenv("TWIT2_OTP_KEY"),
    },
]
try:
    twi = Twitter("session")
except Exception:
    os.remove("session.tw_session")
    twi = Twitter("session")

account = random.choice(accounts)
print("Using: %s" % account["username"])

totp = pyotp.TOTP(account["otp_key"])
otp = totp.now()

twi.sign_in(account["username"], account["password"], extra=otp)

streamer_follower_data = {}

api_url = "https://sanko.tv/api/streams/activity"
contract_address = "0x06f1afa00990A69cA03F82D4c1A3a64A45F45fCb"
referrer = "0xE3983FeA05c4F4a7Bf7DC37c04f55Cb610B4C3BD"

alchemy_api_key = os.getenv("ALCHEMY_API_KEY")
my_address = os.getenv("DEGENSCAPER_ADDRESS")
private_key = os.getenv("DEGENSCAPER_PK")

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

TARGET_SET = {
    "PhewphR",
    "gucciprayers",
    "shelbyaaaaa",
    "starchild_eth",
    "venerate__",
    "paaaaaaaaancake",
    "FreshlobsterC",
    "_ck007",
    "Kawatek_CG",
    "AliasVEDH",
    "DeraJN",
    "Nohandsgamer",
    "thegangsterofl2",
    "TheoHS_",
    "x__poet",
    "G2Thijs",
    "RduStreaming",
    "Lifecoach1981",
    "tylerootd",
    "FenoHS",
    "degeneratefuq",
    "Mothalamp",
    "BillSPACman",
    "lb_dobis",
    "trading_dojo",
    "shishi520_",
    "thedrsuss",
    "Lors_eth",
    "ThreadGirl_eth",
    "cryptotriv",
    "Bonk_Blofin",
    "MissionGains",
    "buildabera",
    "8Guru888",
    "ByteSizedAliza",
    "mochains",
    "notapornfolder_",
    "BloomCapital_",
    "RoofHanzo",
    "ChrisCoffeeEth",
    "adamscochran",
    "CryptoNinjaah",
    "JackAdams66",
    "smol_intern",
    "avocado_toast2",
    "BasedShillBH",
    "ares20k",
    "yueko__",
    "marcusmoles",
    "Greti_eth",
    "OGFaZeCLipZ",
    "ohnePixel",
    "0xTerence",
    "Noirtueur9999",
    "ZhuoxunYin",
    "venturespencer",
    "JARVIS_nfts",
    "dachshundwizard",
    "qbpick",
    "printer_brrr",
    "resaang",
    "Mortpoker",
    "mxryboo",
    "topshotfund",
    "SLiNGOOR",
    "screentimes",
    "knveth",
    "brentradess",
    "fizzlestixx5217",
    "MagusWazir",
    "GardenofDegens",
    "quangocracy",
    "0xkotto",
    "loomlocknft",
    "bywassies",
    "0xlogy",
    "LilGhostyBear",
    "SadeBaeza",
    "GianTheRios",
    "sui414",
    "rootslashbin",
    "0xSoDank",
    "0xbagelface",
    "DailaDotEth",
    "KenobiDesigns",
    "Glug69420",
    "0xYelf",
    "bettor_eth",
    "niftyq_",
    "W3BTHR33",
    "gifdead",
    "optimizoor",
    "painkillerbill",
    "0gcrypt0",
    "BBMondo55",
    "seasonofterror",
    "nemusonaUwU",
    "MySchtyle",
    "0xShual",
    "solminingpunk",
    "jimbol14",
    "gatsXBT",
    "craigscoinpurse",
    "DivineProvdence",
    "0xRaiden",
    "0xG00gly",
    "PC_Larp",
    "focaballena",
    "grimy_trades",
    "templecrash",
    "cryptoaioli",
    "MadameMage",
    "TheRogueItachi",
    "deepfates",
    "heyhaigh",
    "cellar_gg",
    "SpymiIk",
    "redhairshanks86",
    "luxecrypto_club",
    "poordart",
    "melabeeofficial",
    "midgirlfriend",
    "inhuman",
    "djackby9",
    "0xMadeleinee",
    "LordJamieVShiLL",
    "degentalks",
    "jjaymay",
    "dapersiantrader",
    "betafuzz",
    "scorpioblxck",
    "canter",
    "phuktep",
    "TheMIDWave_",
    "Web3_Emily",
    "Carsonated",
    "painXBT",
    "tempst0",
    "realbatdad",
    "cooItimes",
    "Fade",
    "y2k_mischief",
    "BisharaDOTeth",
    "EAT_InSaNiTy",
    "inth3mud",
    "exitIiquidity",
    "SmolPonzi",
    "radGouL",
    "RetardedATH",
    "BurrntDotETH",
    "basedtroy",
    "Tree_of_Alpha",
    "News_Of_Alpha",
    "jimtalbot",
    "abetrade",
    "breakoutprop",
    "Awawat_Trades",
    "0xVKTR",
    "idexio",
    "orionterminal",
    "PC_PR1NCIPAL",
    "The_LoA_Podcast",
    "fomocapdao",
    "Husslin_",
    "CryptoParadyme",
    "TraderMercury",
    "depression2019",
    "tradinglord",
    "kollectiv_io",
    "KAPOTHEGOAT01",
    "paidgroupxbt",
    "Ritesh_Trades",
    "skynetcap",
    "arcanamarkets",
    "openbookdex",
    "zoomerfied",
    "KuroXLB",
    "HiddenStreetCap",
    "CryptoWizardd",
    "Nostradumbass23",
    "jebus911",
    "exitpumpBTC",
    "Bybit_Official",
    "STFX_IO",
    "0xJezza",
    "RookieXBT",
    "magnetmoneyshow",
    "ShardiB2",
    "smardex",
    "bingxofficial",
    "Tradingalpha_",
    "Anbessa100",
    "RevanchistLiqd",
    "mechanismcap",
    "PleasrDAO",
    "Pool2Paulie",
    "willoptions",
    "pvpterminal",
    "CryptoHornHairs",
    "trading_axe",
    "joshnomics",
    "LSDinmycoffee",
    "52kskew",
    "ApeDurden",
    "0x_Leo_",
    "bulltrapper0",
    "Dentoshi",
    "docXBT",
    "0xNBS",
    "naniXBT",
    "TraderMotif",
    "TheParagonGrp",
    "NachoTrades",
    "TheHavenCrypto",
    "kingfisher_btc",
    "VeloData",
    "TylerDurden",
    "trybetterbrand",
    "DrChrisPharmD",
    "TheClinic_",
    "conzimp",
    "AngeloBTC",
    "apg_capital",
    "partyhatDAO",
    "ArtPatsi",
    "panaphud",
    "Kr3py",
    "VibezDao",
    "Dupe_fi",
    "Theft",
    "tradingdojo",
    "LawliettesLab",
    "uvocapital",
    "xbtGBH",
    "Abu9ala7",
    "nyocollective",
    "weetardsdao",
    "0xbones6",
    "TokyoSunbather",
    "RemiliaRabbi",
    "XLMV3",
    "ehrxbt",
    "S117doteth",
    "0xSpot",
    "g3_capital",
    "Le_Zealous",
    "thecryptojourno",
    "0xwonel",
    "CryptoSwiss827",
    "nanoppai_jp",
    "udlfus",
    "reepzNFT",
    "0xIchigo",
    "BIueNinja",
    "titziwitzi",
    "0xfreshed",
    "Pseud0Anon",
    "mememe69696969",
    "bankrowl",
    "0xrhova",
    "NEET_poster",
    "CaramelCoffee8",
    "frogfrogfren",
    "TheReviken",
    "soldmytears",
    "nuanua404",
    "MILADYCITY",
    "FrenMilady",
    "kblune_",
    "0xwodden",
    "0xbobateas",
    "asap0x",
    "tessier_mf",
    "PLUSPLUSEV",
    "miIady68",
    "sibeleth",
    "lil_cpu",
    "0x5D_8F",
    "kozue__777",
    "crypt1ck",
    "Ron1nCrypto",
    "blyatzkrieg",
    "holycryptoroni",
    "witthefanta",
    "fruits4clipper",
    "RuleWhole",
    "0xMogluc",
    "thiccnoggin",
    "PinkSarcophagus",
    "0xjrey",
    "autistic_front",
    "aaaahwaaahnuuuu",
    "Hustle_Grinder",
    "EmmaJamesTweet",
    "lilbaby_fan",
    "leadingains",
    "lambda0xE",
    "ottnaj",
    "gera_eth",
    "rikuthinks",
    "miladycore",
    "anloremi",
    "apixtwts",
    "lowercaseboot",
    "Hercqlit",
    "shampoo_capital",
    "Analytic_ETH",
    "Hab1btc",
    "fandeathvictim",
    "relativeread",
    "PirateFinance",
    "brglover2",
    "yungdoteth",
    "RAnSacks",
    "MiladyMumble",
    "boris_adimov",
    "ohgoshakash",
    "JohnMGhost7",
    "tannishmango",
    "littel_wolfur",
    "RambleGambleEsq",
    "jimjim_eth",
    "sisterxue",
    "k2_nft",
    "0xAlec",
    "femmebotx7",
    "Kristian_cy",
    "shxikxz",
    "quake_champio",
    "spicegirleth",
    "McbMcb59326793",
    "c____aterpillar",
    "birdmademejoin",
    "buyingyourstops",
    "0x_d24",
    "mushmoonz",
    "kalo_nazih",
    "an11000000",
    "capybaraonchain",
    "sshk3n",
    "mikeneuder",
    "p4kao",
    "cbtxbt",
    "0xTaoSu",
    "binky5x5",
    "RAYBEAZY",
    "JamesTh56209952",
    "MasterChanX",
    "kmldot",
    "MLeeJr",
    "mfer1668",
    "hoodiemfer",
    "sartoshi_rip",
    "_nngmi",
    "awerawert",
    "OnTheBull",
    "maniacmfer",
    "minibossgrl",
    "AnotherMFerFren",
    "HeresMyEth",
    "sartocrates",
    "grdenrr",
    "windF_nft_mfers",
    "SAL_BIAnalytics",
    "BluebirdX11",
    "expectmfers",
    "JohnnyCash4243",
    "seandoteth",
    "marcokkkkkkk",
    "mrhammink",
    "mfer8023",
    "everydaymfer",
    "the_imp0ster",
    "ishkeener",
    "MinisterOfNFTs",
    "mfer7166",
    "bullrun20212",
    "matthewvarnell",
    "0xzeroi",
    "jpegmfer",
    "breezy_996",
    "Striker5962",
    "0xSThompson",
    "AshiBons",
    "dappwizard",
    "PrincessDEFI",
    "amigoenmi",
    "sartoshi_junior",
    "richmfer_nft",
    "saltymfer",
    "Touchemontoch",
    "NomadShev",
    "chimpanchz",
    "BabbleCrypto",
    "JpegsWill",
    "BO8CAT",
    "illiquidplays",
    "baobaotoshi",
    "lexnfts",
    "Sartoodles",
    "jiggyboy_eth",
    "Matlok42",
    "deeg631",
    "McEggPro",
    "tslicecrypto",
    "LugoonNFT",
    "mferpapi",
    "MeltedMindz",
    "okamiETH",
    "InflatableBag",
    "HodlerJerry",
    "dirk_crypto",
    "yieldfarmer420",
    "ComancheTippie",
    "atrandomguy",
    "EtherGlassPink",
    "SirRamboPhilthy",
    "jasonbisson",
    "surfsyfafo",
    "0xBoop",
    "glockwithdot",
    "fjuuus",
    "adeedao",
    "sgpmfer",
    "ZilchedHash",
    "ExaminerMo",
    "Aliza46507335",
    "ach245",
    "mferverse",
    "Ewani",
    "VisnuSathia",
    "_seacasa",
    "RACHWISEnft",
    "Paco420_",
    "flonsch98",
    "Caniac_Garv",
    "TediumCrypto",
    "Doobrexofficial",
    "CosmicSam_eth",
    "funnymonkey_eth",
    "zonkoooo",
    "mferBuildsAi",
    "Viktec420_69",
    "0xLawl",
    "kostas_siamp",
    "SpaceKelvin",
    "0xChico_eth",
    "Crouserrr",
    "Gautamguptagg",
    "cozypront",
    "dottaikodomains",
    "NFTDoctor33",
    "_kidrah_24",
    "SOLBigBrain",
    "SolanaSensei",
    "jords",
    "leshka_eth",
    "3orovik",
    "NDIDI_GRAM",
    "MadLadsNFT",
    "yellowpantherx",
    "spacepixel",
    "tofushit888",
    "degenrory",
    "SolJakey",
    "knox_trades",
    "BuildOnBase",
    "sol_nxxn",
    "Abrahamchase09",
    "crypto__kermit",
    "DeRonin_",
    "armaniferrante",
    "MagicDegenSOL",
    "rainascrd",
    "meriahsmith1",
    "koolk123456",
    "CyberKongz",
    "S4mmyEth",
    "huntersolaire_",
    "Atitty_",
    "retiredchaddev",
    "SolportTom",
    "nftmufettisi",
    "SOLbuckets",
    "khurrylicious",
    "ix_wilson",
    "notashenone",
    "patty_fi",
    "watchking69",
    "lostsol404",
    "0xMubeenn",
    "ordinalswallet",
    "Scrambller66",
    "Pickle_cRypto",
    "MonkDoesnt",
    "0xFrisk",
    "asedd72",
    "NFTGUYY",
    "decircusmaster",
    "Legendary_NFT",
    "fwTyo",
    "chikkori3",
    "PedroALPHAA",
    "urbrobecc",
    "SwegServices",
    "0itsali0",
    "FerreNFT",
    "thegreatola",
    "EasyEatsBodega",
    "BozoCollective",
    "JerzyNFT",
    "iamDCinvestor",
    "shivst3r",
    "PixSorcerer",
    "NemoJonw3",
    "WisdomMatic",
    "coopernicus01",
    "zayn4pf",
    "bsheng829",
    "yver__",
    "DaoKwonDo",
    "oCalebSol",
    "Attis_gaming",
    "DSentralized",
    "0xSweep",
    "Solana_Emperor",
    "TobiWebIII",
    "nifemi369",
    "JeremyyNFT",
    "LucaNetz",
    "PrimordialAA",
    "cryptopunksnfts",
    "punk6529",
    "gmoneyNFT",
    "DeeZe",
    "farokh",
    "richerd",
    "RaoulGMI",
    "VonMises14",
    "econoar",
    "chriscantino",
    "santiagoroel",
    "alexarnault",
    "CryptoNovo311",
    "kaiynne",
    "Debussy100",
    "0xRodo",
    "2Yeahyeah",
    "0xTechno",
    "SKYCRYPTOBOOMER",
    "JohnKnopfPhotos",
    "matthall2000",
    "mrforevernft",
    "ZAGABOND",
    "dingalingts",
    "locationtba",
    "IcedcoffeeEth",
    "Bamedi_",
    "andr3w",
    "emilyrosemcg",
    "its_kiki_hehe",
    "iamashchild",
    "latteshelby",
    "vyvvyn",
    "0xSeraph_",
    "2pmflow",
    "whizwang",
    "LeviNotAckerman",
    "illumanbeing",
    "Rewkang",
    "konger_eth",
    "EvaAzuki",
    "NFTooPerfect",
    "aetherfloweth",
    "SunwayIKZ",
    "AzukiFable",
    "hoshiboyzen",
    "ElenaaETH",
    "samuelgildas",
    "Kevin306780",
    "KatsuCompany",
    "kinnnnnnn_____",
    "graildoteth",
    "NickAzuki",
    "the__eeb",
    "0xKirara",
    "kiriragi",
    "SamuraiSpirit88",
    "tubsthetroll",
    "SteveG60117",
    "a1rportEth",
    "juniverseNFT",
    "bonzenitsuki",
    "Csaw07",
    "amplice_eth",
    "The_BigFrank",
    "timechains",
    "colingplatt",
    "basedghoulbot",
    "pedro_bruder",
    "chondiis",
    "Degenyfi",
    "dnkta",
    "0xremedial",
    "ChopsDan",
    "0x0_Lam",
    "RobinWhitney_",
    "jrdsctt",
    "rootdraws",
    "happystake",
    "0xDead4eth",
    "yyolk",
    "freakcertifier",
    "athermant",
    "bl0ckpain",
    "jb0x_",
    "remilio64",
    "CoinGeico",
    "scrantly",
    "PoloNWO",
    "djpuzzleb0x",
    "endewed",
    "RetardedVeteran",
    "0xBumps",
    "harblinger_eth",
    "maximum_habibi",
    "RemilioTrader",
    "undeadcat1or0",
    "portport255",
    "NotFinTech",
    "0xPrasclo",
    "GenuineUndead",
    "tMAIS0N",
    "TheGenuineTimes",
    "Liquidity_Art",
    "CYBERDEMON6669",
    "alex69xeth",
    "UN1536",
    "0x1hockeynut",
    "Vecktooor",
    "NeoMerlinX",
    "Yieldasaurus",
    "vs_investor",
    "phaaz",
    "memedropzone",
    "skatanxx",
    "EROSdzn",
    "mydailyfantasy",
    "434tech",
    "BITCOIN",
    "JohnsonYau4",
    "edos189",
    "vydamo_",
    "Drewso22",
    "TLM_Crypto",
    "stormrdoteth",
    "CookieLoverNFT",
    "Stuffguy_eth",
    "sealgoodman",
    "K__flame",
    "underratedTC",
    "BigM33sh",
    "Sharpp",
    "wandurz",
    "CryptoEmpire11",
    "ZanZai74",
    "RoamDAO",
    "mattzahab",
    "mwilcox",
    "heartornament",
    "8noblest",
    "0xHashy",
    "mung0x",
    "Web3Adam",
    "ItsAditya_xyz",
}


# assumes supply 1,2,3 have been bought
LEGENDARY_BUY_PARAMS = {
    3: {"amount": 7, "eth": "0.01965425"},
    4: {"amount": 6, "eth": "0.01902251"},
    5: {"amount": 5, "eth": "0.01789941"},
    6: {"amount": 4, "eth": "0.01614456"},
    7: {"amount": 3, "eth": "0.01361759"},
    8: {"amount": 2, "eth": "0.01017809"},
    9: {"amount": 1, "eth": "0.00568569"},
}

# assumes supply 1,2,3 have been bought
BULLSEYE_BUY_PARAMS = {
    3: {"amount": 5, "eth": "0.00947616"},
    4: {"amount": 4, "eth": "0.00884441"},
    5: {"amount": 3, "eth": "0.00772131"},
    6: {"amount": 2, "eth": "0.00596647"},
    7: {"amount": 1, "eth": "0.00343949"},
}

# assumes supply 1,2,3 have been bought
TARGET_BUY_PARAMS = {
    3: {"amount": 3, "eth": "0.00350969"},
    4: {"amount": 2, "eth": "0.00287794"},
    5: {"amount": 1, "eth": "0.00175484"},
}

# buys are based on available supply
SMOL_BUY_PARAMS = {
    3: {"amount": 2, "eth": "0.00182504"},
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


def add_to_blacklist(username):
    with open("blacklist.txt", "a") as file:
        file.write("\n" + username.lower())


def load_blacklist():
    try:
        with open("blacklist.txt", "r") as file:
            return {line.strip().lower() for line in file}
    except FileNotFoundError:
        return set()


async def purchase_passes(streamer_address, streamer_username, amount, price):
    checksummed_streamer_address = Web3.to_checksum_address(streamer_address)
    total_eth_to_send = w3.to_wei(str(price), "ether")
    packed_args = contract.functions.packArgs(
        {"amount": amount, "addy": referrer}
    ).call()
    transaction = contract.functions.buyPasses(
        checksummed_streamer_address, packed_args
    ).buildTransaction(
        {
            "chainId": 42161,
            "gas": 2200069,
            "maxPriorityFeePerGas": w3.to_wei("4", "gwei"),
            "maxFeePerGas": w3.to_wei("4", "gwei"),
            "nonce": w3.eth.get_transaction_count(my_address),
            "value": total_eth_to_send,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(get_timestamp(), end=" - ")
    print(
        f"sniping {amount} passes for {checksummed_streamer_address} - txn hash: {txn_hash.hex()}"
    )

    loop = asyncio.get_running_loop()
    receipt = await loop.run_in_executor(
        None, w3.eth.wait_for_transaction_receipt, txn_hash
    )

    arbiscan_link = f"https://arbiscan.io/tx/{txn_hash}"
    if receipt.status:
        print(get_timestamp(), end=" - ")
        print(colored(f"txn {txn_hash.hex()} was successful!", "green"))
        log_transaction("Hit", arbiscan_link)
        add_to_blacklist(streamer_username)
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


async def display_transactions(transactions, blacklist):
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
        if streamer_username.lower() not in blacklist:
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
                elif follower_count > 10000:
                    buy_params = TARGET_BUY_PARAMS.get(supply)
                elif follower_count > 5000:
                    buy_params = SMOL_BUY_PARAMS.get(supply)

        if buy_params:
            success = await purchase_passes(
                streamer_address,
                streamer_username,
                buy_params["amount"],
                buy_params["eth"],
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
    blacklist = load_blacklist()
    while True:
        print(f"{get_timestamp()} - Scanning for targets to snipe...", end="\r")
        data = await fetch_data()
        if data:
            filtered = filter_data(data, seen_hashes)
            await display_transactions(reversed(filtered), blacklist)
        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
