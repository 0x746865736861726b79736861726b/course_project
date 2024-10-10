class UserManager:
    def __init__(self, contract_client):
        self.contract_client = contract_client

    def create_user(self, account, role, private_key):
        transaction = self.contract_client.build_transaction(
            "createUser", [account, role], account
        )
        receipt = self.contract_client.send_transaction(transaction, private_key)
        return receipt

    def get_user_role(self, account):
        return self.contract_client.call_function("getUserRole", [account])
