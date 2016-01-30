import sys
import logging
from urllib.parse import quote_plus as urlencode

from shellpartylib.lib import config, script
from shellpartycli import util
from shellpartycli import wallet
from shellpartycli import messages
from shellpartycli.messages import get_pubkeys

logger = logging.getLogger()

DEFAULT_REQUESTS_TIMEOUT = 5 # seconds

class ConfigurationError(Exception):
    pass

def initialize(testnet=False, testcoin=False,
                shellparty_rpc_connect=None, shellparty_rpc_port=None, 
                shellparty_rpc_user=None, shellparty_rpc_password=None,
                shellparty_rpc_ssl=False, shellparty_rpc_ssl_verify=False,
                wallet_name=None, wallet_connect=None, wallet_port=None, 
                wallet_user=None, wallet_password=None,
                wallet_ssl=False, wallet_ssl_verify=False,
                requests_timeout=DEFAULT_REQUESTS_TIMEOUT):

    def handle_exception(exc_type, exc_value, exc_traceback):
        logger.error("Unhandled Exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception

    # testnet
    config.TESTNET = testnet or False

    # testcoin
    config.TESTCOIN = testcoin or False

    ##############
    # THINGS WE CONNECT TO

    # Server host (Shellcoin Core)
    config.SCHPARTY_RPC_CONNECT = shellparty_rpc_connect or 'localhost'

    # Server RPC port (Shellcoin Core)
    if shellparty_rpc_port:
        config.SCHPARTY_RPC_PORT = shellparty_rpc_port
    else:
        if config.TESTNET:
            config.SCHPARTY_RPC_PORT = config.DEFAULT_RPC_PORT_TESTNET
        else:
            config.SCHPARTY_RPC_PORT = config.DEFAULT_RPC_PORT
    try:
        config.SCHPARTY_RPC_PORT = int(config.SCHPARTY_RPC_PORT)
        if not (int(config.SCHPARTY_RPC_PORT) > 1 and int(config.SCHPARTY_RPC_PORT) < 65535):
            raise ConfigurationError('invalid RPC port number')
    except:
        raise Exception("Please specific a valid port number shellparty-rpc-port configuration parameter")

    # Server RPC user (Shellcoin Core)
    config.SCHPARTY_RPC_USER = shellparty_rpc_user or 'rpc'

    # Server RPC password (Shellcoin Core)
    if shellparty_rpc_password:
        config.SCHPARTY_RPC_PASSWORD = shellparty_rpc_password
    else:
        config.SCHPARTY_RPC_PASSWORD = None

    # Server RPC SSL
    config.SCHPARTY_RPC_SSL = shellparty_rpc_ssl or False  # Default to off.

    # Server RPC SSL Verify
    config.SCHPARTY_RPC_SSL_VERIFY = shellparty_rpc_ssl_verify or False # Default to off (support self‐signed certificates)

    # Construct server URL.
    config.SCHPARTY_RPC = config.SCHPARTY_RPC_CONNECT + ':' + str(config.SCHPARTY_RPC_PORT)
    if config.SCHPARTY_RPC_PASSWORD:
        config.SCHPARTY_RPC = urlencode(config.SCHPARTY_RPC_USER) + ':' + urlencode(config.SCHPARTY_RPC_PASSWORD) + '@' + config.SCHPARTY_RPC
    if config.SCHPARTY_RPC_SSL:
        config.SCHPARTY_RPC = 'https://' + config.SCHPARTY_RPC
    else:
        config.SCHPARTY_RPC = 'http://' + config.SCHPARTY_RPC
    config.SCHPARTY_RPC += '/rpc/'

    # SCH Wallet name
    config.WALLET_NAME = wallet_name or 'SatoshiChaincore'

    # SCH Wallet host
    config.WALLET_CONNECT = wallet_connect or 'localhost'

    # SCH Wallet port
    if wallet_port:
        config.WALLET_PORT = wallet_port
    else:
        if config.TESTNET:
            config.WALLET_PORT = config.DEFAULT_BACKEND_PORT_TESTNET
        else:
            config.WALLET_PORT = config.DEFAULT_BACKEND_PORT
    try:
        config.WALLET_PORT = int(config.WALLET_PORT)
        if not (int(config.WALLET_PORT) > 1 and int(config.WALLET_PORT) < 65535):
            raise ConfigurationError('invalid wallet API port number')
    except:
        raise ConfigurationError("Please specific a valid port number wallet-port configuration parameter")

    # SCH Wallet user
    config.WALLET_USER = wallet_user or 'SatoshiChainrpc'

    # SCH Wallet password
    if wallet_password:
        config.WALLET_PASSWORD = wallet_password
    else:
        raise ConfigurationError('wallet RPC password not set. (Use configuration file or --wallet-password=PASSWORD)')

    # SCH Wallet SSL
    config.WALLET_SSL = wallet_ssl or False  # Default to off.

    # SCH Wallet SSL Verify
    config.WALLET_SSL_VERIFY = wallet_ssl_verify or False # Default to off (support self‐signed certificates)

    # Construct SCH wallet URL.
    config.WALLET_URL = urlencode(config.WALLET_USER) + ':' + urlencode(config.WALLET_PASSWORD) + '@' + config.WALLET_CONNECT + ':' + str(config.WALLET_PORT)
    if config.WALLET_SSL:
        config.WALLET_URL = 'https://' + config.WALLET_URL
    else:
        config.WALLET_URL = 'http://' + config.WALLET_URL

    config.REQUESTS_TIMEOUT = requests_timeout

    # Encoding
    if config.TESTCOIN:
        config.PREFIX = b'XX'                   # 2 bytes (possibly accidentally created)
    else:
        config.PREFIX = b'CNTRPRTY'             # 8 bytes

    # (more) Testnet
    if config.TESTNET:
        config.MAGIC_BYTES = config.MAGIC_BYTES_TESTNET
        if config.TESTCOIN:
            config.ADDRESSVERSION = config.ADDRESSVERSION_TESTNET
            config.BLOCK_FIRST = config.BLOCK_FIRST_TESTNET_TESTCOIN
            config.BURN_START = config.BURN_START_TESTNET_TESTCOIN
            config.BURN_END = config.BURN_END_TESTNET_TESTCOIN
            config.UNSPENDABLE = config.UNSPENDABLE_TESTNET
        else:
            config.ADDRESSVERSION = config.ADDRESSVERSION_TESTNET
            config.BLOCK_FIRST = config.BLOCK_FIRST_TESTNET
            config.BURN_START = config.BURN_START_TESTNET
            config.BURN_END = config.BURN_END_TESTNET
            config.UNSPENDABLE = config.UNSPENDABLE_TESTNET
    else:
        config.MAGIC_BYTES = config.MAGIC_BYTES_MAINNET
        if config.TESTCOIN:
            config.ADDRESSVERSION = config.ADDRESSVERSION_MAINNET
            config.BLOCK_FIRST = config.BLOCK_FIRST_MAINNET_TESTCOIN
            config.BURN_START = config.BURN_START_MAINNET_TESTCOIN
            config.BURN_END = config.BURN_END_MAINNET_TESTCOIN
            config.UNSPENDABLE = config.UNSPENDABLE_MAINNET
        else:
            config.ADDRESSVERSION = config.ADDRESSVERSION_MAINNET
            config.BLOCK_FIRST = config.BLOCK_FIRST_MAINNET
            config.BURN_START = config.BURN_START_MAINNET
            config.BURN_END = config.BURN_END_MAINNET
            config.UNSPENDABLE = config.UNSPENDABLE_MAINNET

WALLET_METHODS = [
    'get_wallet_addresses', 'get_shell_balances', 'sign_raw_transaction', 
    'get_pubkey', 'is_valid', 'is_mine', 'get_shell_balance', 'send_raw_transaction',
    'wallet', 'asset', 'balances', 'pending', 'is_locked', 'unlock', 'wallet_last_block'
]

def call(method, args, pubkey_resolver=None):
    """
        Unified function to call Wallet and Server API methods
        Should be used by applications like `shellparty-gui`

        :Example:

        import shellpartycli.clientapi
        clientapi.initialize(...)
        unsigned_hex = clientapi.call('create_send', {...}) 
        signed_hex =  clientapi.call('sign_raw_transaction', unsigned_hex)
        tx_hash = clientapi.call('send_raw_transaction', signed_hex)
    """
    if method in WALLET_METHODS:
        func = getattr(wallet, method)
        return func(**args)
    else:
        if method.startswith('create_'):
            # Get provided pubkeys from params.
            pubkeys = []
            for address_name in ['source', 'destination']:
                if address_name in args:
                    address = args[address_name]
                    if script.is_multisig(address) or address_name != 'destination':    # We don’t need the pubkey for a mono‐sig destination.
                        pubkeys += get_pubkeys(address, pubkey_resolver=pubkey_resolver)
            args['pubkey'] = pubkeys

        result = util.api(method, args)

        if method.startswith('create_'):
            messages.check_transaction(method, args, result)

        return result


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
