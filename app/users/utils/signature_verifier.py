from loguru import logger
from eth_account import Account


class SignatureVerifier:
    @staticmethod
    def verify_signature(user_address, signature, message):
        """
        Verifies the user's signature against the given message.

        :param str user_address: The Ethereum address of the user.
        :param str signature: The signature from the user.
        :param str message: The original message that was signed.
        :return: True if the signature is valid, else False.
        """
        try:
            recovered_address = Account.recover_message(message, signature=signature)
            return recovered_address.lower() == user_address.lower()
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False
