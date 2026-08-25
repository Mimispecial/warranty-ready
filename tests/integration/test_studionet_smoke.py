import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


@pytest.mark.integration
def test_studionet_warranty_readiness(default_account, secondary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "warranty_ready.py")
    deployed = ok(factory.deploy_contract_tx(args=[secondary_account.address, "Home desk lamps", "This intake records document readiness for a manual desk and never determines coverage, rights, fault, payment, repair, replacement, or eligibility.", "The purchase record names product model, serial reference, and purchase date.", "The condition record indexes claimant-declared images of the product label and reported condition."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    issuer = factory.build_contract(address, account=default_account)
    claimant = factory.build_contract(address, account=secondary_account)
    ok(claimant.submit_intake_package(args=["Lamp model DL-4, serial L40071", "The claimant reports the lamp stopped switching on after ordinary desk use and records no visible cable damage.", "Receipt R-881 lists model DL-4, serial L40071, and purchase date 2026-05-14.", "Files label.jpg and condition.jpg are indexed to serial L40071 and the reported condition."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(claimant.screen_document_lanes(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = issuer.get_state(args=[]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["status"] == "ISSUER_ROUTING"
    assert state["purchase_state"] in ("PRESENT", "MISSING", "CONFLICT")
    assert state["condition_state"] in ("PRESENT", "MISSING", "CONFLICT")
    assert state["readiness"] in ("READY", "MISSING", "CONFLICT")
    observed = {"condition_state": state["condition_state"], "purchase_state": state["purchase_state"], "readiness": state["readiness"]}
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": observed}, sort_keys=True))
