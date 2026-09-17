"""Offline top-context regressions; recording fakes only, no live main or SDK."""
import unittest
from unittest.mock import patch

import test_inspect_resolve as base


CHAIN = (
    ("resolve", "project_manager", "GetProjectManager"),
    ("manager", "project", "GetCurrentProject"),
    ("project", "timeline", "GetCurrentTimeline"),
    ("timeline", "item", "GetCurrentVideoItem"),
)


class TopContextTests(unittest.TestCase):
    def capture_answer(self, owner, getter, answer):
        case = base.SnapshotContractTests()
        case.setUp()
        getattr(case, owner).answers[getter] = answer
        with patch.object(base.helper, "main", side_effect=AssertionError("Live main forbidden")):
            result = case.capture()
        return case, result

    def assert_child_reason(self, data, stage, reason):
        group = data["color_group"]
        self.assertEqual(group["status"], "unknown")
        self.assertEqual(group["reason"], reason)
        for key in ("pre_clip_node_graph", "post_clip_node_graph"):
            self.assertEqual(group[key]["status"], "unknown")
            self.assertEqual(group[key]["reason"], reason)
            self.assertIsNone(group[key]["nodes"])
        if stage == "item":
            self.assertEqual(data["timeline_node_graph"]["status"], "ok")
            self.assertEqual(data["timeline_node_graph"]["nodes"][0]["lut_filename"], "timeline.cube")
            self.assertEqual(data["timeline_name"], "Current timeline")
        else:
            self.assertEqual(data["timeline_node_graph"]["status"], "unknown")
            self.assertEqual(data["timeline_node_graph"]["reason"], reason)
            self.assertIsNone(data["timeline_node_graph"]["nodes"])
        self.assertEqual(data["clip_node_graphs"], [])

    def test_exception_at_every_stage_is_unknown_with_getter_reason(self):
        for owner, stage, getter in CHAIN:
            with self.subTest(stage=stage):
                case, data = self.capture_answer(owner, getter, base.Failure())
                reason = f"{stage}.{getter}:getter_failed"
                self.assertEqual(data["status"], "unknown")
                self.assertEqual(data["reason"], reason)
                self.assert_child_reason(data, stage, reason)
                self.assertEqual(case.rec.forbidden, [])

    def test_missing_method_at_every_stage_is_unknown_with_getter_reason(self):
        for owner, stage, getter in CHAIN:
            with self.subTest(stage=stage):
                _, data = self.capture_answer(owner, getter, base.MISSING)
                reason = f"{stage}.{getter}:method_unavailable"
                self.assertEqual(data["status"], "unknown")
                self.assertEqual(data["reason"], reason)
                self.assert_child_reason(data, stage, reason)

    def test_successful_absent_manager_is_unknown_not_no_project(self):
        case, data = self.capture_answer("resolve", "GetProjectManager", None)
        self.assertEqual(data["status"], "unknown")
        self.assertEqual(data["reason"], "project_manager_not_returned")
        self.assert_child_reason(data, "project_manager", "project_manager_not_returned")
        self.assertFalse(any(label == "manager" for label, _, _ in case.rec.calls))

    def test_successful_absent_project_timeline_item_keeps_no_current(self):
        for owner, stage, getter in CHAIN[1:]:
            with self.subTest(stage=stage):
                _, data = self.capture_answer(owner, getter, None)
                status = "no_current_video_item" if stage == "item" else f"no_current_{stage}"
                self.assertEqual(data["status"], status)
                self.assertEqual(data["reason"], status)
                self.assert_child_reason(data, stage, status)

    def test_successful_chain_retains_prior_context_and_null_reason(self):
        case = base.SnapshotContractTests()
        case.setUp()
        data = case.capture()
        self.assertEqual(data["status"], "ok")
        self.assertIsNone(data["reason"])
        self.assertEqual(data["project_name"], "Current project")
        self.assertEqual(data["current_clip_name"], "test.mxf")
        self.assertEqual(data["timeline_node_graph"]["status"], "ok")
        self.assertEqual(data["color_group"]["status"], "ok")
        case.assert_clip_layers_preserved(data)

    def test_invalid_scalar_or_container_context_remains_unknown(self):
        for owner, stage, getter in CHAIN:
            for answer in (False, 0, "", [], {}):
                with self.subTest(stage=stage, answer=repr(answer)):
                    _, data = self.capture_answer(owner, getter, answer)
                    reason = f"{stage}.{getter}:invalid_context_returned"
                    self.assertEqual(data["status"], "unknown")
                    self.assertEqual(data["reason"], reason)
                    self.assert_child_reason(data, stage, reason)


if __name__ == "__main__":
    unittest.main(verbosity=2)
