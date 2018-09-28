macro(make_path varname)
   # accepts any number of path variables
   string(REPLACE ";" "${PATH_SEP}" ${varname} "${ARGN}")
endmacro()

macro(unmake_path varname)
   string(REPLACE "${PATH_SEP}" ";" ${varname} "${ARGN}")
endmacro()

macro(create_pyside_module
      module_name
      module_include_dir
      module_libraries
      module_deps
      module_typesystem_path
      module_sources
      module_static_sources)
    string(TOLOWER ${module_name} _module)
    string(REGEX REPLACE ^qt "" _module ${_module})
    if(${ARGC} GREATER 7)
        set (typesystem_name ${ARGV7})
    else()
        set (typesystem_name "")
    endif()
    if(${ARGC} GREATER 8)
        string(REPLACE ";" "\\;" dropped_entries "${${ARGV8}}")
    else()
        set (dropped_entries "")
    endif()

    if (NOT EXISTS ${typesystem_name})
        set(typesystem_path ${CMAKE_CURRENT_SOURCE_DIR}/typesystem_${_module}.xml)
    else()
        set(typesystem_path ${typesystem_name})
    endif()

    # check for class files that were commented away.
    if(DEFINED ${module_sources}_skipped_files)
        if(DEFINED PYTHON3_EXECUTABLE)
            set(_python_interpreter "${PYTHON3_EXECUTABLE}")
        else()
            set(_python_interpreter "${PYTHON_EXECUTABLE}")
        endif()
        if(NOT _python_interpreter)
            message(FATAL_ERROR "*** we need a python interpreter for postprocessing!")
        endif()
        set(_python_postprocessor "${_python_interpreter}" "${CMAKE_CURRENT_BINARY_DIR}/filter_init.py")
    else()
        set(_python_postprocessor "")
    endif()

    # Create typesystem XML dependencies list, so that whenever they change, shiboken is invoked
    # automatically.
    # First add the main file.
    set(total_type_system_files ${typesystem_path})

    get_filename_component(typesystem_root "${CMAKE_CURRENT_SOURCE_DIR}" DIRECTORY)

    set(deps ${module_name} ${${module_deps}})
    foreach(dep ${deps})
        set(glob_expression "${typesystem_root}/${dep}/*.xml")
        file(GLOB type_system_files ${glob_expression})
        set(total_type_system_files ${total_type_system_files} ${type_system_files})
    endforeach(dep)

    # Remove any possible duplicates.
    list(REMOVE_DUPLICATES total_type_system_files)

    # Contains include directories to pass to shiboken's preprocessor.
    set(shiboken_include_dirs ${pyside2_SOURCE_DIR}${PATH_SEP}${QT_INCLUDE_DIR})
    set(shiboken_framework_include_dirs_option "")
    if(CMAKE_HOST_APPLE)
        set(shiboken_framework_include_dirs "${QT_FRAMEWORK_INCLUDE_DIR}")
        make_path(shiboken_framework_include_dirs ${shiboken_framework_include_dirs})
        set(shiboken_framework_include_dirs_option "--framework-include-paths=${shiboken_framework_include_dirs}")
    endif()

    # Transform the path separators into something shiboken understands.
    make_path(shiboken_include_dirs ${shiboken_include_dirs})

    get_filename_component(pyside_binary_dir ${CMAKE_CURRENT_BINARY_DIR} DIRECTORY)

    add_custom_command(OUTPUT ${${module_sources}}
                        COMMAND "${SHIBOKEN_BINARY}" ${GENERATOR_EXTRA_FLAGS}
                        "${pyside2_BINARY_DIR}/${module_name}_global.h"
                        --include-paths=${shiboken_include_dirs}
                        ${shiboken_framework_include_dirs_option}
                        --typesystem-paths=${pyside_binary_dir}${PATH_SEP}${pyside2_SOURCE_DIR}${PATH_SEP}${${module_typesystem_path}}
                        --output-directory=${CMAKE_CURRENT_BINARY_DIR}
                        --license-file=${CMAKE_CURRENT_SOURCE_DIR}/../licensecomment.txt
                        ${typesystem_path}
                        --api-version=${SUPPORTED_QT_VERSION}
                        --drop-type-entries="${dropped_entries}"
                        COMMAND ${_python_postprocessor}
                        DEPENDS ${total_type_system_files}
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                        COMMENT "Running generator for ${module_name}...")

    include_directories(${module_name} ${${module_include_dir}} ${pyside2_SOURCE_DIR})
    add_library(${module_name} MODULE ${${module_sources}} ${${module_static_sources}})
    set_target_properties(${module_name} PROPERTIES
                          PREFIX ""
                          OUTPUT_NAME "${module_name}${PYTHON_EXTENSION_SUFFIX}"
                          LIBRARY_OUTPUT_DIRECTORY ${pyside2_BINARY_DIR})
    if(WIN32)
        set_target_properties(${module_name} PROPERTIES SUFFIX ".pyd")
        # Sanitize windows.h as pulled by gl.h to prevent clashes with QAbstract3dAxis::min(), etc.
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DNOMINMAX")
    endif()

    target_link_libraries(${module_name} ${${module_libraries}})
    if(${module_deps})
        add_dependencies(${module_name} ${${module_deps}})
    endif()

    # install
    install(TARGETS ${module_name} LIBRARY DESTINATION ${PYTHON_SITE_PACKAGES}/PySide2)
    string(TOLOWER ${module_name} lower_module_name)
    install(FILES ${CMAKE_CURRENT_BINARY_DIR}/PySide2/${module_name}/pyside2_${lower_module_name}_python.h
            DESTINATION include/PySide2${pyside2_SUFFIX}/${module_name}/)
    file(GLOB typesystem_files ${CMAKE_CURRENT_SOURCE_DIR}/typesystem_*.xml ${typesystem_path})

