# -*- cmake -*-
if (USE_CONAN)
# TODO
else (USE_CONAN)

include(Prebuilt)

use_prebuilt_binary(tinyexr)

set(TINYEXR_INCLUDE_DIR ${LIBS_PREBUILT_DIR}/include/tinyexr)

endif (USE_CONAN)
