"""
Tests for buildtools/cmake_wx.py, the command-line generation for the CMake
based wxWidgets build.  Nothing here needs CMake or a compiler.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
from buildtools import cmake_wx


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


class MswConfigureTests(unittest.TestCase):
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
        self.assertNotIn("wxUSE_WEBVIEW_EDGE", defs(self.cfg()))
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


class PosixConfigureTests(unittest.TestCase):
    def test_posix(self):
        a = cmake_wx.configureArgs("src", "bld", msw=False, wxpython=True,
                                   set_rpath_origin=True, prefix="/p")
        d = defs(a)
        self.assertNotIn("-A", a)
        self.assertIn("wxBUILD_TOOLKIT", d)
        self.assertEqual(d["CMAKE_INSTALL_RPATH"], "$ORIGIN")
        self.assertEqual(d["CMAKE_BUILD_WITH_INSTALL_RPATH"], "ON")
        self.assertEqual(d["CMAKE_INSTALL_PREFIX"], "/p")
        self.assertNotIn("wxUSE_WEBVIEW_EDGE", d)


class BuildArgTests(unittest.TestCase):
    def test_build(self):
        a = cmake_wx.buildArgs("bld", debug=True, jobs=4, extra=["-v"])
        self.assertEqual(a, ["--build", "bld", "--config", "Debug",
                             "--parallel", "4", "--", "-v"])


if __name__ == "__main__":
    unittest.main()
