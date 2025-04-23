# Definir flags de compilação condicionalmente (Release ou Debug)
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Diretórios do projeto
set(PROJECT_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src")
set(PROJECT_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/include")

# Usar GLOB para obter automaticamente todos os arquivos .hpp e .cpp
file(GLOB_RECURSE HEADER_FILES "${PROJECT_INCLUDE_DIR}/*.hpp")
file(GLOB_RECURSE SOURCE_FILES "${PROJECT_SOURCE_DIR}/*.cpp")

# Criação da biblioteca compartilhada com o nome ctreelearn_lib
add_library(ctreelearn_lib SHARED ${HEADER_FILES} ${SOURCE_FILES})

# Diretórios de inclusão
target_include_directories(ctreelearn_lib PRIVATE ${PROJECT_INCLUDE_DIR})

# Agrupamento para IDEs
source_group(TREE ${PROJECT_INCLUDE_DIR} PREFIX "Headers" FILES ${HEADER_FILES})
source_group(TREE ${PROJECT_SOURCE_DIR} PREFIX "Sources" FILES ${SOURCE_FILES})

# Instalação da biblioteca
install(TARGETS ctreelearn_lib DESTINATION lib)

# Instalação de headers
install(DIRECTORY ${PROJECT_INCLUDE_DIR}/ DESTINATION include/ctreelearn)

