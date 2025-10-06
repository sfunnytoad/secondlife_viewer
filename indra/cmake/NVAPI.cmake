# -*- cmake -*-
if (USE_CONAN)
# TODO
else (USE_CONAN)

include(Prebuilt)

set(NVAPI ON CACHE BOOL "Use NVAPI.")

if (NVAPI)
  if (WINDOWS)
    add_library( ll::nvapi INTERFACE IMPORTED )
    target_link_libraries( ll::nvapi INTERFACE nvapi)
    use_prebuilt_binary(nvapi)
  endif (WINDOWS)
endif (NVAPI)

endif (USE_CONAN)
