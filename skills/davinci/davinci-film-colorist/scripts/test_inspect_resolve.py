"""Offline contract tests: standalone helper import, recording fake Resolve API only.

Run with a standard-library Python: python3 -B test_inspect_resolve.py
No vendor wrapper, application connection, rendering, or UI is used.
"""

import builtins
import importlib
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


VENDOR_MODULES = {"DaVinciResolveScript", "DaVinciResolve", "fusionscript"}


def load_helper():
    original_import = builtins.__import__
    original_import_module = importlib.import_module

    def guarded_import(name, *args, **kwargs):
        if name.split(".", 1)[0] in VENDOR_MODULES:
            raise AssertionError("Vendor module import forbidden in offline tests")
        return original_import(name, *args, **kwargs)

    def guarded_import_module(name, *args, **kwargs):
        if name.split(".", 1)[0] in VENDOR_MODULES:
            raise AssertionError("Vendor module import forbidden in offline tests")
        return original_import_module(name, *args, **kwargs)

    path = Path(__file__).with_name("inspect_resolve.py")
    spec = importlib.util.spec_from_file_location("_offline_color_helper", path)
    module = importlib.util.module_from_spec(spec)
    with patch("builtins.__import__", guarded_import), patch(
        "importlib.import_module", guarded_import_module
    ):
        spec.loader.exec_module(module)
    return module


helper = load_helper()
MISSING = object()


class Failure:
    """A documented getter exists, but calling it fails."""


class ByArgs:
    def __init__(self, answers, default=None):
        self.answers = answers
        self.default = default

    def lookup(self, args):
        return self.answers.get(args, self.default)


# Independent, role-specific allowlist from the SDK. Unexpected methods are
# recorded even if the helper swallows the exception raised by the fake.
READ_METHODS = {
    "resolve": {"GetCurrentPage", "GetProjectManager"},
    "manager": {"GetCurrentProject"},
    "project": {"GetName", "GetCurrentTimeline", "GetSetting"},
    "timeline": {"GetName", "GetCurrentVideoItem", "GetCurrentTimecode",
                 "GetSetting", "GetNodeGraph"},
    "item": {"GetName", "GetMediaPoolItem", "GetCurrentVersion",
             "GetVersionNameList", "GetNodeGraph", "GetColorGroup"},
    "media": {"GetClipProperty", "GetMetadata"},
    "group": {"GetName", "GetPreClipNodeGraph", "GetPostClipNodeGraph"},
    "graph": {"GetNumNodes", "GetLUT", "GetToolsInNode"},
}


