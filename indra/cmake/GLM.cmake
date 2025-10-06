# -*- cmake -*-
include(Prebuilt)

add_library( ll::glm INTERFACE IMPORTED )

if (USE_CONAN)

find_package(glm REQUIRED)
target_link_libraries(ll::glm INTERFACE glm::glm)

else (USE_CONAN)

use_system_binary( glm )
use_prebuilt_binary(glm)

endif (USE_CONAN)
