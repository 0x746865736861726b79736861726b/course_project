from django.conf import settings

from utils.loader import ABImanager
from utils.connector import BlockchainConnector
from users.services.user_manager import UserManager
from users.services.contract_client import ContractClient


def get_user_manager():
    abi_manager = ABImanager(settings.CONTRACT_ABI_PATH)
    contract_abi = abi_manager.get_abi()
    blockchain_connector = BlockchainConnector(settings.ETHEREUM_NODE_URL)
    contract_client = ContractClient(
        blockchain_connector, settings.CONTRACT_ADDRESS, contract_abi
    )
    return UserManager(contract_client)
