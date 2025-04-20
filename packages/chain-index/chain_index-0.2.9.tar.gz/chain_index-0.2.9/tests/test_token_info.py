import pytest
import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from chain_index import get_token_info, get_chain_tokens, TokenNotFoundError, ChainNotFoundError, get_all_chain_tokens

def test_get_token_info():
    # Test getting USDT on Ethereum
    usdt = get_token_info(1, "USDT")
    assert usdt.symbol == "USDT"
    assert usdt.decimals == 6
    assert usdt.contract.startswith("0x")

def test_get_chain_tokens():
    # Test getting all tokens on Ethereum
    eth_tokens = get_chain_tokens(1)
    assert len(eth_tokens) > 0
    assert "USDT" in eth_tokens
    assert "USDC" in eth_tokens

def test_token_not_found():
    with pytest.raises(TokenNotFoundError):
        get_token_info(1, "NONEXISTENT")

def test_chain_not_found():
    with pytest.raises(ChainNotFoundError):
        get_token_info(999999, "USDT")

def test_get_all_chain_tokens():
    chain_tokens = get_all_chain_tokens(1)  # Ethereum
    
    # Test native token
    assert chain_tokens.native_token.symbol == "ETH"
    assert chain_tokens.native_token.contract == "0x0000000000000000000000000000000000000000"
    
    # Test wrapped native token
    assert chain_tokens.wrapped_native.symbol == "WETH"
    assert chain_tokens.wrapped_native.contract.startswith("0x")
    
    # Test getting all tokens
    all_tokens = chain_tokens.get_all_tokens()
    assert "ETH" in all_tokens
    assert "WETH" in all_tokens
    assert "USDT" in all_tokens
    
    # Test getting specific token
    usdt = chain_tokens.get_token("USDT")
    assert usdt.symbol == "USDT"
    assert usdt.decimals == 6

def test_get_token_not_found():
    chain_tokens = get_all_chain_tokens(1)
    with pytest.raises(TokenNotFoundError):
        chain_tokens.get_token("NONEXISTENT") 