#   Copy typesystem files and remove module names from the <load-typesystem> element
#   so that it works in a flat directory:
#   <load-typesystem name="QtWidgets/typesystem_widgets.xml" ... ->
#   <load-typesystem name="typesystem_widgets.xml"
    foreach(typesystem_file ${typesystem_files})
        get_filename_component(typesystem_file_name "${typesystem_file}" NAME)
        file(READ "${typesystem_file}" typesystemXml)
        string(REGEX REPLACE "<load-typesystem name=\"[^/\"]+/" "<load-typesystem name=\"" typesystemXml "${typesystemXml}")
        set (typesystem_target_file "${CMAKE_CURRENT_BINARY_DIR}/PySide2/typesystems/${typesystem_file_name}")
        file(WRITE "${typesystem_target_file}" "${typesystemXml}")
        install(FILES "${typesystem_target_file}" DESTINATION share/PySide2${pyside2_SUFFIX}/typesystems)
    endforeach()
endmacro()

#macro(check_qt_class_with_namespace module namespace class optional_source_files dropped_entries [namespace] [module])
macro(check_qt_class module class optional_source_files dropped_entries)
    if (${ARGC} GREATER 4)
        set (namespace ${ARGV4})
        string(TOLOWER ${namespace} _namespace)
    else ()
        set (namespace "")
    endif ()
    if (${ARGC} GREATER 5)
        set (include_file ${ARGV5})
    else ()
        set (include_file ${class})
    endif ()
    string(TOLOWER ${class} _class)
    # Remove the "Qt" prefix.
    string(SUBSTRING ${module} 2 -1 _module_no_qt_prefix)
    if (_namespace)
        set(_cppfile ${CMAKE_CURRENT_BINARY_DIR}/PySide2/${module}/${_namespace}_${_class}_wrapper.cpp)
    else ()
        set(_cppfile ${CMAKE_CURRENT_BINARY_DIR}/PySide2/${module}/${_class}_wrapper.cpp)
    endif ()
    if (DEFINED PYSIDE_${class})
        if (PYSIDE_${class})
            list(APPEND ${optional_source_files} ${_cppfile})
        else()
            list(APPEND ${dropped_entries} PySide2.${module}.${class})
        endif()
    else()
        if (NOT ${namespace} STREQUAL "" )
            set (NAMESPACE_USE "using namespace ${namespace};")
        else ()
            set (NAMESPACE_USE "")
        endif ()
        set(SRC_FILE ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/test${class}.cxx)
        file(WRITE ${SRC_FILE}
             "#include <${include_file}>\n"
             "${NAMESPACE_USE}\n"
             "int main() { sizeof(${class}); }\n"
        )

        # Because Qt is built with -fPIC (by default), the compile tests also have to have that.
        get_property(ADDITIONAL_FLAGS TARGET Qt5::Core PROPERTY INTERFACE_COMPILE_OPTIONS)

        # Don't add version tagging, because for some reason linker fails with:
        # (.qtversion[qt_version_tag]+0x0): undefined reference to `qt_version_tag'
        # Force usage of the C++11 standard. CMAKE_CXX_STANDARD does not work with try_compile
        # but the issue has a fix in CMake 3.9. Thus we use a terrible workaround, we pass the C++
        # standard flag the way CheckCXXSourceCompiles.cmake does it.

        set(ADDITIONAL_FLAGS "${ADDITIONAL_FLAGS} -DQT_NO_VERSION_TAGGING ${CMAKE_CXX11_EXTENSION_COMPILE_OPTION}")

        try_compile(Q_WORKS ${CMAKE_BINARY_DIR}
                    ${SRC_FILE}
                    CMAKE_FLAGS
                        "-DINCLUDE_DIRECTORIES=${QT_INCLUDE_DIR};${Qt5${_module_no_qt_prefix}_INCLUDE_DIRS}"
                        "-DCOMPILE_DEFINITIONS:STRING=${ADDITIONAL_FLAGS}"
                    OUTPUT_VARIABLE OUTPUT)
        file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeCheckQtClassTest.log ${OUTPUT})

        set("PYSIDE_${class}" ${Q_WORKS} CACHE STRING "Has ${class} class been found?")
        if(Q_WORKS)
            message(STATUS "Checking for ${class} in ${module} -- found")
            list(APPEND ${optional_source_files} ${_cppfile})
        else()
            message(STATUS "Checking for ${class} in ${module} -- not found")
            list(APPEND ${dropped_entries} PySide2.${module}.${class})
        endif()
    endif()
endmacro()


# Only add subdirectory if the associated Qt module is found.
# As a side effect, this macro now also defines the variable ${name}_GEN_DIR
# and must be called for every subproject.
macro(HAS_QT_MODULE var name)
    if (NOT DISABLE_${name} AND ${var})
        # we keep the PySide name here because this is compiled into shiboken
        set(${name}_GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/${name}/PySide2/${name}
            CACHE INTERNAL "dir with generated source" FORCE)
        add_subdirectory(${name})
    else()
        # Used on documentation to skip modules
        set("if_${name}" "<!--" PARENT_SCOPE)
        set("end_${name}" "-->" PARENT_SCOPE)
    endif()
endmacro()

