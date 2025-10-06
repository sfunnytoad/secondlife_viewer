# -*- cmake -*-
include_guard()
add_library( ll::xxhash INTERFACE IMPORTED )

if (USE_CONAN)

  find_package(xxHash REQUIRED)
  target_link_libraries(ll::xxhash INTERFACE xxHash::xxhash)

else (USE_CONAN)

include(Prebuilt)
use_prebuilt_binary(xxhash)

endif (USE_CONAN)
