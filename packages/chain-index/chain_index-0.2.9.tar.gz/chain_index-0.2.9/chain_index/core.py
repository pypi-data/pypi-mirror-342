import json
from pathlib import Path
import logging
from typing import Union, Optional
from pydantic import BaseModel, Field
from .exceptions import ChainNotFoundError, TokenNotFoundError
import numpy as np

logging.basicConfig(level=logging.DEBUG)  # Change to DEBUG level
logger = logging.getLogger(__name__)

class NativeCurrency(BaseModel):
    name: str
    symbol: str
    decimals: int

class WrapperNativeCurrency(BaseModel):
    name: str
    symbol: str
    decimals: int
    contract: str

class Explorer(BaseModel):
    name: str
    url: str
    standard: Optional[str] = None

class TokenInfo(BaseModel):
    name: str
    symbol: str
    decimals: int
    contract: str
    chain_id: int
    price_usd: Optional[float] = None

class ChainInfo(BaseModel):
    name: str
    chain: Optional[str] = None
    chainId: int
    networkId: Optional[int] = None
    rpc: list[str] = []
    faucets: list[str] = []
    nativeCurrency: NativeCurrency
    wrapperNativeCurrency: Optional[WrapperNativeCurrency] = None
    infoURL: Optional[str] = None
    shortName: str
    icon: Optional[str] = None
    explorers: Optional[list[Explorer]] = None
    ens: Optional[dict] = None
    slip44: Optional[int] = None
    common_tokens: Optional[dict[str, TokenInfo]] = None

class ChainTokens:
    """Container class for all tokens on a chain"""
    def __init__(self, chain_id: int):
        self.chain_id = chain_id
        self.chain = get_chain_info(chain_id)
        
        # Native token
        self.native_token = TokenInfo(
            name=self.chain.nativeCurrency.name,
            symbol=self.chain.nativeCurrency.symbol,
            decimals=self.chain.nativeCurrency.decimals,
            contract="0x0000000000000000000000000000000000000000",  # Native token uses zero address
            chain_id=chain_id,
            price_usd=0
        )
        
        # Wrapped native token if exists
        self.wrapped_native = None
        if self.chain.wrapperNativeCurrency:
            self.wrapped_native = TokenInfo(
                name=self.chain.wrapperNativeCurrency.name,
                symbol=self.chain.wrapperNativeCurrency.symbol,
                decimals=self.chain.wrapperNativeCurrency.decimals,
                contract=self.chain.wrapperNativeCurrency.contract,
                chain_id=chain_id,
                price_usd=0
            )
        
        # Common tokens
        self.common_tokens = get_chain_tokens(chain_id) if str(chain_id) in TOKENS else {}

    def get_all_tokens(self) -> dict[str, TokenInfo]:
        """Get all tokens including native, wrapped native, and common tokens"""
        all_tokens = {}
        if self.wrapped_native:
            all_tokens[self.wrapped_native.symbol] = self.wrapped_native
        all_tokens.update(self.common_tokens)
        return all_tokens

    def get_token(self, symbol: str) -> TokenInfo:
        """Get a specific token by symbol"""
        symbol = symbol.upper()
        all_tokens = self.get_all_tokens()
        if symbol not in all_tokens:
            raise TokenNotFoundError(f"Token {symbol} not found on chain {self.chain_id}")
        return all_tokens[symbol]

def load_chains():
    json_path = Path(__file__).parent / 'data' / 'chains.json'
    with open(json_path, 'r') as f:
        return json.load(f)

CHAINS = load_chains()

def load_tokens():
    json_path = Path(__file__).parent / 'data' / 'common_tokens.json'
    with open(json_path, 'r') as f:
        return json.load(f)

TOKENS = load_tokens()

def get_chain_info(chain_identifier: Union[int, str]) -> ChainInfo:
    # logger.debug(f"Searching for chain: {chain_identifier}")
    for chain in CHAINS:
        if isinstance(chain_identifier, (int, np.integer)):
            if chain_identifier == chain['chainId']:
                # logger.debug(f"Found chain by ID: {chain_identifier}")
                return ChainInfo(**chain)
        elif isinstance(chain_identifier, str):
            if (chain_identifier.lower() == chain['name'].lower() or
                chain_identifier.lower() in [alias.lower() for alias in chain.get('alias', [])] or
                chain_identifier.lower() == chain.get('shortName', '').lower()):
                # logger.debug(f"Found chain by name or alias: {chain_identifier}")
                return ChainInfo(**chain)
            try:
                # Handle both decimal and hexadecimal string representations
                chain_id = int(chain_identifier, 16 if chain_identifier.lower().startswith('0x') else 10)
                if chain_id == chain['chainId']:
                    # logger.debug(f"Found chain by ID (string): {chain_identifier}")
                    return ChainInfo(**chain)
            except ValueError:
                pass
    # logger.debug(f"Chain not found: {chain_identifier}")
    raise ChainNotFoundError(f"Chain not found: {chain_identifier}")

def get_token_info(chain_id: int, symbol: str) -> TokenInfo:
    """Get token information for a specific chain and symbol.
    
    Args:
        chain_id: The chain ID to look up
        symbol: The token symbol (e.g., 'USDT', 'USDC')
    
    Returns:
        TokenInfo object containing token details
    
    Raises:
        ChainNotFoundError: If the chain_id is not found
        TokenNotFoundError: If the token symbol is not found on the chain
    """
    chain_tokens = TOKENS.get(str(chain_id))
    if not chain_tokens:
        raise ChainNotFoundError(f"Chain ID {chain_id} not found in token database")
    
    token = chain_tokens.get(symbol.upper())
    if not token:
        raise TokenNotFoundError(f"Token {symbol} not found on chain {chain_id}")
    
    return TokenInfo(**token, chain_id=chain_id)

def get_chain_tokens(chain_id: int) -> dict[str, TokenInfo]:
    """Get all common tokens for a specific chain.
    
    Args:
        chain_id: The chain ID to look up
    
    Returns:
        Dictionary of token symbols to TokenInfo objects
    
    Raises:
        ChainNotFoundError: If the chain_id is not found
    """
    chain_tokens = TOKENS.get(str(chain_id))
    if not chain_tokens:
        raise ChainNotFoundError(f"Chain ID {chain_id} not found in token database")
    
    return {
        symbol: TokenInfo(**token_data, chain_id=chain_id)
        for symbol, token_data in chain_tokens.items()
    }

def get_all_chain_tokens(chain_id: int) -> ChainTokens:
    """Get all tokens for a chain including native, wrapped native and common tokens.
    
    Args:
        chain_id: The chain ID to look up
    
    Returns:
        ChainTokens object containing all token information
    
    Raises:
        ChainNotFoundError: If the chain_id is not found
    """
    return ChainTokens(chain_id)
