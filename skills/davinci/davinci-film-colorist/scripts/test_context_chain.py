"""Independent upper-context regressions using recording getter-only stubs."""

import builtins
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


def import_helper():
    original_import = builtins.__import__

    def guarded(name, *args, **kwargs):
        if name.split(".", 1)[0] in {"DaVinciResolveScript", "DaVinciResolve", "fusionscript"}:
            raise AssertionError("Vendor import forbidden")
        return original_import(name, *args, **kwargs)

    spec = importlib.util.spec_from_file_location(
        "_offline_context_helper", Path(__file__).with_name("inspect_resolve.py"))
    module = importlib.util.module_from_spec(spec)
    with patch("builtins.__import__", guarded):
        spec.loader.exec_module(module)
    return module


helper = import_helper()
MISSING = object()
FAILED = object()
GETTERS = {"GetCurrentPage", "GetProjectManager", "GetCurrentProject", "GetCurrentTimeline",
           "GetCurrentVideoItem", "GetName", "GetSetting", "GetMediaPoolItem", "GetCurrentVersion",
           "GetVersionNameList", "GetNodeGraph", "GetColorGroup", "GetCurrentTimecode",
           "GetNumNodes", "GetLUT", "GetToolsInNode"}


class Stub:
    def __init__(self, label, calls, forbidden, **answers):
        self.label, self.calls, self.forbidden, self.answers = label, calls, forbidden, answers

    def __getattr__(self, method):
        if method not in GETTERS:
            self.forbidden.append((self.label, method))
            raise AttributeError("Unexpected/mutating API access")
        answer = self.answers.get(method, MISSING)
        if answer is MISSING:
            self.calls.append((self.label, method, "missing"))
            raise AttributeError(method)

        def invoke(*args):
            self.calls.append((self.label, method, args))
            if answer is FAILED:
                raise RuntimeError("mocked getter failure")
            return answer(*args) if callable(answer) else answer

        return invoke


def context():
    calls, forbidden = [], []
    def stub(label, **answers):
        return Stub(label, calls, forbidden, **answers)
    graph = stub("graph", GetNumNodes=0)
    item = stub("item", GetName="test.mxf", GetMediaPoolItem=None,
                GetCurrentVersion={"versionName": "Original", "versionType": 0},
                GetVersionNameList=["Original"], GetNodeGraph=lambda *args: graph,
                GetColorGroup=None)
    timeline = stub("timeline", GetName="Current timeline", GetCurrentVideoItem=item,
                    GetSetting=lambda key: None, GetCurrentTimecode="00:00:01:00",
                    GetNodeGraph=graph)
    project = stub("project", GetName="Current project", GetCurrentTimeline=timeline,
                   GetSetting=lambda key: "1" if key == "nodeStackLayers" else None)
    manager = stub("manager", GetCurrentProject=project)
    resolve = stub("resolve", GetCurrentPage="color", GetProjectManager=manager)
    return {"resolve": resolve, "manager": manager, "project": project,
            "timeline": timeline, "item": item, "calls": calls, "forbidden": forbidden}


