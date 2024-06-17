cmake_minimum_required(VERSION 3.5)
project(quantif_experiments)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(performance_test REQUIRED)
find_package(performance_test_factory REQUIRED)

add_executable(simple_arch src/quantif_simple_arch.cpp)
ament_target_dependencies(simple_arch rclcpp performance_test performance_test_factory)

install(TARGETS
  simple_arch
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY test_archs
  DESTINATION share/${PROJECT_NAME}
)


##
## build the unit tests
##
if(BUILD_TESTING)
  # Linters
  find_package(ament_cmake_cppcheck REQUIRED)
  find_package(ament_cmake_cpplint REQUIRED)
  find_package(ament_cmake_lint_cmake REQUIRED)
  find_package(ament_cmake_uncrustify REQUIRED)
  find_package(ament_cmake_xmllint REQUIRED)

  ament_cppcheck(
    LANGUAGE C++
  )
  ament_cpplint()
  ament_lint_cmake()
  ament_uncrustify(
    LANGUAGE C++
  )
  ament_xmllint()
endif()

ament_package()