def freeze(value):
    if isinstance(value, Fake):
        return ("fake", value.label)
    if isinstance(value, ByArgs):
        return ("by_args", freeze(value.answers), freeze(value.default))
    if isinstance(value, dict):
        return tuple((freeze(k), freeze(v)) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return tuple(freeze(v) for v in value)
    return value


class Recorder:
    def __init__(self):
        self.objects = []
        self.calls = []
        self.forbidden = []

    def state(self):
        return tuple((obj.label, freeze(obj.answers)) for obj in self.objects)


class Fake:
    def __init__(self, recorder, role, label, **answers):
        self.recorder, self.role, self.label = recorder, role, label
        self.answers = answers
        recorder.objects.append(self)

    def __getattr__(self, method):
        if method not in READ_METHODS[self.role]:
            self.recorder.forbidden.append((self.label, method))
            raise AttributeError("Unexpected or mutating API access: " + method)
        answer = self.answers.get(method, MISSING)
        if answer is MISSING:
            self.recorder.calls.append((self.label, method, "missing"))
            raise AttributeError(method)

        def invoke(*args):
            self.recorder.calls.append((self.label, method, args))
            value = answer.lookup(args) if isinstance(answer, ByArgs) else answer
            if isinstance(value, Failure):
                raise RuntimeError("Simulated getter failure")
            return value

        return invoke


class SnapshotContractTests(unittest.TestCase):
    def setUp(self):
        self.rec = Recorder()
        self.clip1 = self.graph("clip_1", 1, "clip-one.cube")
        self.clip2 = self.graph("clip_2", 2, "clip-two.cube")
        self.timeline_graph = self.graph("timeline_graph", 1, "timeline.cube")
        self.pre_graph = self.graph("group_pre", 1, "group-pre.cube")
        self.post_graph = self.graph("group_post", 0)
        self.group = self.fake("group", "group", GetName="Scene group",
                               GetPreClipNodeGraph=self.pre_graph,
                               GetPostClipNodeGraph=self.post_graph)
        self.media = self.fake("media", "media", GetClipProperty=ByArgs({
            ("Camera Type",): "Test camera", ("Gamma Notes",): "Test gamma"}),
            GetMetadata=ByArgs({}))
        self.item = self.fake("item", "item", GetName="/private/source/test.mxf",
                              GetMediaPoolItem=self.media,
                              GetCurrentVersion={"versionName": "Original", "versionType": 0},
                              GetVersionNameList=["Original", "Alternate"],
                              GetNodeGraph=ByArgs({(): self.clip1, (1,): self.clip1,
                                                   (2,): self.clip2}),
                              GetColorGroup=self.group)
        self.timeline = self.fake("timeline", "timeline", GetName="Current timeline",
                                  GetCurrentVideoItem=self.item,
                                  GetCurrentTimecode="01:00:04:12",
                                  GetSetting=ByArgs({}), GetNodeGraph=self.timeline_graph)
        self.project = self.fake("project", "project", GetName="Current project",
                                 GetCurrentTimeline=self.timeline,
                                 GetSetting=ByArgs({("nodeStackLayers",): "2"}))
        self.manager = self.fake("manager", "manager", GetCurrentProject=self.project)
        self.resolve = self.fake("resolve", "resolve", GetCurrentPage="color",
                                 GetProjectManager=self.manager)

    def fake(self, role, label, **answers):
        return Fake(self.rec, role, label, **answers)

    def graph(self, label, count, lut=""):
        return self.fake("graph", label, GetNumNodes=count,
                         GetLUT=ByArgs({(1,): "/private/luts/" + lut if lut else ""}, ""),
                         GetToolsInNode=ByArgs({}, ["Corrector"]))

    def capture(self):
        before = self.rec.state()
        with patch.object(helper, "load_resolve_module", side_effect=AssertionError(
            "Live Resolve access forbidden")):
            result = helper.snapshot(self.resolve)
        self.assertEqual(self.rec.state(), before, "Getter source data was mutated")
        self.assertEqual(self.rec.forbidden, [], "Unexpected/mutating API access")
        return result

    def assert_clip_layers_preserved(self, result):
        self.assertEqual([g["layer"] for g in result["clip_node_graphs"]], [1, 2])
        self.assertEqual([g["node_count"] for g in result["clip_node_graphs"]], [1, 2])
        self.assertEqual(result["grade_versions"]["local_names"], ["Original", "Alternate"])

    def test_all_scopes_keep_their_own_graphs_and_clip_layers(self):
        result = self.capture()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["current_page"], "color")
        self.assertEqual(self.rec.calls[0], ("resolve", "GetCurrentPage", ()))
        self.assert_clip_layers_preserved(result)
        self.assertEqual(result["timeline_node_graph"]["nodes"][0]["lut_filename"],
                         "timeline.cube")
        group = result["color_group"]
        self.assertEqual(group["status"], "ok")
        self.assertEqual(group["name"], "Scene group")
        self.assertEqual(group["pre_clip_node_graph"]["nodes"][0]["lut_filename"],
                         "group-pre.cube")
        self.assertEqual(group["post_clip_node_graph"]["nodes"], [])
        self.assertNotIn("/private/", str(result))

    def test_non_color_page_stops_before_project_chain(self):
        for page in ("edit", "fusion", "media", "COLOR"):
            with self.subTest(page=page):
                self.resolve.answers["GetCurrentPage"] = page
                start = len(self.rec.calls)
                result = self.capture()
                self.assertEqual(result["status"], "not_color_page")
                self.assertEqual(self.rec.calls[start:], [("resolve", "GetCurrentPage", ())])

    def test_unknown_page_stops_before_project_chain(self):
        for page in (None, "", 0, False, [], Failure(), MISSING):
            with self.subTest(page=repr(page)):
                self.resolve.answers["GetCurrentPage"] = page
                start = len(self.rec.calls)
                result = self.capture()
                self.assertEqual(result["status"], "page_unavailable")
                calls = self.rec.calls[start:]
                self.assertEqual(len(calls), 1)
                self.assertEqual(calls[0][:2], ("resolve", "GetCurrentPage"))

    def test_successful_no_group_is_not_applicable(self):
        self.item.answers["GetColorGroup"] = None
        result = self.capture()
        group = result["color_group"]
        self.assertEqual(group["status"], "not_applicable")
        self.assertEqual(group["pre_clip_node_graph"]["status"], "not_applicable")
        self.assertEqual(group["post_clip_node_graph"]["status"], "not_applicable")
        self.assertEqual(result["timeline_node_graph"]["status"], "ok")
        self.assert_clip_layers_preserved(result)

    def test_failed_and_missing_group_getter_are_unknown(self):
        for answer in (Failure(), MISSING):
            with self.subTest(answer=type(answer).__name__):
                self.item.answers["GetColorGroup"] = answer
                group = self.capture()["color_group"]
                self.assertEqual(group["status"], "unknown")
                self.assertEqual(group["pre_clip_node_graph"]["status"], "unknown")
                self.assertEqual(group["post_clip_node_graph"]["status"], "unknown")

    def test_malformed_group_return_is_unknown_not_a_group_or_no_group(self):
        for answer in (False, 0, 1.2, "", [], {}, (), set()):
            with self.subTest(answer=repr(answer)):
                self.item.answers["GetColorGroup"] = answer
                result = self.capture()
                group = result["color_group"]
                self.assertEqual(group["status"], "unknown")
                self.assertEqual(group["pre_clip_node_graph"]["status"], "unknown")
                self.assertEqual(group["post_clip_node_graph"]["status"], "unknown")
                self.assert_clip_layers_preserved(result)
                self.assertEqual(result["timeline_node_graph"]["status"], "ok")

    def test_group_name_and_pre_graph_failures_do_not_hide_post_graph(self):
        self.group.answers["GetName"] = Failure()
        self.group.answers["GetPreClipNodeGraph"] = Failure()
        result = self.capture()
        group = result["color_group"]
        self.assertEqual(group["status"], "ok")
        self.assertEqual(group["name_status"], "unknown")
        self.assertIsNone(group["name"])
        self.assertEqual(group["pre_clip_node_graph"]["status"], "unknown")
        self.assertEqual(group["post_clip_node_graph"]["status"], "ok")
        self.assert_clip_layers_preserved(result)

    def test_timeline_getter_failure_does_not_hide_clip_or_group(self):
        self.timeline.answers["GetNodeGraph"] = Failure()
        result = self.capture()
        self.assertEqual(result["timeline_node_graph"]["status"], "unknown")
        self.assertEqual(result["color_group"]["pre_clip_node_graph"]["status"], "ok")
        self.assert_clip_layers_preserved(result)

    def test_no_project_returns_unknown_graph_context(self):
        self.manager.answers["GetCurrentProject"] = None
        result = self.capture()
        self.assertEqual(result["status"], "no_current_project")
        self.assertEqual(result["clip_node_graphs"], [])
        self.assertEqual(result["timeline_node_graph"]["status"], "unknown")
        self.assertEqual(result["color_group"]["status"], "unknown")
        self.assertFalse(any(label == "project" for label, _, _ in self.rec.calls))

    def test_no_timeline_returns_unknown_group_not_no_group(self):
        self.project.answers["GetCurrentTimeline"] = None
        result = self.capture()
        self.assertEqual(result["status"], "no_current_timeline")
        self.assertEqual(result["timeline_node_graph"]["status"], "unknown")
        self.assertEqual(result["color_group"]["status"], "unknown")
        self.assertFalse(any(label == "timeline" for label, _, _ in self.rec.calls))

    def test_no_current_item_still_reads_timeline_graph(self):
        self.timeline.answers["GetCurrentVideoItem"] = None
        result = self.capture()
        self.assertEqual(result["status"], "no_current_video_item")
        self.assertEqual(result["clip_node_graphs"], [])
        self.assertEqual(result["timeline_node_graph"]["status"], "ok")
        self.assertEqual(result["color_group"]["status"], "unknown")
        self.assertFalse(any(label == "item" for label, _, _ in self.rec.calls))

    def test_graph_returning_none_is_unknown_not_empty(self):
        self.timeline.answers["GetNodeGraph"] = None
        graph = self.capture()["timeline_node_graph"]
        self.assertEqual(graph["status"], "unknown")
        self.assertIsNone(graph["node_count"])
        self.assertIsNone(graph["nodes"])

    def test_zero_nodes_is_known_empty_graph(self):
        self.timeline_graph.answers["GetNumNodes"] = 0
        graph = self.capture()["timeline_node_graph"]
        self.assertEqual(graph["status"], "ok")
        self.assertEqual(graph["node_count"], 0)
        self.assertEqual(graph["nodes"], [])
        self.assertFalse(any(label == "timeline_graph" and method in
                             {"GetLUT", "GetToolsInNode"}
                             for label, method, _ in self.rec.calls))

    def test_malformed_counts_are_unknown_without_index_reads(self):
        for count in (True, False, -1, "2", 2.0, 2.5, None, [], {}):
            with self.subTest(count=repr(count)):
                self.timeline_graph.answers["GetNumNodes"] = count
                calls_before = len(self.rec.calls)
                result = self.capture()
                graph = result["timeline_node_graph"]
                self.assertEqual(graph["status"], "unknown")
                self.assertIsNone(graph["node_count"])
                self.assertIsNone(graph["nodes"])
                self.assert_clip_layers_preserved(result)
                self.assertEqual(result["color_group"]["post_clip_node_graph"]["status"], "ok")
                self.assertFalse(any(label == "timeline_graph" and method in
                                     {"GetLUT", "GetToolsInNode"}
                                     for label, method, _ in self.rec.calls[calls_before:]))

    def test_failed_node_count_is_unknown_and_other_scopes_survive(self):
        self.pre_graph.answers["GetNumNodes"] = Failure()
        result = self.capture()
        self.assertEqual(result["color_group"]["pre_clip_node_graph"]["status"], "unknown")
        self.assertEqual(result["color_group"]["post_clip_node_graph"]["status"], "ok")
        self.assertEqual(result["timeline_node_graph"]["status"], "ok")
        self.assert_clip_layers_preserved(result)

    def test_missing_middle_clip_layer_does_not_drop_later_layer(self):
        third = self.graph("clip_3", 3)
        self.project.answers["GetSetting"] = ByArgs({("nodeStackLayers",): "3"})
        self.item.answers["GetNodeGraph"] = ByArgs({(1,): self.clip1, (2,): None, (3,): third})
        result = self.capture()
        layers = result["clip_node_graphs"]
        self.assertEqual([g["layer"] for g in layers], [1, 2, 3])
        self.assertEqual([g["status"] for g in layers], ["ok", "unknown", "ok"])
        self.assertEqual(layers[2]["node_count"], 3)

    def test_unknown_layer_count_uses_documented_default_first_layer(self):
        self.project.answers["GetSetting"] = ByArgs({})
        result = self.capture()
        self.assertEqual([g["layer"] for g in result["clip_node_graphs"]], [1])
        calls = [args for label, method, args in self.rec.calls
                 if label == "item" and method == "GetNodeGraph"]
        self.assertEqual(calls, [()])
        self.assertEqual(result["timeline_node_graph"]["status"], "ok")
        self.assertEqual(result["color_group"]["status"], "ok")

    def test_failed_lut_does_not_drop_other_node_details_or_layers(self):
        self.clip1.answers["GetLUT"] = Failure()
        self.clip1.answers["GetToolsInNode"] = ["Corrector", 12, None, "Color Space Transform"]
        result = self.capture()
        self.assert_clip_layers_preserved(result)
        self.assertEqual(result["clip_node_graphs"][0]["status"], "unknown")
        node = result["clip_node_graphs"][0]["nodes"][0]
        self.assertIsNone(node["lut_filename"])
        self.assertEqual(node["tool_names"], ["Corrector", "Color Space Transform"])
        self.assertEqual(node["tools_status"], "unknown")


if __name__ == "__main__":
    unittest.main(verbosity=2)
