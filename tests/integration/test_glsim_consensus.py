from pathlib import Path
import json

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Screen two declared warranty document lanes"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"lane_code": "PP"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_document_lane_readiness():
    issuer_account, claimant_account = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "warranty_ready.py")
    deployed = factory.deploy_contract_tx(args=[claimant_account.address, "Home desk lamps", "This intake records document readiness for a manual desk and never determines coverage, rights, fault, payment, repair, replacement, or eligibility.", "The purchase record names product model, serial reference, and purchase date.", "The condition record indexes claimant-declared images of the product label and reported condition."], account=issuer_account, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    issuer = factory.build_contract(address, account=issuer_account)
    claimant = factory.build_contract(address, account=claimant_account)
    ok(claimant.submit_intake_package(args=["Lamp model DL-4, serial L40071", "The claimant reports the lamp stopped switching on after ordinary desk use and records no visible cable damage.", "Receipt R-881 lists model DL-4, serial L40071, and purchase date 2026-05-14.", "Files label.jpg and condition.jpg are indexed to serial L40071 and the reported condition."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(claimant.screen_document_lanes(args=[]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(issuer.route_to_desk(args=["MANUAL_REVIEW", "Both lanes are ready for human desk review; no coverage outcome is recorded."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert issuer.get_state(args=[]).call()["routing"] == "MANUAL_REVIEW"
