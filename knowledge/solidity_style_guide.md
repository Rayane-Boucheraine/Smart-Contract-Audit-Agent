# Solidity Style Guide and Best Practices

## Naming Conventions

- **Contracts**: CapWords (PascalCase) - `MyContract`
- **Functions**: mixedCase (camelCase) - `myFunction`
- **Variables**: mixedCase - `myVariable`
- **Constants**: UPPER_CASE_WITH_UNDERSCORES - `MAX_SUPPLY`
- **Events**: CapWords - `Transfer`
- **Modifiers**: mixedCase - `onlyOwner`

## Code Layout

### Import Statements

```solidity
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./MyOtherContract.sol";
```

### Contract Layout Order

1. Type declarations
2. State variables
3. Events
4. Modifiers
5. Functions

### Function Order

1. constructor
2. receive/fallback
3. external functions
4. public functions
5. internal functions
6. private functions

## Gas Optimization Tips

1. **Pack Structs**: Order variables by size to minimize storage slots
2. **Use Events**: For data that doesn't need on-chain access
3. **Batch Operations**: Combine multiple operations when possible
4. **Avoid Loops**: Especially with unbounded arrays
5. **Use `immutable` and `constant`**: For values that don't change

## Documentation Standards

### NatSpec Comments

```solidity
/// @title A title for the contract
/// @notice Explain to an end user what this does
/// @dev Explain to a developer any extra details
contract MyContract {
    /// @notice Deposit ETH into the contract
    /// @dev Updates the balance mapping
    /// @param amount The amount to deposit
    /// @return success Whether the deposit was successful
    function deposit(uint256 amount) external returns (bool success) {
        // Implementation
    }
}
```

## Security Patterns

### Checks-Effects-Interactions

```solidity
function withdraw(uint256 amount) external {
    // Checks
    require(balances[msg.sender] >= amount, "Insufficient balance");

    // Effects
    balances[msg.sender] -= amount;

    // Interactions
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

### Pull Over Push Pattern

```solidity
// Instead of pushing payments, let users pull them
mapping(address => uint256) public pendingWithdrawals;

function withdraw() external {
    uint256 amount = pendingWithdrawals[msg.sender];
    pendingWithdrawals[msg.sender] = 0;
    payable(msg.sender).transfer(amount);
}
```
