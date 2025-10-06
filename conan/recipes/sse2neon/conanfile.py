from conan import ConanFile
from conan.tools.files import get, copy
import os

class Sse2NeonConan(ConanFile):
    name = "sse2neon"
    version = "1.8.0"  # or current tag
    license = "MIT"
    url = "https://github.com/DLTcollab/sse2neon"
    description = "SSE-to-NEON header shim"
    package_type = "header-library"   # header-only
    no_copy_source = True

    def source(self):
        get(self,
            url=f"https://github.com/DLTcollab/sse2neon/archive/refs/tags/v{self.version}.tar.gz",
            strip_root=True)

    def package(self):
        copy(self, "sse2neon.h", src=self.source_folder,
             dst=os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "sse2neon")
        self.cpp_info.set_property("cmake_target_name", "sse2neon::sse2neon")
        self.cpp_info.includedirs = ["include"]
