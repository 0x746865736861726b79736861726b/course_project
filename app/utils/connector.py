from web3 import Web3


class BlockchainConnector:
    def __init__(self, url):
        self.w3 = Web3(Web3.HTTPProvider(url))

    def is_connected(self):
        """
        Check if the provider is connected.

        :return: True if the provider is connected, False otherwise.
        :rtype: bool
        """
        return self.w3.is_connected()

    def get_contract(self, contract_address, abi):
        """
        Get a contract instance from a given contract address and ABI.

        :param str contract_address: The address of the contract.
        :param list abi: The ABI of the contract.
        :return: A contract instance.
        :rtype: web3.eth.Contract
        """
        contract_address = self.w3.to_checksum_address(contract_address)
        return self.w3.eth.contract(address=contract_address, abi=abi)
