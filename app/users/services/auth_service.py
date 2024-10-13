from loguru import logger

from web3 import Web3
from eth_account.messages import encode_defunct

from users.exceptions.user_exceptions import (
    UserNotRegisteredError,
)
from users.exceptions.signature_exeptions import InvalidSignatureError


class AuthService:
    def __init__(self, user_manager, signature_verifier):
        self.user_manager = user_manager
        self.signature_verifier = signature_verifier

    def authenticate_user(self, user_address, signature, message):
        """
        Authenticates the user based on the account address and signature.

        :param str user_address: The Ethereum address of the user.
        :param str signature: The signature from the user.
        :param str message: The original message that was signed.
        :return: The user's role if authenticated.
        :raises UserNotRegisteredError: If the user is not registered in the smart contract.
        :raises InvalidSignatureError: If the signature is invalid.
        """
        user_address_checksum = Web3.to_checksum_address(user_address)
        message_encoded = encode_defunct(text=message)

        if not self.signature_verifier.verify_signature(
            user_address_checksum, signature, message_encoded
        ):
            logger.warning(f"Invalid signature for user {user_address_checksum}")
            raise InvalidSignatureError("Invalid signature.")

        role = self.user_manager.get_user_role(user_address_checksum)
        if role is None:
            logger.warning(f"User {user_address_checksum} not found in contract.")
            raise UserNotRegisteredError("Address not registered in the contract.")

        logger.info(f"User {user_address_checksum} authenticated with role {role}")
        return role
