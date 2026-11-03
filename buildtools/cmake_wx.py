"""
Helpers for building wxWidgets with CMake.

This replaces the old MSW build, which edited include/wx/msw/setup.h in place
and drove ``nmake -f makefile.vc``.  Everything here is kept free of side
effects (command lines are *returned*, not run) so that it can be unit tested
on any platform; build_wxwidgets.py is the thing that actually executes them.
"""

import os
import shutil
import subprocess
import sys

# Minimum CMake needed by the wxWidgets build system we drive.
CMAKE_MINIMUM = (3, 15)

# Name of the folder, below <wxRoot>/build, used for MSW builds.  One folder
# per architecture so that building for several Pythons does not clash (the
# old makefile.vc build did the same thing with lib/vcNNN_<arch>_dll).
MSW_BUILD_PREFIX = "cmake-msw"


def findCMake():
    """Return the path to the cmake executable, or None."""
    return shutil.which(os.environ.get("CMAKE", "cmake"))


def cmakeVersion(cmake):
    out = subprocess.run([cmake, "--version"], capture_output=True, text=True).stdout
    try:
        return tuple(int(i) for i in out.split()[2].split("-")[0].split(".")[:2])
    except (IndexError, ValueError):
        return None


def mswArch(cpu=None, python64=None):
    """
    Return 'x64', 'arm64' or 'x86' for the MSW build.  This is the same
    decision build_wxpy.getMSWSettings has always made: the CPU environment
    variable (set up by the MSVC environment) wins, otherwise the bitness of
    the target Python.
    """
    if cpu is None:
        cpu = os.environ.get("CPU")
    if python64 is None:
        python64 = sys.maxsize > 2**32
    if cpu == "ARM64":
        return "arm64"
    if cpu in ("AMD64", "X64") or python64:
        return "x64"
    return "x86"


def mswBuildDir(wxRoot, arch):
    """The CMake binary directory for an MSW build."""
    return os.path.join(wxRoot, "build", "%s-%s" % (MSW_BUILD_PREFIX, arch))


def mswLibDir(wxRoot, arch):
    """
    The folder where wx's DLLs, import libs and the generated
    ``msw[u|ud]/wx/setup.h`` end up.  This is wxWidgets' own naming
    (see wxPLATFORM_LIB_DIR in build/cmake/init.cmake) and differs from the
    old makefile.vc layout in that it has no compiler version in it: the
    old ``lib/vc140_x64_dll`` is now ``build/cmake-msw-x64/lib/vc_x64_dll``.
    """
    suffix = "" if arch == "x86" else "_" + arch
    return os.path.join(mswBuildDir(wxRoot, arch), "lib", "vc%s_dll" % suffix)


def _onoff(value):
    return "ON" if value else "OFF"


def cacheFile():
    """The static initial cache holding the settings every wxPython build shares."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "cmake", "wxpython.cmake")


def configureArgs(wxRoot, buildDir, *, msw, debug=False, wxpython=False,
                  cairo=False, no_msedge=False, no_dpi_aware=False, gtk2=False,
                  set_rpath_origin=False, prefix=None, generator=None,
                  arch=None, mac_arch=None, features=(), shared=True):
    """
    Build the ``cmake`` configure command line (as a list).

    The fixed wxPython feature set is in buildtools/cmake/wxpython.cmake and
    is loaded with -C.  Only what varies from build to build is given as -D
    here (command line values win over the initial cache).
    """
    args = ["-S", wxRoot, "-B", buildDir]
    if wxpython:
        args += ["-C", cacheFile()]
    if generator:
        args += ["-G", generator]
    effective_gen = generator or os.environ.get("CMAKE_GENERATOR") or ""
    # With nothing specified CMake picks a Visual Studio generator on MSW.
    is_vs = (not effective_gen) or effective_gen.startswith("Visual Studio")
    if msw and arch == "arm64" and not is_vs:
        raise ValueError("ARM64 builds need a Visual Studio generator: wxWidgets' CMake "
                         "build can't tell it is cross building for ARM64 with %r" % effective_gen)
    if msw and arch and is_vs:
        # Only the Visual Studio generators take -A; Ninja & co. get their
        # architecture from the compiler environment (vcvars).
        args += ["-A", {"x64": "x64", "arm64": "ARM64", "x86": "Win32"}[arch]]

    D = []
    if not wxpython:
        D.append(("wxBUILD_SHARED", _onoff(shared)))
    # Single-config generators need the build type at configure time.
    # (Multi-config ones, like Visual Studio, ignore it and take --config.)
    D.append(("CMAKE_BUILD_TYPE", "Debug" if debug else "Release"))
    if prefix:
        D.append(("CMAKE_INSTALL_PREFIX", prefix))

    if msw:
        if no_msedge:
            D.append(("wxUSE_WEBVIEW_EDGE", "OFF"))
        if no_dpi_aware:
            D.append(("wxUSE_DPI_AWARE_MANIFEST", "none"))
        if cairo:
            D.append(("wxUSE_CAIRO", "ON"))
            # wx only needs the headers; the cairo DLL is loaded at runtime.
            # But its FindCairo module insists on both variables being set,
            # otherwise it silently turns wxUSE_CAIRO back off.
            root = cairo if isinstance(cairo, str) else ""
            D.append(("CAIRO_INCLUDE_DIRS", os.path.join(root, "include", "cairo")))
            D.append(("CAIRO_LIBRARIES", os.path.join(root, "lib", "cairo-placeholder.lib")))
    else:
        if gtk2:
            D.append(("wxBUILD_TOOLKIT", "gtk2"))
        elif sys.platform != "darwin":
            D.append(("wxBUILD_TOOLKIT", "gtk3"))
        if mac_arch:
            D.append(("CMAKE_OSX_ARCHITECTURES", mac_arch.replace(",", ";")))
        if set_rpath_origin:
            # Use only $ORIGIN, not the absolute build tree path as well.
            D.append(("CMAKE_BUILD_WITH_INSTALL_RPATH", "ON"))
            D.append(("CMAKE_INSTALL_RPATH", "$ORIGIN"))

    for d in D:
        args.append("-D%s=%s" % d)

    # Free-form extras: "wxUSE_FOO=ON" / "-DFOO=bar"
    for feat in features:
        feat = feat.strip()
        if not feat:
            continue
        if feat.startswith("--"):
            raise ValueError("%r looks like an autoconf option; with CMake give wxUSE_XXX=ON/OFF "
                             "or -DNAME=value" % feat)
        args.append(feat if feat.startswith("-D") else "-D" + feat)
    return args


def buildArgs(buildDir, *, debug=False, jobs=None, targets=(), extra=()):
    args = ["--build", buildDir, "--config", "Debug" if debug else "Release"]
    if jobs:
        args += ["--parallel", str(jobs)]
    for t in targets:
        args += ["--target", t]
    if extra:
        args += ["--"] + list(extra)
    return args


def installArgs(buildDir, *, debug=False):
    # DESTDIR, if wanted, is passed to cmake through the environment.
    return ["--install", buildDir, "--config", "Debug" if debug else "Release"]


def run(cmake, args, env=None, verbose=True):
    cmd = [cmake] + list(args)
    if verbose:
        print(" ".join(cmd))
    return subprocess.run(cmd, env=env).returncode
