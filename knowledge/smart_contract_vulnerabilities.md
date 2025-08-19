# Smart Contract Security Vulnerabilities Reference

## SWC-107: Reentrancy

**Description:** One of the most critical vulnerabilities in smart contracts. Occurs when a contract calls an external contract before updating its internal state, allowing the external contract to call back and potentially drain funds.

**Example Pattern:**

```solidity
function withdraw() public {
    uint amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0; // State updated AFTER external call
}
```

**Mitigation:**

- Use Checks-Effects-Interactions pattern
- Update state before external calls
- Use reentrancy guards (OpenZeppelin's ReentrancyGuard)

## SWC-136: Unchecked Return Values

**Description:** Failure to check return values of external calls can lead to silent failures and unexpected behavior.

**Mitigation:**

- Always check return values
- Use `require()` statements for critical operations
- Consider using `transfer()` for ETH transfers (limited gas)

## SWC-101: Integer Overflow and Underflow

**Description:** Arithmetic operations that exceed type limits can wrap around, causing unexpected behavior.

**Mitigation:**

- Use Solidity 0.8.0+ for automatic overflow/underflow protection
- Use SafeMath library for older versions
- Validate input ranges

## SWC-132: Access Control Issues

**Description:** Functions lacking proper access control can be called by unauthorized users.

**Mitigation:**

- Implement role-based access control
- Use modifiers for permission checks
- Follow principle of least privilege

## Best Practices

1. **Checks-Effects-Interactions Pattern**

   - Checks: Validate conditions
   - Effects: Update state
   - Interactions: Call external contracts

2. **Gas Optimization**

   - Minimize storage operations
   - Use events for data that doesn't need on-chain storage
   - Pack struct variables efficiently

3. **Documentation**

   - Use NatSpec comments (@notice, @dev, @param, @return)
   - Document security assumptions
   - Explain complex logic

4. **Testing**
   - Comprehensive unit tests
   - Integration tests
   - Fuzzing and property-based testing
   - Security audits
