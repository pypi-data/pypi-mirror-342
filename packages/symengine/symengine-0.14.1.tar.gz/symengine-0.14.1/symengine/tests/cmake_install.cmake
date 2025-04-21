# Install script for directory: /home/isuru/projects/symengine.py/symengine/tests

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/home/isuru/miniforge3/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/__init__.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_arit.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_cse.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_dict_basic.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_eval.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_expr.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_functions.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_lambdify.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_logic.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_matrices.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_ntheory.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_number.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_pickling.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_printing.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_sage.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_series_expansion.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_sets.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_solve.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_subs.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_symbol.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_sympify.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_sympy_compat.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_sympy_conv.py;/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests/test_var.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/home/isuru/miniforge3/lib/python3.13/site-packages/symengine/tests" TYPE FILE FILES
    "/home/isuru/projects/symengine.py/symengine/tests/__init__.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_arit.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_cse.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_dict_basic.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_eval.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_expr.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_functions.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_lambdify.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_logic.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_matrices.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_ntheory.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_number.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_pickling.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_printing.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_sage.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_series_expansion.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_sets.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_solve.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_subs.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_symbol.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_sympify.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_sympy_compat.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_sympy_conv.py"
    "/home/isuru/projects/symengine.py/symengine/tests/test_var.py"
    )
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/home/isuru/projects/symengine.py/symengine/tests/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
