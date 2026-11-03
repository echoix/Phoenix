"""
Tests for buildtools/cmake_wx.py, the command-line generation for the CMake
based wxWidgets build.  Nothing here needs CMake or a compiler.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
from buildtools import cmake_wx


WXCMAKE = os.path.join(os.path.dirname(__file__), os.pardir, "ext", "wxWidgets")


class _NoGeneratorEnv(unittest.TestCase):
    """Make the tests independent of a CMAKE_GENERATOR set in the environment."""
    def setUp(self):
        self._gen = os.environ.pop("CMAKE_GENERATOR", None)

    def tearDown(self):
        if self._gen is not None:
            os.environ["CMAKE_GENERATOR"] = self._gen


def _read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def defs(args):
    out = {}
    for a in args:
        if a.startswith("-D"):
            k, _, v = a[2:].partition("=")
            out[k] = v
    return out


class ArchTests(unittest.TestCase):
    def test_arch(self):
        self.assertEqual(cmake_wx.mswArch("ARM64", True), "arm64")
        self.assertEqual(cmake_wx.mswArch("AMD64", False), "x64")
        self.assertEqual(cmake_wx.mswArch("X64", True), "x64")
        self.assertEqual(cmake_wx.mswArch(None, True), "x64")
        self.assertEqual(cmake_wx.mswArch("", False), "x86")

    def test_libdir(self):
        d = cmake_wx.mswLibDir("wx", "x64").replace("\\", "/")
        self.assertTrue(d.endswith("build/cmake-msw-x64/lib/vc_x64_dll"), d)
        d = cmake_wx.mswLibDir("wx", "arm64").replace("\\", "/")
        self.assertTrue(d.endswith("lib/vc_arm64_dll"), d)
        d = cmake_wx.mswLibDir("wx", "x86").replace("\\", "/")
        self.assertTrue(d.endswith("lib/vc_dll"), d)


class MswConfigureTests(_NoGeneratorEnv):
    def cfg(self, **kw):
        kw.setdefault("msw", True)
        kw.setdefault("wxpython", True)
        kw.setdefault("arch", "x64")
        return cmake_wx.configureArgs("src", "bld", **kw)

    def test_static_cache_file(self):
        a = self.cfg()
        self.assertEqual(a[a.index("-C") + 1], cmake_wx.cacheFile())
        self.assertTrue(os.path.exists(cmake_wx.cacheFile()))
        self.assertNotIn("-C", self.cfg(wxpython=False))

    def test_cache_file_contents(self):
        # The feature set wxPython needs is plain data in the cache file.
        import re
        cache = dict(re.findall(r'^\s*set\((\w+)\s+("[^"]*"|[^\s)]+)\s+CACHE',
                                _read(cmake_wx.cacheFile()), re.M))
        for k, v in dict(wxBUILD_SHARED="ON", wxBUILD_MONOLITHIC="OFF",
                         wxUSE_GRAPHICS_CONTEXT="ON", wxUSE_OPENGL="ON",
                         wxUSE_DEBUGREPORT="OFF", wxUSE_WINRT="OFF",
                         wxUSE_WEBVIEW_EDGE="ON", wxUSE_ACCESSIBILITY="ON",
                         wxUSE_DATEPICKCTRL_GENERIC="ON", wxUSE_UIACTIONSIMULATOR="ON",
                         wxUSE_IFF="ON", wxUSE_AUTOID_MANAGEMENT="ON", wxUSE_DPI_AWARE_MANIFEST='"per-monitor"',
                         wxBUILD_VENDOR='""').items():
            self.assertEqual(cache.get(k), v, k)
        self.assertIn("/Zi", cache["CMAKE_CXX_FLAGS_RELEASE"])

    def test_options(self):
        d = defs(self.cfg(no_msedge=True, no_dpi_aware=True, debug=True, cairo=True))
        self.assertEqual(d["wxUSE_WEBVIEW_EDGE"], "OFF")
        self.assertEqual(d["wxUSE_DPI_AWARE_MANIFEST"], "none")
        dflt = defs(self.cfg())
        self.assertEqual(dflt["wxUSE_WEBVIEW_EDGE"], "ON")
        self.assertEqual(dflt["wxUSE_DPI_AWARE_MANIFEST"], "per-monitor")
        self.assertEqual(dflt["wxUSE_CAIRO"], "OFF")
        self.assertEqual(d["CMAKE_BUILD_TYPE"], "Debug")
        self.assertEqual(d["wxUSE_CAIRO"], "ON")

    def test_arch_flag_only_for_vs_generators(self):
        self.assertEqual(self.cfg()[self.cfg().index("-A") + 1], "x64")
        self.assertIn("ARM64", self.cfg(arch="arm64"))
        self.assertIn("Win32", self.cfg(arch="x86"))
        self.assertIn("-A", self.cfg(generator="Visual Studio 17 2022"))
        self.assertNotIn("-A", self.cfg(generator="Ninja"))

    def test_cairo_placeholders(self):
        d = defs(self.cfg(cairo="C:/cairo"))
        self.assertEqual(d["wxUSE_CAIRO"], "ON")
        self.assertIn("cairo", d["CAIRO_INCLUDE_DIRS"])
        self.assertIn("CAIRO_LIBRARIES", d)
        self.assertNotIn("CAIRO_LIBRARIES", defs(self.cfg()))
        self.assertEqual(defs(self.cfg())["wxUSE_CAIRO"], "OFF")

    def test_generator_from_environment(self):
        old = os.environ.get("CMAKE_GENERATOR")
        try:
            os.environ["CMAKE_GENERATOR"] = "Ninja"
            self.assertNotIn("-A", self.cfg())
            with self.assertRaises(ValueError):
                self.cfg(arch="arm64")
            os.environ["CMAKE_GENERATOR"] = "Visual Studio 17 2022"
            self.assertIn("-A", self.cfg())
        finally:
            if old is None:
                os.environ.pop("CMAKE_GENERATOR", None)
            else:
                os.environ["CMAKE_GENERATOR"] = old

    def test_features_passthrough(self):
        a = self.cfg(features=["wxUSE_FOO=ON", "-DBAR=1", ""])
        self.assertIn("-DwxUSE_FOO=ON", a)
        self.assertIn("-DBAR=1", a)
        with self.assertRaises(ValueError):
            self.cfg(features=["--enable-foo"])


class PosixConfigureTests(_NoGeneratorEnv):
    def test_posix(self):
        a = cmake_wx.configureArgs("src", "bld", msw=False, wxpython=True,
                                   set_rpath_origin=True, prefix="/p")
        d = defs(a)
        self.assertNotIn("-A", a)
        if sys.platform == "darwin":
            self.assertNotIn("wxBUILD_TOOLKIT", d)   # wx picks osx_cocoa itself
        else:
            self.assertEqual(d["wxBUILD_TOOLKIT"], "gtk3")
        self.assertEqual(d["CMAKE_INSTALL_RPATH"], "$ORIGIN")
        self.assertEqual(d["CMAKE_BUILD_WITH_INSTALL_RPATH"], "ON")
        self.assertEqual(d["CMAKE_INSTALL_PREFIX"], "/p")
        self.assertNotIn("wxUSE_WEBVIEW_EDGE", d)

    def test_switches_are_explicit_when_off(self):
        # Values from an earlier configure stay in CMakeCache.txt, so a switch
        # that is off must be passed as off, not left out.
        d = defs(cmake_wx.configureArgs("src", "bld", msw=False, wxpython=True))
        self.assertEqual(d["CMAKE_BUILD_WITH_INSTALL_RPATH"], "OFF")
        self.assertEqual(d["CMAKE_INSTALL_RPATH"], "")

    def test_sometimes_wanted_values_are_unset_when_absent(self):
        a = cmake_wx.configureArgs("src", "bld", msw=False)
        self.assertIn("-UCMAKE_INSTALL_PREFIX", a)
        self.assertIn("-UCMAKE_OSX_ARCHITECTURES", a)
        a = cmake_wx.configureArgs("src", "bld", msw=False, prefix="/p", mac_arch="arm64")
        self.assertNotIn("-UCMAKE_INSTALL_PREFIX", a)
        self.assertNotIn("-UCMAKE_OSX_ARCHITECTURES", a)

    def test_mac_arch_default(self):
        d = defs(cmake_wx.configureArgs("src", "bld", msw=False, mac_arch="default"))
        self.assertEqual(d["CMAKE_OSX_ARCHITECTURES"], "arm64;x86_64")


def _fake_cache(d, home):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "CMakeCache.txt"), "w") as f:
        f.write("CMAKE_HOME_DIRECTORY:INTERNAL=%s\n" % home)


class CacheTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = os.path.join(self._tmp.name, "wx")
        os.makedirs(self.root)
        self.bld = os.path.join(self._tmp.name, "bld")

    def test_no_cache_nothing_to_do(self):
        self.assertFalse(cmake_wx.resetStaleCache(self.bld, self.root))
        os.makedirs(self.bld)
        self.assertFalse(cmake_wx.resetStaleCache(self.bld, self.root))

    def test_unrecorded_cache_is_reset_then_left_alone(self):
        _fake_cache(self.bld, self.root)
        # never recorded as configured by us: start from scratch
        self.assertTrue(cmake_wx.resetStaleCache(self.bld, self.root))
        # a configure happens and is recorded...
        _fake_cache(self.bld, self.root)
        cmake_wx.recordCache(self.bld)
        # ...so the next run keeps it.
        self.assertFalse(cmake_wx.resetStaleCache(self.bld, self.root))
        self.assertTrue(os.path.exists(os.path.join(self.bld, "CMakeCache.txt")))

    def test_stamp_is_not_written_by_reset(self):
        # First run on a fresh dir must not make the second run discard the cache
        # (the stamp is only written after a successful configure).
        self.assertFalse(cmake_wx.resetStaleCache(self.bld, self.root))
        self.assertFalse(os.path.exists(self.bld))
        _fake_cache(self.bld, self.root)
        cmake_wx.recordCache(self.bld)
        self.assertFalse(cmake_wx.resetStaleCache(self.bld, self.root))

    def test_changed_cache_file_resets(self):
        _fake_cache(self.bld, self.root)
        with open(os.path.join(self.bld, ".wxpython-cache-stamp"), "w") as f:
            f.write("not the hash of the current file")
        self.assertTrue(cmake_wx.resetStaleCache(self.bld, self.root))

    def test_force(self):
        _fake_cache(self.bld, self.root)
        cmake_wx.recordCache(self.bld)
        self.assertTrue(cmake_wx.resetStaleCache(self.bld, self.root, force=True))
        self.assertFalse(os.path.exists(os.path.join(self.bld, "CMakeCache.txt")))

    def test_refuses_foreign_cache(self):
        _fake_cache(self.bld, os.path.join(self._tmp.name, "other-project"))
        with self.assertRaises(ValueError):
            cmake_wx.resetStaleCache(self.bld, self.root)
        self.assertTrue(os.path.exists(os.path.join(self.bld, "CMakeCache.txt")))

    def test_clean_only_removes_our_trees(self):
        _fake_cache(self.bld, os.path.join(self._tmp.name, "other-project"))
        with self.assertRaises(ValueError):
            cmake_wx.cleanBuildDir(self.bld, self.root)
        self.assertTrue(os.path.isdir(self.bld))
        _fake_cache(self.bld, self.root)
        self.assertTrue(cmake_wx.cleanBuildDir(self.bld, self.root))
        self.assertFalse(os.path.exists(self.bld))
        self.assertFalse(cmake_wx.cleanBuildDir(self.bld, self.root))
        # an arbitrary non-CMake folder is not touched either
        os.makedirs(self.bld)
        with self.assertRaises(ValueError):
            cmake_wx.cleanBuildDir(self.bld, self.root)


@unittest.skipUnless(os.path.isdir(os.path.join(WXCMAKE, "build", "cmake")),
                     "wxWidgets sources not available")
class NamesExistInWxTests(unittest.TestCase):
    """The names we set must be ones wxWidgets' CMake files actually use."""
    def test_names(self):
        import glob
        import re
        text = ""
        for pat in ("build/cmake/**/*.cmake", "build/cmake/**/CMakeLists.txt",
                    "build/cmake/setup.h.in", "CMakeLists.txt"):
            for f in glob.glob(os.path.join(WXCMAKE, pat), recursive=True):
                text += _read(f)
        names = re.findall(r"^\s*set\((\w+)\s", _read(cmake_wx.cacheFile()), re.M)
        names = [n for n in names if n.startswith("wx")]
        self.assertTrue(names)
        for n in names:
            self.assertIn(n, text, "%s is not known to wxWidgets' CMake files" % n)


