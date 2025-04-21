# Create a shared library from all .cc files in this directory
file(GLOB DATETIME_SRC CONFIGURE_DEPENDS "*.cc")

add_library(datetime SHARED ${DATETIME_SRC})

# Use C++17, enable warnings and optimizations like in your Makefile
target_compile_features(datetime PRIVATE cxx_std_17)
target_compile_options(datetime PRIVATE -O3 -g -Wextra -fPIC)

# Link math lib (like LDFLAGS = -lm)
target_link_libraries(datetime PRIVATE m)

# Public include path (assumes headers are in ../include)
target_include_directories(datetime PUBLIC ${CMAKE_SOURCE_DIR}/include)

# Output library to lib/
set_target_properties(datetime PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib
)

install(TARGETS datetime
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin        # For Windows .dll
    ARCHIVE DESTINATION lib        # For static libs
)

install(DIRECTORY ${CMAKE_SOURCE_DIR}/include/ DESTINATION include)