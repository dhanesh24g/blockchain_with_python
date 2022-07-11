from scripts.deploy import deploy_fund_me
from scripts.supporting_script import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 1

    # Test FUND function
    txn1 = fund_me.fund({"from": account, "value": entrance_fee})
    txn1.wait(1)
    assert fund_me.addressToAmountMapping(account.address) == entrance_fee

    # Test WITHDRAW function
    txn2 = fund_me.withdraw({"from": account})
    txn2.wait(1)
    assert fund_me.addressToAmountMapping(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only available for local testing !")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # With exception handling
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
