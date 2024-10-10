class ContractClient:
    def __init__(self, blockchain_connector, contract_address, abi):
        self.connector = blockchain_connector
        self.contract = self.connector.get_contract(contract_address, abi)

    def build_transaction(self, function_name, args, sender):
        nonce = self.connector.w3.eth.get_transaction_count(sender)
        transaction = getattr(self.contract.functions, function_name)(
            *args
        ).build_transaction(
            {
                "from": sender,
                "nonce": nonce,
                "gas": 2000000,
                "gasPrice": self.connector.w3.toWei("20", "gwei"),
            }
        )
        return transaction

    def send_transaction(self, transaction, private_key):
        signed_tx = self.connector.w3.eth.account.sign_transaction(
            transaction, private_key=private_key
        )
        tx_hash = self.connector.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.connector.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def call_function(self, function_name, args):
        return getattr(self.contract.functions, function_name)(*args).call()
