# Initial CMake cache for the wxWidgets build that wxPython bundles.
#
# Used as:  cmake -C buildtools/cmake/wxpython.cmake -S ext/wxWidgets -B <dir>
#
# Everything that is the same for every wxPython build lives here, as plain
# data.  The few things that really vary per build (build type, architecture,
# install prefix, GTK version, optional features like Cairo) are given on the
# command line by buildtools/cmake_wx.py, and override what is set here.
#
# Note: initial-cache scripts run before project(), so only the CMAKE_HOST_*
# variables are available here, not WIN32/APPLE/UNIX.

set(wxBUILD_SHARED     ON  CACHE BOOL "")
set(wxBUILD_MONOLITHIC OFF CACHE BOOL "")
set(wxBUILD_SAMPLES    OFF CACHE STRING "")
set(wxBUILD_TESTS      OFF CACHE STRING "")
set(wxBUILD_DEMOS      OFF CACHE BOOL "")

# Features wxPython needs (these were the setup.h / ./configure tweaks)
set(wxUSE_GRAPHICS_CONTEXT ON  CACHE BOOL "")
set(wxUSE_OPENGL           ON  CACHE BOOL "")   # implies wxUSE_GLCANVAS
set(wxUSE_DISPLAY          ON  CACHE BOOL "")
set(wxUSE_POSTSCRIPT       ON  CACHE BOOL "")
set(wxUSE_AFM_FOR_POSTSCRIPT OFF CACHE BOOL "")
set(wxUSE_IFF              ON  CACHE BOOL "")
set(wxUSE_UIACTIONSIMULATOR ON CACHE BOOL "")
set(wxUSE_DEBUGREPORT      OFF CACHE BOOL "")
# wx.NewIdRef() relies on this; it is on by default for MSW only, but the
# autoconf build always had --enable-autoidman.
set(wxUSE_AUTOID_MANAGEMENT ON CACHE BOOL "")
# These two are plain #cmakedefine01 variables in setup.h.in, not options.
set(wxUSE_DATEPICKCTRL_GENERIC ON  CACHE BOOL "")
set(wxDIALOG_UNIT_COMPATIBILITY OFF CACHE BOOL "")

if(CMAKE_HOST_WIN32)
    set(wxBUILD_VENDOR "" CACHE STRING "")          # no "_custom" in the DLL names
    set(wxBUILD_MSVC_MULTIPROC ON CACHE BOOL "")
    set(wxUSE_ACCESSIBILITY ON  CACHE BOOL "")
    set(wxUSE_WINRT         OFF CACHE BOOL "")
    set(wxUSE_DIALUP_MANAGER OFF CACHE BOOL "")
    set(wxUSE_WEBVIEW_EDGE  ON  CACHE BOOL "")      # --no_msedge turns this off
    set(wxUSE_DPI_AWARE_MANIFEST "per-monitor" CACHE STRING "")
    # Keep debug info in release builds, as makefile.vc's DEBUG_INFO=1 did,
    # so that --relwithdebug produces useful PDBs.
    set(CMAKE_C_FLAGS_RELEASE   "/O2 /Ob2 /DNDEBUG /Zi" CACHE STRING "")
    set(CMAKE_CXX_FLAGS_RELEASE "/O2 /Ob2 /DNDEBUG /Zi" CACHE STRING "")
endif()
