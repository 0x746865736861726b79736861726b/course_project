import json


class ABImanager:
    def __init__(self, path):
        """
        Initialize an ABImanager instance.

        :param str path: The path to the JSON file containing the ABI.
        """
        self.path = path
        self.abi = None

    def load(self):
        """
        Load the ABI from the JSON file at self.path.

        :return: The ABI as a list of dictionaries.
        :rtype: list
        """
        with open(self.path, "r") as f:
            abi_data = json.load(f)
            self.abi = abi_data.get("abi", [])
        return self.abi

    def get_abi(self):
        """
        Return the ABI as a list of dictionaries.

        If the ABI has not been loaded before, this method will load it
        from the JSON file at self.path.

        :return: The ABI as a list of dictionaries.
        :rtype: list
        """
        if self.abi is None:
            self.load()
        return self.abi
