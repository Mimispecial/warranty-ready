from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "warranty_ready.py"
SDK = "v0.2.16"
PROMPT = "Screen two declared warranty document lanes"
POLICY = "This intake records document readiness for a manual warranty desk. It does not determine coverage, legal rights, product fault, payment, repair, replacement, or eligibility, and records are not externally authenticated."


def address(account):
    return "0x" + account.hex()


def package(vm, direct_deploy, issuer, claimant):
    vm.sender = issuer
    contract = direct_deploy(
        str(CONTRACT), address(claimant), "Home desk lamps", POLICY,
        "The purchase record must name the product model, serial reference, and purchase date.",
        "The condition record must index claimant-declared images of the product label and reported condition.", sdk_version=SDK,
    )
    vm.sender = claimant
    contract.submit_intake_package(
        "Lamp model DL-4, serial L40071",
        "The claimant reports that the lamp stopped switching on after ordinary desk use and records no visible cable damage.",
        "Receipt R-881 lists model DL-4, serial L40071, and purchase date 2026-05-14.",
        "Files label.jpg and condition.jpg are indexed to the declared serial L40071 and reported lamp condition.",
    )
    return contract


def test_present_lanes_derive_ready_and_human_routing(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = package(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.mock_llm(PROMPT, json.dumps({"lane_code": "PP"}))
    contract.screen_document_lanes()
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True
    assert contract.get_state()["readiness"] == "READY"
    direct_vm.sender = direct_alice
    contract.route_to_desk("MANUAL_REVIEW", "The two document lanes are ready for a human warranty-desk review; no coverage outcome is recorded.")
    assert contract.get_state()["routing"] == "MANUAL_REVIEW"


def test_missing_lane_allows_one_claimant_supplement(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = package(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.mock_llm(PROMPT, json.dumps({"lane_code": "PM"}))
    contract.screen_document_lanes()
    direct_vm.sender = direct_bob
    contract.supplement_records("The supplement identifies label.jpg and condition.jpg, ties both to serial L40071, and states which image records the reported condition.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"lane_code": "PP"}))
    contract.screen_document_lanes()
    assert contract.get_state()["screening_round"] == 2
    assert contract.get_state()["supplement_used"] is True


def test_claimant_role_and_bad_lane_code_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    direct_vm.sender = direct_alice
    contract = direct_deploy(str(CONTRACT), address(direct_bob), "Home desk lamps", POLICY, "Purchase record names model, serial, and date.", "Condition record indexes product label and condition images.", sdk_version=SDK)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_claimant"):
        contract.submit_intake_package("Lamp DL-4 L40071", "An unauthorized incident summary must not enter this designated package.", "Unauthorized receipt record with model and date.", "Unauthorized condition image index with serial data.")
    direct_vm.sender = direct_bob
    contract.submit_intake_package("Lamp DL-4 L40071", "The claimant reports the lamp stopped switching on during ordinary use without visible cable damage.", "Receipt R-881 lists DL-4, L40071, and purchase date.", "label.jpg and condition.jpg are indexed to L40071.")
    direct_vm.mock_llm(PROMPT, json.dumps({"lane_code": "PPP"}))
    with direct_vm.expect_revert("invalid_lane_code"):
        contract.screen_document_lanes()
    assert contract.get_state()["status"] == "READY_FOR_SCREENING"
