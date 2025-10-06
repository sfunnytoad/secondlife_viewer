# -*- cmake -*-

include(Prebuilt)

add_library(ll::sse2neon INTERFACE IMPORTED)

if (DARWIN)
    if (USE_CONAN)
        find_package(sse2neon REQUIRED)
        target_link_libraries(ll::sse2neon INTERFACE sse2neon::sse2neon)
    else (USE_CONAN)
        use_system_binary(sse2neon)
        use_prebuilt_binary(sse2neon)

        target_include_directories( ll::sse2neon SYSTEM INTERFACE ${LIBS_PREBUILT_DIR}/include/sse2neon)
    endif (USE_CONAN)
endif()
