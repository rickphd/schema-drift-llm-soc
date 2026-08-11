from __future__ import annotations

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from src.blue.blue_agent_graph import log, retrieve_memory


class MemoryDisabledTests(unittest.TestCase):
    def test_retrieve_memory_does_not_open_faiss(self) -> None:
        state = {
            "memory_enabled": False,
            "detection_event": {
                "timestamp": "2026-01-01T00:00:00Z",
                "event_type": "authentication",
                "host": "host-a",
                "user": "service-account",
                "src_ip": "192.0.2.10",
                "action": "login",
                "outcome": "success",
                "severity": "medium",
                "tags": ["service_account"],
            },
            "asset_context": {"criticality": "medium"},
        }

        with patch(
            "src.blue.blue_agent_graph.get_memory",
            side_effect=AssertionError("FAISS must remain unopened"),
        ):
            result = retrieve_memory(state)

        self.assertEqual(result["memory_hits"], [])
        self.assertTrue(result["case_text"])
        self.assertTrue(result["pattern_text"])

    def test_log_does_not_learn_when_memory_is_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            decisions_path = os.path.join(tmp_dir, "decisions.jsonl")
            state = {
                "episode_id": 1,
                "run_id": "memory_disabled_test",
                "decisions_path": decisions_path,
                "memory_enabled": False,
                "memory_dir": os.path.join(tmp_dir, "memory"),
                "case_text": "recurrent benign case",
                "proposed_decision": "no_block",
                "final_decision": "no_block",
                "decision_reason": "test",
                "memory_hits": [],
                "timing": {},
            }

            with patch(
                "src.blue.blue_agent_graph.get_memory",
                side_effect=AssertionError("FAISS must remain unopened"),
            ):
                log(state)

            with open(decisions_path, "r", encoding="utf-8") as handle:
                record = json.loads(handle.readline())
            self.assertFalse(record["evidence"]["memory_enabled"])
            self.assertFalse(os.path.exists(state["memory_dir"]))


if __name__ == "__main__":
    unittest.main()
