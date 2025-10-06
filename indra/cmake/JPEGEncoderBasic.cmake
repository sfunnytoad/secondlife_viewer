# -*- cmake -*-
if (USE_CONAN)
# TODO
else (USE_CONAN)

use_prebuilt_binary(jpegencoderbasic)

# Main JS file
configure_file("${AUTOBUILD_INSTALL_DIR}/js/jpeg_encoder_basic.js" "${CMAKE_SOURCE_DIR}/newview/skins/default/html/common/equirectangular/js/jpeg_encoder_basic.js" COPYONLY)

endif (USE_CONAN)
