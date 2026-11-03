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
                                open(cmake_wx.cacheFile()).read(), re.M))
        for k, v in dict(wxBUILD_SHARED="ON", wxBUILD_MONOLITHIC="OFF",
                         wxUSE_GRAPHICS_CONTEXT="ON", wxUSE_OPENGL="ON",
                         wxUSE_DEBUGREPORT="OFF", wxUSE_WINRT="OFF",
                         wxUSE_WEBVIEW_EDGE="ON", wxUSE_ACCESSIBILITY="ON",
                         wxUSE_DATEPICKCTRL_GENERIC="ON", wxUSE_UIACTIONSIMULATOR="ON",
                         wxUSE_IFF="ON", wxUSE_DPI_AWARE_MANIFEST='"per-monitor"',
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

    def test_mac_arch_default(self):
        d = defs(cmake_wx.configureArgs("src", "bld", msw=False, mac_arch="default"))
        self.assertEqual(d["CMAKE_OSX_ARCHITECTURES"], "arm64;x86_64")


class CacheTests(unittest.TestCase):
    def test_reset_when_cache_file_changes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            cache = os.path.join(d, "CMakeCache.txt")
            open(cache, "w").write("x")
            # unknown stamp: treated as changed
            self.assertTrue(cmake_wx.resetStaleCache(d))
            open(cache, "w").write("x")
            # same static cache file as last time: left alone
            self.assertFalse(cmake_wx.resetStaleCache(d))
            self.assertTrue(os.path.exists(cache))
            # forced
            self.assertTrue(cmake_wx.resetStaleCache(d, force=True))
            self.assertFalse(os.path.exists(cache))

    def test_no_cache_nothing_to_do(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(cmake_wx.resetStaleCache(d))


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
                text += open(f, encoding="utf-8", errors="replace").read()
        names = re.findall(r"^\s*set\((\w+)\s", open(cmake_wx.cacheFile()).read(), re.M)
        names = [n for n in names if n.startswith("wx")]
        self.assertTrue(names)
        for n in names:
            self.assertIn(n, text, "%s is not known to wxWidgets' CMake files" % n)


class BuildArgTests(unittest.TestCase):
    def test_build(self):
        a = cmake_wx.buildArgs("bld", debug=True, jobs=4, extra=["-v"])
        self.assertEqual(a, ["--build", "bld", "--config", "Debug",
                             "--parallel", "4", "--", "-v"])


if __name__ == "__main__":
    unittest.main()
