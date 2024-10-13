const UsersContact = artifacts.require("UsersContract");

module.exports = function (deployer) {
    deployer.deploy(UsersContact, { gas: 6721975 });
}