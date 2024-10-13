from django.conf import settings

from utils.loader import ABImanager
from utils.connector import BlockchainConnector
from users.services.auth_service import AuthService
from users.services.user_manager import UserManager
from users.services.contract_client import ContractClient
from users.utils.signature_verifier import SignatureVerifier


def get_user_manager():
    """
    Return an instance of UserManager, which wraps the ContractClient and
    provides services for managing users.
    """
    abi_manager = ABImanager(settings.CONTRACT_ABI_PATH)
    contract_abi = abi_manager.get_abi()
    blockchain_connector = BlockchainConnector(settings.ETHEREUM_NODE_URL)
    contract_client = ContractClient(
        blockchain_connector, settings.CONTRACT_ADDRESS, contract_abi
    )
    return UserManager(contract_client)


def get_auth_service():
    """
    Create and return an instance of AuthService.
    """
    user_manager = get_user_manager()
    signature_verifier = SignatureVerifier()
    return AuthService(user_manager, signature_verifier)
