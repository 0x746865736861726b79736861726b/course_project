class UserManager:
    def __init__(self, contract_client):
        """
        Initializes a UserManager instance.

        :param contract_client: A contract client connected to the UsersContract
        :type contract_client: eth_client.EthClient
        """

        self.contract_client = contract_client

    def create_user(self, account, role, private_key):
        """
        Creates a new user with the given account and role.

        :param str account: The address of the new user
        :param int role: The role of the new user
        :param str private_key: The private key to use for signing
        :return: The transaction receipt
        :rtype: dict
        """

        transaction = self.contract_client.build_transaction(
            "createUser", [account, role], account
        )
        receipt = self.contract_client.send_transaction(transaction, private_key)
        return receipt

    def get_user_role(self, account):
        """
        Returns the role of the user at the given account.

        :param str account: The address of the user
        :return: The role of the user
        :rtype: int
        """
        return self.contract_client.call_function("getUserRole", [account])

    def get_all_users(self):
        user_details = []
        user_addresses, user_role = self.contract_client.call_function(
            "getAllUsers", []
        )
        for address, role in zip(user_addresses, user_role):
            user_details.append({"account": address, "role": role})

        return user_details
