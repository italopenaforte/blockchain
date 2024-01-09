import logging
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

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


def test_generate_hash_from_a_block():
    _hash = "4d967a30111bf29f0eba01c448b375c1629b2fed01cdfcc3aed91f1b57d5dd5e"
    sut = Blockchain()

    response = sut.hash("test")

    assert _hash == response


@pytest.mark.parametrize(
    "address, expected",
    [
        ("http://127.0.0.1:5000", "127.0.0.1:5000"),
        ("https://example.com", "example.com"),
        ("http://[::1]:5000", "[::1]:5000"),
    ],
)
def test_register_node_success(address, expected):
    sut = Blockchain()

    sut.register_node(address)

    for node in sut.nodes:
        assert node == expected


@pytest.mark.parametrize(
    "address, expected",
    [
        (
            "not-url",
            None,
        )
    ],
)
def test_register_node_fail(address, expected):
    sut = Blockchain()

    with pytest.raises(ValueError):
        sut.register_node(address)
        logging.debug(sut.nodes)


def test_proof_of_work():
    proof = 100
    sut = Blockchain()
    result = sut.proof_of_work(proof)
    assert result == 35293


def test_valid_proof_success():
    last_proof = 100
    proof = 35293

    sut = Blockchain()

    result = sut.valid_proof(last_proof, proof)

    assert result


def test_valid_proof_fail():
    last_proof = 100
    proof = 35292

    sut = Blockchain()

    result = sut.valid_proof(last_proof, proof)

    assert not result


def test_valid_one_chain():
    sut = Blockchain()
    result = sut.valid_chain(sut.chain)
    assert result


def test_valid_two_chain():
    def mine(sut):
        node_identifier = str(uuid4()).replace("-", "")
        last_block = sut.last_block
        last_proof = last_block["proof"]
        proof = sut.proof_of_work(last_proof)

        sut.new_transction(sender="0", recipient=node_identifier, amount=1)

        previous_hash = sut.hash(last_block)
        sut.new_block(proof, previous_hash)

    sut = Blockchain()
    mine(sut)
    result = sut.valid_chain(sut.chain)
    assert result
