# -*- cmake -*-
if (USE_CONAN)
# TODO
else (USE_CONAN)

include(Prebuilt)

use_prebuilt_binary(vulkan_gltf)

endif (USE_CONAN)
