// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract UsersContract {
    address public Owner;
    enum Roles {None, User, Admin}

    struct User {
        address account;
        Roles role;
        uint createdAt; 
        bytes32 userId;
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

    event UserCreated(address indexed account, Roles role, bytes32 userId);
    event RoleAssigned(address indexed account, Roles role);
    event UserUpdated(address indexed account, Roles role);  // Подія для оновлення

    constructor() {
        Owner = msg.sender;
        bytes32 ownerId = keccak256(abi.encodePacked(msg.sender, block.timestamp));
        users[msg.sender] = User(msg.sender, Roles.Admin, block.timestamp, ownerId);
        userAddresses.push(msg.sender);
        emit UserCreated(msg.sender, Roles.Admin, ownerId);
    }

    function createUser(address _account, Roles _role) public onlyAdmin {
        require(_role != Roles.None, "Invalid role");
        require(users[_account].account == address(0), "User already exists");

        bytes32 newUserId = keccak256(abi.encodePacked(_account, block.timestamp));
        
        users[_account] = User(_account, _role, block.timestamp, newUserId);
        userAddresses.push(_account);

        emit UserCreated(_account, _role, newUserId);
    }

    function assignRole(address _account, Roles _role) public onlyAdmin {
        require(users[_account].account != address(0), "User does not exist");
        users[_account].role = _role;
        emit RoleAssigned(_account, _role);
    }

    function updateUser(address _account, Roles _role) public onlyAdmin {
        require(users[_account].account != address(0), "User does not exist");
        require(_role != Roles.None, "Invalid role");

        users[_account].role = _role;  
        emit UserUpdated(_account, _role);
    }

    function removeUser(address _account) public onlyAdmin {
        delete users[_account];
    }

    function getUserRole(address _account) public view returns (Roles) {
        return users[_account].role;
    }

    function getUserCreationDate(address _account) public view returns (uint) {
        return users[_account].createdAt;
    }

    function getUserId(address _account) public view returns (bytes32) {
        return users[_account].userId; 
    }

    function getAllUsers() public view returns (address[] memory, Roles[] memory, uint[] memory, bytes32[] memory) {
        Roles[] memory roles = new Roles[](userAddresses.length);
        uint[] memory creationDates = new uint[](userAddresses.length); 
        bytes32[] memory userIds = new bytes32[](userAddresses.length);

        for (uint i = 0; i < userAddresses.length; i++) {
            roles[i] = users[userAddresses[i]].role;
            creationDates[i] = users[userAddresses[i]].createdAt; 
            userIds[i] = users[userAddresses[i]].userId; 
        }

        return (userAddresses, roles, creationDates, userIds); 
    }
}
