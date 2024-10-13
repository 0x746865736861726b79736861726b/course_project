class ContractClient:
    def __init__(self, blockchain_connector, contract_address, abi):
        """
        :param BlockchainConnector blockchain_connector:
        :param str contract_address:
        :param list abi:
        """
        self.connector = blockchain_connector
        self.contract = self.connector.get_contract(contract_address, abi)

    def build_transaction(self, function_name, args, sender):
        """
        Builds a transaction for the given function with the given arguments.

        :param str function_name:
        :param list args:
        :param str sender:
        :return: The transaction
        :rtype: dict
        """
        nonce = self.connector.w3.eth.get_transaction_count(sender)
        transaction = getattr(self.contract.functions, function_name)(
            *args
        ).build_transaction(
            {
                "from": sender,
                "nonce": nonce,
                "gas": 2000000,
                "gasPrice": self.connector.w3.to_wei("20", "gwei"),
            }
        )
        return transaction

    def send_transaction(self, transaction, private_key):
        """
        Sends the given transaction with the given private key.

        :param dict transaction: The transaction (in dict form)
        :param str private_key: The private key to use for signing
        :return: The transaction receipt
        :rtype: dict
        """
        signed_tx = self.connector.w3.eth.account.sign_transaction(
            transaction, private_key=private_key
        )
        tx_hash = self.connector.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = self.connector.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def call_function(self, function_name, args):
        """
        Calls the given function on the contract with the given arguments.

        :param str function_name: The name of the function to call
        :param list args: The arguments to pass to the function
        :return: The result of the function call
        :rtype: Any
        """
        return getattr(self.contract.functions, function_name)(*args).call()
