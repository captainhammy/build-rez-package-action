cmake_minimum_required(VERSION 3.6)

include(RezBuild)

file(GLOB_RECURSE py_files "src/*.py")

rez_install_files(
    FILES ${py_files}
    RELATIVE src/python
    DESTINATION python
)