class ContextChainTests(unittest.TestCase):
    def capture(self, chain):
        with patch.object(helper, "load_resolve_module", side_effect=AssertionError("Live forbidden")):
            report = helper.snapshot(chain["resolve"])
        self.assertEqual(chain["forbidden"], [])
        self.assertEqual(chain["calls"][0], ("resolve", "GetCurrentPage", ()))
        return report

    def assert_failed_getter(self, owner, method, unavailable_owners):
        reasons = []
        stage = {"resolve": "project_manager", "manager": "project",
                 "project": "timeline", "timeline": "item"}[owner]
        for failure in (MISSING, FAILED):
            with self.subTest(owner=owner, failure="missing" if failure is MISSING else "raise"):
                chain = context()
                chain[owner].answers[method] = failure
                report = self.capture(chain)
                self.assertEqual(report["status"], "unknown")
                cause = "method_unavailable" if failure is MISSING else "getter_failed"
                self.assertEqual(report["reason"], f"{stage}.{method}:{cause}")
                reasons.append(report["reason"])
                for downstream in unavailable_owners:
                    self.assertFalse(any(label == downstream for label, _, _ in chain["calls"]))
                self.assertEqual(report["color_group"]["status"], "unknown")
                self.assertEqual(report["color_group"]["reason"], report["reason"])
                for key in ("pre_clip_node_graph", "post_clip_node_graph"):
                    self.assertEqual(report["color_group"][key]["status"], "unknown")
                    self.assertEqual(report["color_group"][key]["reason"], report["reason"])
                if owner == "timeline":
                    self.assertEqual(report["timeline_node_graph"]["status"], "ok")
                    self.assertEqual(report["timeline_node_graph"]["node_count"], 0)
                else:
                    self.assertEqual(report["timeline_node_graph"]["status"], "unknown")
                    self.assertEqual(report["timeline_node_graph"]["reason"], report["reason"])
        # The machine-readable reason must retain unavailable vs failed cause.
        self.assertNotEqual(reasons[0], reasons[1])

    def test_missing_or_failed_manager_getter_is_unknown(self):
        self.assert_failed_getter("resolve", "GetProjectManager", ("manager", "project", "timeline", "item"))

    def test_missing_or_failed_project_getter_is_unknown(self):
        self.assert_failed_getter("manager", "GetCurrentProject", ("project", "timeline", "item"))

    def test_missing_or_failed_timeline_getter_is_unknown(self):
        self.assert_failed_getter("project", "GetCurrentTimeline", ("timeline", "item"))

    def test_missing_or_failed_item_getter_preserves_available_timeline_graph(self):
        self.assert_failed_getter("timeline", "GetCurrentVideoItem", ("item",))

    def test_successful_none_manager_remains_unknown(self):
        chain = context()
        chain["resolve"].answers["GetProjectManager"] = None
        report = self.capture(chain)
        self.assertEqual(report["status"], "unknown")
        self.assertEqual(report["reason"], "project_manager_not_returned")
        self.assertFalse(any(label == "manager" for label, _, _ in chain["calls"]))

    def test_successful_none_project_is_known_absence(self):
        chain = context()
        chain["manager"].answers["GetCurrentProject"] = None
        report = self.capture(chain)
        self.assertEqual(report["status"], "no_current_project")
        self.assertFalse(any(label == "project" for label, _, _ in chain["calls"]))

    def test_successful_none_timeline_is_known_absence(self):
        chain = context()
        chain["project"].answers["GetCurrentTimeline"] = None
        report = self.capture(chain)
        self.assertEqual(report["status"], "no_current_timeline")
        self.assertFalse(any(label == "timeline" for label, _, _ in chain["calls"]))

    def test_successful_none_item_is_known_absence_and_timeline_survives(self):
        chain = context()
        chain["timeline"].answers["GetCurrentVideoItem"] = None
        report = self.capture(chain)
        self.assertEqual(report["status"], "no_current_video_item")
        self.assertEqual(report["timeline_node_graph"]["status"], "ok")
        self.assertFalse(any(label == "item" for label, _, _ in chain["calls"]))

    def test_healthy_context_still_reads_current_clip_and_timeline(self):
        report = self.capture(context())
        self.assertEqual(report["status"], "ok")
        self.assertIsNone(report["reason"])
        self.assertEqual(report["project_name"], "Current project")
        self.assertEqual(report["timeline_name"], "Current timeline")
        self.assertEqual(report["current_clip_name"], "test.mxf")
        self.assertEqual(report["clip_node_graphs"][0]["node_count"], 0)
        self.assertEqual(report["timeline_node_graph"]["node_count"], 0)
        self.assertEqual(report["color_group"]["status"], "not_applicable")


if __name__ == "__main__":
    unittest.main(verbosity=2)
