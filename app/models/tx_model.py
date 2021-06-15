import uuid


class Tx:

    def __init__(self, id, unsigned_tx, signed_tx):
        self.id = id
        self.unsigned_tx = unsigned_tx
        self.signed_tx = signed_tx

    @classmethod
    def create(cls, unsigned_tx, signed_tx):
        return cls(
            id=_get_tx_id(),
            unsigned_tx=unsigned_tx,
            signed_tx=signed_tx
        )


def _get_tx_id():
    return f'tx-{str(uuid.uuid4())[-12:]}'
