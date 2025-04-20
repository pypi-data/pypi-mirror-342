# Chain Index

Chain Index is a Python package that provides easy access to information about various blockchain networks. It allows developers to retrieve details such as native currencies, RPC URLs, common tokens, and more for different chains.

## Features

- Retrieve chain information by chain ID or name
- Access details like native currency, RPC URLs, and block explorers
- Get token information including contract addresses and decimals
- Access commonly used blockchain constants (event topics, function signatures)
- Handle multiple chain identifiers (ID, name, alias)
- Robust error handling for non-existent chains

## Installation

You can install Chain Index using pip:

```bash
pip install chain-index
```

## Usage

### Chain Information

```python
from chain_index import get_chain_info, ChainNotFoundError

try:
    # Get chain info by ID
    ethereum = get_chain_info(1)
    print(f"Ethereum native currency: {ethereum.nativeCurrency.symbol}")

    # Get chain info by name
    polygon = get_chain_info("Polygon Mainnet")
    print(f"Polygon chain ID: {polygon.chainId}")

    # Error handling
    non_existent = get_chain_info(999999)
except ChainNotFoundError as e:
    print(f"Error: {e}")
```

### Token Information

```python
from chain_index import get_token_info, get_chain_tokens, get_all_chain_tokens, TokenNotFoundError

# Get specific token information
usdt = get_token_info(1, "USDT")
print(f"USDT contract on Ethereum: {usdt.contract}")
print(f"USDT decimals: {usdt.decimals}")

# Get all common tokens on a chain
ethereum_tokens = get_chain_tokens(1)
for symbol, token in ethereum_tokens.items():
    print(f"{symbol}: {token.contract}")

# Get all tokens including native and wrapped tokens
all_tokens = get_all_chain_tokens(1)
print(f"Native token: {all_tokens.native_token.symbol}")
print(f"Wrapped native token: {all_tokens.wrapped_native.symbol}")
```

### Blockchain Constants

The package provides organized blockchain constants in two formats:

#### Method 1: Direct access

```python
from chain_index import constants

# Direct access to constants
print(f"Transfer Topic: {constants.TRANSFER_EVENT_TOPIC}")
print(f"Null Address: {constants.ETH_NULL_ADDRESS}")
print(f"ETH Block Time: {constants.ETHEREUM_AVERAGE_BLOCK_TIME}")

# Use in web3.py
logs = web3.eth.get_logs({
    'fromBlock': 'latest',
    'toBlock': 'latest',
    'topics': [constants.TRANSFER_EVENT_TOPIC]
})
```

#### Method 2: Categorized access (recommended)

```python
from chain_index import constants

# Access via categories (more organized)
print(f"Transfer Topic: {constants.EventTopics.TRANSFER}")
print(f"Approval Topic: {constants.EventTopics.APPROVAL}")

# Nested categories for better organization
print(f"ERC20 Transfer: {constants.EventTopics.ERC20.TRANSFER}")
print(f"Uniswap V2 Swap: {constants.EventTopics.Uniswap.V2_SWAP}")

# Function signatures
print(f"Transfer: {constants.FunctionSignatures.TRANSFER}")

# Addresses
print(f"Null Address: {constants.Addresses.NULL_ADDRESS}")
print(f"Uniswap V2 Factory: {constants.Addresses.Uniswap.V2_FACTORY}")

# Wrapped tokens across different chains
print(f"WETH on Ethereum: {constants.WrappedToken.ETHEREUM}")
print(f"WMATIC on Polygon: {constants.WrappedToken.POLYGON}")
print(f"WBNB on BSC: {constants.WrappedToken.BSC}")

# Gas limits
print(f"ERC20 Transfer Gas: {constants.GasLimits.ERC20_TRANSFER}")

# Block times
print(f"ETH Block Time: {constants.BlockTime.ETHEREUM}")
print(f"Polygon Block Time: {constants.BlockTime.POLYGON}")
```

## API Reference

### Chain Information

- `get_chain_info(chain_identifier: Union[int, str]) -> ChainInfo`
  - Retrieves chain information based on the provided identifier
  - `chain_identifier`: Can be an integer (chain ID) or a string (chain name or alias)
  - Returns a `ChainInfo` object containing chain details
  - Raises `ChainNotFoundError` if the chain is not found

### Token Information

- `get_token_info(chain_id: int, symbol: str) -> TokenInfo`
  - Retrieves token information for a specific chain and symbol
  - Returns a `TokenInfo` object containing token details
  - Raises `TokenNotFoundError` if the token is not found

- `get_chain_tokens(chain_id: int) -> dict[str, TokenInfo]`
  - Retrieves all common tokens for a specific chain
  - Returns a dictionary mapping token symbols to `TokenInfo` objects

- `get_all_chain_tokens(chain_id: int) -> ChainTokens`
  - Retrieves all tokens for a chain including native, wrapped native, and common tokens
  - Returns a `ChainTokens` object with properties:
    - `native_token`: The chain's native token (e.g., ETH on Ethereum)
    - `wrapped_native`: The chain's wrapped native token (e.g., WETH on Ethereum)
    - `common_tokens`: Dictionary of common tokens on the chain

### Constants Module

The package provides a `constants` module with various blockchain-related constants, organized into categories:

- `EventTopics`: Event signature topics (keccak hash of event signatures)
  - `TRANSFER`, `APPROVAL`, `UNISWAP_V2_SWAP`, etc.
  - Nested categories: `ERC20`, `ERC721`, `Uniswap`

- `FunctionSignatures`: Function signature selectors (first 4 bytes of keccak hash)
  - `TRANSFER`, `APPROVE`, `BALANCE_OF`, etc.
  - Nested categories: `ERC20`

- `Addresses`: Common contract addresses
  - `NULL_ADDRESS`
  - Nested categories: `Uniswap`, `Sushiswap`

- `GasLimits`: Standard gas limits for operations
  - `ERC20_TRANSFER`, `ERC20_APPROVE`, `SWAP`

- `BlockTime`: Average block times in seconds
  - `ETHEREUM`, `BSC`, `POLYGON`, `ARBITRUM`, etc.

- `WrappedToken`: Wrapped token information
  - `ETHEREUM`, `POLYGON`, `BSC`, etc.

Direct access to all constants is also available at the module level for convenience.

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project uses data from the [chainid.network](https://chainid.network/) project, which provides a comprehensive list of EVM-compatible chains.

## Disclaimer

This package is provided as-is, and while we strive for accuracy, we cannot guarantee the correctness of all chain information. Users should verify critical information independently.