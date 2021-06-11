from app.adapters import Explorer

address = '1HiE8iHHRJyMooJLxue76pjsj8rmxKXe95'

'https://sochain.com/api/v2/get_address_balance/BTC/1HiE8iHHRJyMooJLxue76pjsj8rmxKXe95'


# def test_balanance():
#     resp = sochain.get_confirmed_sat_balance(address=address)

#     assert 1 == 1


# def test_get_tx_inputs():
#     resp = sochain.get_tx_inputs(address=address)
#     assert 1 == 1


def test_address_resource():
    explorer = Explorer(address=address)
    resp = explorer.tx_inputs
