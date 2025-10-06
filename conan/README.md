# Build Instructions

### Prerequisites
- Ensure **Conan 2.x** is installed.
- Confirm your Conan profile is configured for **C++20**:
  ```bash
  conan profile show default
  ```

  Update it if necessary:

  ```bash
  conan profile update settings.compiler.cppstd=20 default
  ```

### Build Steps
From the indra/ directory:

1. Install dependencies via Conan:
   ```bash
   conan install . --build=missing
   ```

2. Configure the CMake build (using the Conan-generated preset):
   ```bash
   cmake --preset conan-release
   ```

3. Build the project:
   ```bash
   cmake --build --preset conan-release
   ```

# Known Issues / To-Do
- OpenAL package failure

  The Conan OpenAL package currently fails to download due to an expired SSL certificate at openal-soft.org

  __Temporary workaround:__ edit the package recipe at `~/.conan2/p/openaf47db0a4b219/e/conanfile.py` and modify the `source()` method as follows:

  ```python
  def source(self):
    get(self, **self.conan_data["sources"][self.version],
        strip_root=True, verify=False)
  ```

- Upgrade APR to 1.7.5
- Replace zlib with zlib-ng
