# Second Life Viewer - Conan Proof of Concept

This repository contains proof-of-concept work for building the `indra/llcommon` library using Conan package manager with modern C++20 and CMake.

## Prerequisites

- **Conan 2.x** must be installed on your system
- Your Conan profile must be configured for **C++20**

### Verify Conan Configuration

Check your current Conan profile:
```bash
conan profile show default
```

If C++20 is not configured, update your profile:
```bash
conan profile update settings.compiler.cppstd=20 default
```

## Platform Support

| Platform | Status |
|----------|--------|
| 🪟 Windows | ✅ Supported |
| 🐧 Linux | ✅ Supported |
| 🍎 macOS | 🚧 Work in Progress |

## Build Instructions

Navigate to the `indra/` directory and follow these steps:

### 1. Install Dependencies
```bash
conan install . --build=missing
```

### 2. Configure CMake Build
```bash
cmake --preset conan-release
```

### 3. Build the Project
```bash
cmake --build --preset conan-release
```

## Known Issues

### OpenAL Package Failure
The Conan OpenAL package currently fails to download due to an expired SSL certificate at openal-soft.org.

**Temporary Workaround:**
Edit the package recipe at `~/.conan2/p/openaf47db0a4b219/e/conanfile.py` and modify the `source()` method:

```python
def source(self):
    get(self, **self.conan_data["sources"][self.version],
        strip_root=True, verify=False)
```

## Roadmap

- [ ] Upgrade APR to version 1.7.5
- [ ] Replace zlib with zlib-ng for improved performance
- [ ] Create sse2neon Conan package for macOS ARM64 support
