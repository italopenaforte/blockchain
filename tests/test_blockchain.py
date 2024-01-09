import logging
from unittest.mock import Mock

import pytest

from src.blockchain import Blockchain


def test_blockchain_instantiation():
    sut = Blockchain()
    chain = sut.chain[0]

    assert len(sut.chain) == 1
    assert chain.get("proof") == 100
    assert chain.get("previous_hash") == 1
    assert len(sut.current_transactions) == 0


def test_new_transaction():
    sut = Blockchain()

    new_transaction = {
        "sender": "my address",
        "recipient": "someone else's address",
        "amount": 5,
    }

    response = sut.new_transction(**new_transaction)

    assert response == 2
    assert len(sut.current_transactions) == 1
