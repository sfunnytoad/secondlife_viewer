import os

from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMakeDeps, CMakeToolchain
from conan.tools.microsoft import is_msvc
from conan.tools.build import check_min_cppstd


class SecondLifeViewer(ConanFile):
    version = "0.1.0"
    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/sfunnytoad/secondlife_viewer"
    homepage = "https://secondlife.com"
    name = "SecondLifeViewer"
    license = "GPL-3.0-or-later"
    author = ""

    options = {
    }

    default_options = {
    }

    def config_options(self):
        return

    def requirements(self):
        self.requires("vorbis/1.3.7")
        self.requires("xxhash/0.8.3")
        self.requires("openal/1.22.2")
        self.requires("hunspell/1.7.2")
        self.requires("apr/1.7.4")
        self.requires("apr-util/1.6.1")
        self.requires("boost/1.86.0")
        self.requires("expat/2.7.3")
        self.requires("tracy/0.12.2")
        self.requires("zlib/1.3.1")
        self.requires("glm/1.0.1")

    def validate(self):
        check_min_cppstd(self, "20")

    def generate(self):
        deps = CMakeDeps(self)
        # OGRE provides its own CMake files which we should use
        deps.set_property("ogre", "cmake_find_mode", "none")
        deps.generate()

        tc = CMakeToolchain(self)
        # We need to do some stuff differently if Conan is in use, so we'll tell the CMake system this.
        tc.variables["USE_CONAN"]           = "TRUE"
        tc.variables["LL_BUILD"]            = self.configure_ll_build()
        tc.variables["CMAKE_CXX_STANDARD"]  = "20"

        if self.settings.arch in ["x86_64"]:
            self.output.info("64-bit build detected.")
            tc.variables["ADDRESS_SIZE"] = "64"
        elif self.settings.arch in ["x86"]:
            self.output.info("32-bit build detected.")
            tc.variables["ADDRESS_SIZE"] = "32"
        else:
            self.output.error("Could not detect address size.")

        # tc.generator = "Ninja"
        tc.generate()

    def layout(self):
        cmake_layout(self)

    def configure_ll_build(self) -> str:
        LL_BUILD_WINDOWS_BASE_MACROS                = "/D_SECURE_STL=0 /D_HAS_ITERATOR_DEBUGGING=0 /DWIN32 /D_WINDOWS /DLL_WINDOWS=1 /DUNICODE /D_UNICODE /DWINVER=0x0602 /D_WIN32_WINNT=0x0602 /DLL_OS_DRAGDROP_ENABLED=1 /DLIB_NDOF=1"
        # removed the /SAFESEH:NO /NODEFAULTLIB:LIBCMT altogether. Earlier solution of inserting /LINK switch
        # earlier in the command line did not work for all projects. Removing switches entirely still works as expected.
        LL_BUILD_WINDOWS_BASE_SWITCHES              = "/std:c++20 /permissive- /Zc:wchar_t /Zi /GR /DEBUG"
        LL_BUILD_WINDOWS_BASE                       = f"{LL_BUILD_WINDOWS_BASE_SWITCHES} {LL_BUILD_WINDOWS_BASE_MACROS}"

        LL_BUILD_WINDOWS_RELEASE_MACROS             = f"/DLL_RELEASE=1 /DLL_RELEASE_FOR_DOWNLOAD=1 /DNDEBUG {LL_BUILD_WINDOWS_BASE_MACROS}"
        LL_BUILD_WINDOWS_RELEASE_SWITCHES           = f"/MD /O2 /Ob2 {LL_BUILD_WINDOWS_BASE_SWITCHES}"
        LL_BUILD_WINDOWS_RELEASE                    = f"{LL_BUILD_WINDOWS_RELEASE_SWITCHES} {LL_BUILD_WINDOWS_RELEASE_MACROS}"
        LL_BUILD_WINDOWS_RELEASEOS                  = f"{LL_BUILD_WINDOWS_RELEASE}"

        LL_BUILD_WINDOWS_RELWITHDEBINFO_MACROS      = f"/DLL_RELEASE=1 /DLL_RELEASE_WITH_DEBUG_INFO=1 /DNDEBUG {LL_BUILD_WINDOWS_BASE_MACROS}"
        LL_BUILD_WINDOWS_RELWITHDEBINFO_SWITCHES    = f"/MD /Od /Ob0 {LL_BUILD_WINDOWS_BASE_SWITCHES}"
        LL_BUILD_WINDOWS_RELWITHDEBINFO             = f"{LL_BUILD_WINDOWS_RELWITHDEBINFO_SWITCHES} {LL_BUILD_WINDOWS_RELWITHDEBINFO_MACROS}"
        LL_BUILD_WINDOWS_RELWITHDEBINFOOS           = f"{LL_BUILD_WINDOWS_RELWITHDEBINFO}"

        LL_BUILD_WINDOWS_DEBUG_MACROS               = f"/D_DEBUG /DLL_DEBUG=1 /D_SCL_SECURE_NO_WARNINGS=1 {LL_BUILD_WINDOWS_BASE_MACROS}"
        LL_BUILD_WINDOWS_DEBUG_SWITCHES             = f"/MDd /Od /NODEFAULTLIB:LIBCMTD /NODEFAULTLIB:MSVCRT {LL_BUILD_WINDOWS_BASE_SWITCHES}"
        LL_BUILD_WINDOWS_DEBUG                      = f"{LL_BUILD_WINDOWS_DEBUG_SWITCHES} {LL_BUILD_WINDOWS_DEBUG_MACROS}"
        LL_BUILD_WINDOWS_DEBUGOS                    = f"{LL_BUILD_WINDOWS_DEBUG}"

        # Mac and Linux common
        LL_BUILD_POSIX_BASE_MACROS                  = "-DPIC -DLL_OS_DRAGDROP_ENABLED=1"
        LL_BUILD_POSIX_BASE_SWITCHES                = "-std=c++20 -fPIC"

        # Mac
        LL_BUILD_DARWIN_DEPLOY_TARGET               = "11"
        LL_BUILD_DARWIN_BASE_MACROS                 = f"-DLL_DARWIN=1 -DLIB_NDOF=1 {LL_BUILD_POSIX_BASE_MACROS}"
        LL_BUILD_DARWIN_BASE_SWITCHES               = f"-g --debug -mmacosx-version-min={LL_BUILD_DARWIN_DEPLOY_TARGET} {LL_BUILD_POSIX_BASE_SWITCHES}"
        LL_BUILD_DARWIN_BASE                        = f"{LL_BUILD_DARWIN_BASE_SWITCHES} {LL_BUILD_DARWIN_BASE_MACROS}"

        LL_BUILD_DARWIN_RELEASE_MACROS              = "-DLL_RELEASE=1 -DLL_RELEASE_FOR_DOWNLOAD=1 -DNDEBUG {LL_BUILD_DARWIN_BASE_MACROS}"
        LL_BUILD_DARWIN_RELEASE_SWITCHES            = f"-O3 {LL_BUILD_DARWIN_BASE_SWITCHES}"
        LL_BUILD_DARWIN_RELEASE                     = f"{LL_BUILD_DARWIN_RELEASE_SWITCHES} {LL_BUILD_DARWIN_RELEASE_MACROS}"
        LL_BUILD_DARWIN_RELEASEOS                   = f"{LL_BUILD_DARWIN_RELEASE}"

        LL_BUILD_DARWIN_RELWITHDEBINFO_MACROS       = f"-DLL_RELEASE=1 -DNDEBUG -DLL_RELEASE_WITH_DEBUG_INFO=1 {LL_BUILD_DARWIN_BASE_MACROS}"
        LL_BUILD_DARWIN_RELWITHDEBINFO_SWITCHES     = f"-O0 {LL_BUILD_DARWIN_BASE_SWITCHES}"
        LL_BUILD_DARWIN_RELWITHDEBINFO              = f"{LL_BUILD_DARWIN_RELWITHDEBINFO_SWITCHES} {LL_BUILD_DARWIN_RELWITHDEBINFO_MACROS}"
        LL_BUILD_DARWIN_RELWITHDEBINFOOS            = f"{LL_BUILD_DARWIN_RELWITHDEBINFO}"

        LL_BUILD_DARWIN_DEBUG_MACROS                = f"-D_DEBUG -DLL_DEBUG=1 {LL_BUILD_DARWIN_BASE_MACROS}"
        LL_BUILD_DARWIN_DEBUG_SWITCHES              = f"-O0 {LL_BUILD_DARWIN_BASE_SWITCHES}"
        LL_BUILD_DARWIN_DEBUG                       = f"{LL_BUILD_DARWIN_DEBUG_SWITCHES} {LL_BUILD_DARWIN_DEBUG_MACROS}"
        LL_BUILD_DARWIN_DEBUGOS                     = f"{LL_BUILD_DARWIN_DEBUG}"

        # Linux
        LL_BUILD_LINUX_BASE_MACROS                  = f"-DLL_LINUX=1 {LL_BUILD_POSIX_BASE_MACROS}"
        LL_BUILD_LINUX_BASE_SWITCHES                = f"-g {LL_BUILD_POSIX_BASE_SWITCHES}"
        LL_BUILD_LINUX_BASE                         = f"{LL_BUILD_LINUX_BASE_SWITCHES} {LL_BUILD_LINUX_BASE_MACROS}"

        LL_BUILD_LINUX_RELEASE_MACROS               = f"-DLL_RELEASE=1 -DLL_RELEASE_FOR_DOWNLOAD=1 -DNDEBUG {LL_BUILD_LINUX_BASE_MACROS}"
        LL_BUILD_LINUX_RELEASE_SWITCHES             = f"-O3 {LL_BUILD_LINUX_BASE_SWITCHES}"
        LL_BUILD_LINUX_RELEASE                      = f"{LL_BUILD_LINUX_RELEASE_SWITCHES} {LL_BUILD_LINUX_RELEASE_MACROS}"
        LL_BUILD_LINUX_RELEASEOS                    = f"{LL_BUILD_LINUX_RELEASE}"

        LL_BUILD_LINUX_RELWITHDEBINFO_MACROS        = f"-DLL_RELEASE=1 -DLL_RELEASE_WITH_DEBUG_INFO=1 -DNDEBUG {LL_BUILD_LINUX_BASE_MACROS}"
        LL_BUILD_LINUX_RELWITHDEBINFO_SWITCHES      = f"-O0 {LL_BUILD_LINUX_BASE_SWITCHES}"
        LL_BUILD_LINUX_RELWITHDEBINFO               = f"{LL_BUILD_LINUX_RELWITHDEBINFO_SWITCHES} {LL_BUILD_LINUX_RELWITHDEBINFO_MACROS}"
        LL_BUILD_LINUX_RELWITHDEBINFOOS             = f"{LL_BUILD_LINUX_RELWITHDEBINFO}"

        LL_BUILD_LINUX_DEBUG_MACROS                 = f"-D_DEBUG -DLL_DEBUG=1 {LL_BUILD_LINUX_BASE_MACROS}"
        LL_BUILD_LINUX_DEBUG_SWITCHES               = f"-O0 {LL_BUILD_LINUX_BASE_SWITCHES}"
        LL_BUILD_LINUX_DEBUG                        = f"{LL_BUILD_LINUX_DEBUG_SWITCHES} {LL_BUILD_LINUX_DEBUG_MACROS}"
        LL_BUILD_LINUX_DEBUGOS                      = f"{LL_BUILD_LINUX_DEBUG}"

        if self.settings.os == "Windows":
            build_options = (LL_BUILD_WINDOWS_DEBUG, LL_BUILD_WINDOWS_RELEASE, LL_BUILD_WINDOWS_RELWITHDEBINFO)
        elif self.settings.os == "Linux":
            build_options = (LL_BUILD_LINUX_DEBUG, LL_BUILD_LINUX_RELEASE, LL_BUILD_LINUX_RELWITHDEBINFO)
        elif self.settings.os == "Macos":
            build_options = (LL_BUILD_DARWIN_DEBUG, LL_BUILD_DARWIN_RELEASE, LL_BUILD_DARWIN_RELWITHDEBINFO)

        if self.settings.build_type == "Debug":
            options = build_options[0]
        elif self.settings.build_type == "Release":
            options = build_options[1]
        elif self.settings.build_type == "RelWithDebInfo":
            options = build_options[2]

        if self.settings.compiler == "gcc":
            options += " -Wno-error=nonnull"

        return options