@unittest.skipUnless(os.path.isdir(os.path.join(WXCMAKE, "build", "cmake")),
                     "wxWidgets sources not available")
class DriverTests(_NoGeneratorEnv):
    """buildtools.build_wxwidgets.main with cmake mocked out."""
    def run_main(self, *extra, existing=False):
        import tempfile
        from unittest import mock
        from buildtools import build_wxwidgets as bw
        calls = []
        with tempfile.TemporaryDirectory() as tmp:
            bld = os.path.join(tmp, "bld")
            if existing:
                _fake_cache(bld, os.path.realpath(WXCMAKE))
                cmake_wx.recordCache(bld)
            def fake_run(cmake, args, env=None, verbose=True):
                calls.append(list(args))
                if args[0] == "-S":            # configure creates the cache
                    _fake_cache(bld, os.path.realpath(WXCMAKE))
                return 0
            with mock.patch.object(cmake_wx, "run", fake_run), \
                 mock.patch.object(cmake_wx, "findCMake", lambda: "cmake"), \
                 mock.patch.object(cmake_wx, "cmakeVersion", lambda c: (3, 28)), \
                 mock.patch.object(sys, "platform", "linux"):
                bw.exitWithException = True
                try:
                    bw.main(os.path.realpath(WXCMAKE),
                            ["--wxpython", "--builddir=" + bld] + list(extra))
                except SystemExit as e:
                    calls.append(("exit", e.code))
            stamp = os.path.exists(os.path.join(bld, ".wxpython-cache-stamp"))
        return calls, stamp

    def test_configure_twice_on_fresh_tree_then_build_and_stamp(self):
        calls, stamp = self.run_main("--jobs=3")
        self.assertEqual(calls[0][0], "-S")
        self.assertIn("-C", calls[0])
        # wx's CMake settles setup.h only on the second configure of a tree
        self.assertEqual(calls[1], calls[0])
        self.assertEqual(calls[2][:2], ["--build", calls[2][1]])
        self.assertIn("3", calls[2])
        self.assertTrue(stamp)

    def test_configure_once_on_existing_tree(self):
        calls, _ = self.run_main("--jobs=3", existing=True)
        self.assertEqual([c[0] for c in calls], ["-S", "--build"])

    def test_extra_make_is_split(self):
        calls, _ = self.run_main("--extra_make=-k VERBOSE=0")
        self.assertEqual(calls[-1][-3:], ["--", "-k", "VERBOSE=0"])

    def test_clean_requires_builddir(self):
        from buildtools import build_wxwidgets as bw
        with self.assertRaises(SystemExit):
            bw.main(os.path.realpath(WXCMAKE), ["--clean"])


class BuildArgTests(unittest.TestCase):
    def test_build(self):
        a = cmake_wx.buildArgs("bld", debug=True, jobs=4, extra=["-v"])
        self.assertEqual(a, ["--build", "bld", "--config", "Debug",
                             "--parallel", "4", "--", "-v"])


if __name__ == "__main__":
    unittest.main()
