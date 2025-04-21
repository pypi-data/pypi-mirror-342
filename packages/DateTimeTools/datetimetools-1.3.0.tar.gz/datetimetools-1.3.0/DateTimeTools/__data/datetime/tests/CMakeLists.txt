find_package(PkgConfig REQUIRED)
pkg_check_modules(CHECK REQUIRED check)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/heads/main.zip
)
FetchContent_MakeAvailable(googletest)

link_directories(${CMAKE_SOURCE_DIR}/lib)

add_executable(test_datetime test_datetime.cc)

# Link to Google Test + your datetime shared lib
target_link_libraries(test_datetime
    gtest_main
    datetime
    m
)

# Include headers
target_include_directories(test_datetime PRIVATE ${CMAKE_SOURCE_DIR}/include)

# So test executable can find the shared lib at runtime
set_target_properties(test_datetime PROPERTIES
    BUILD_RPATH ${CMAKE_SOURCE_DIR}/lib
    INSTALL_RPATH ${CMAKE_SOURCE_DIR}/lib
)

include(GoogleTest)
gtest_discover_tests(test_datetime)

add_executable(test_c test_c.c)

# Add include paths and link libraries using pkg-config
target_include_directories(test_c PRIVATE
    ${CHECK_INCLUDE_DIRS}
    ${CMAKE_SOURCE_DIR}/include
)

target_link_libraries(test_c
    ${CHECK_LIBRARIES}
    datetime
    m
)

set_target_properties(test_c PROPERTIES
    BUILD_RPATH ${CMAKE_SOURCE_DIR}/lib
    INSTALL_RPATH ${CMAKE_SOURCE_DIR}/lib
)
