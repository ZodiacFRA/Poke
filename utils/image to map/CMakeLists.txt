cmake_minimum_required(VERSION 3.14)
set(CMAKE_CXX_STANDARD 17)

project( ImageToMap )

find_package( OpenCV REQUIRED )

add_executable( ImageToMap 
    Main_copy.cpp
)
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries( ImageToMap ${OpenCV_LIBS} )