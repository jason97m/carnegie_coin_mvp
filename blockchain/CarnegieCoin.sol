// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CarnegieCoin {
    string public name = "Carnegie Coin";
    string public symbol = "CC";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply;
        // Required ERC20 mint event:
        emit Transfer(address(0), msg.sender, _initialSupply);
    }

    function transfer(address _to, uint256 _amount) public returns (bool) {
        require(balanceOf[msg.sender] >= _amount, "Not enough balance");
        balanceOf[msg.sender] -= _amount;
        balanceOf[_to] += _amount;
        // Required ERC20 transfer event:
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
}
