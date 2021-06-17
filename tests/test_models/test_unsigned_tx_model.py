from app.models.unsigned_tx_model import UnsignedTx
import tests.data as data


def test_messages(unsigned_tx_no_change):
    messages = unsigned_tx_no_change.messages

    assert messages == data.messages


def test_to_sign(unsigned_tx_no_change):
    to_sign = unsigned_tx_no_change.to_sign

    assert to_sign == data.to_sign


def test_version(unsigned_tx_no_change):
    version = unsigned_tx_no_change.version

    assert version == data.version


def test_tx_inputs(unsigned_tx_no_change):
    tx_inputs = unsigned_tx_no_change.tx_inputs

    assert tx_inputs == data.tx_inputs


def test_tx_in_count(unsigned_tx_no_change):
    tx_in_count = unsigned_tx_no_change.tx_in_count

    assert tx_in_count == data.tx_in_count


def test_placeholder(unsigned_tx_no_change):
    placeholder = unsigned_tx_no_change.placeholder

    assert placeholder == data.placeholder


def test_sequence(unsigned_tx_no_change):
    sequence = unsigned_tx_no_change.sequence

    assert sequence == data.sequence


def test_tx_out_count(unsigned_tx_no_change):
    tx_out_count = unsigned_tx_no_change.tx_out_count

    assert tx_out_count == data.tx_out_count


def test_lock_time(unsigned_tx_no_change):
    lock_time = unsigned_tx_no_change.lock_time

    assert lock_time == data.lock_time


def test_hash_code(unsigned_tx_no_change):
    hash_code = unsigned_tx_no_change.hash_code

    assert hash_code == data.hash_code
