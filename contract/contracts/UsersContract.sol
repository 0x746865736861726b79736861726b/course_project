// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract UsersContract {
    address public Owner;
    enum Roles {None, User, Admin}

    struct User {
        address account;
        Roles role;
    }

    mapping(address => User) public users;
    address[] public userAddresses;

    modifier onlySuperUser() {
        require(msg.sender == Owner, "Only Super User");
        _;
    }

    modifier onlyAdmin() {
        require(users[msg.sender].role == Roles.Admin, "Only admin can perform this");
        _;
    }

    event UserCreated(address indexed account, Roles role);
    event RoleAssigned(address indexed account, Roles role);

    constructor() {
        Owner = msg.sender;
        users[msg.sender] = User(msg.sender, Roles.Admin);
        userAddresses.push(msg.sender);
        emit UserCreated(msg.sender, Roles.Admin);
    }

    function createUser(address _account, Roles _role) public onlyAdmin {
        require(_role != Roles.None, "Invalid role");
        require(users[_account].account == address(0), "User already exists");

        users[_account] = User(_account, _role);
        userAddresses.push(_account);

        emit UserCreated(_account, _role);
    }

    function assignRole(address _account, Roles _role) public onlyAdmin {
        require(users[_account].account != address(0), "User does not exist");
        users[_account].role = _role;
        emit RoleAssigned(_account, _role);
    }

    function removeUser(address _account) public onlyAdmin {
        delete users[_account];
    }

    function getUserRole(address _account) public view returns (Roles) {
        return users[_account].role;
    }

    function getAllUsers() public view returns (address[] memory, Roles[] memory) {
        Roles[] memory roles = new Roles[](userAddresses.length);

        for (uint i = 0; i < userAddresses.length; i++) {
            roles[i] = users[userAddresses[i]].role;
        }

        return (userAddresses, roles);
    }
}
