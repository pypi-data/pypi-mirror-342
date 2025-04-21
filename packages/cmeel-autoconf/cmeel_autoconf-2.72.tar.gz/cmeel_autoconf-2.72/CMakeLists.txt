cmake_minimum_required(VERSION 3.30)

set(NAME autoconf)
set(VERSION 2.72)
set(EXT tar.xz)
set(SHA256 ba885c1319578d6c94d46e9b0dceb4014caafe2490e437a0dbca3f270a223f5a)

project("cmeel-${NAME}" VERSION "${VERSION}")

include(ExternalProject)
ExternalProject_Add(
  ${NAME}
  URL "https://ftpmirror.gnu.org/gnu/${NAME}/${NAME}-${VERSION}.${EXT}"
  URL_HASH "SHA256=${SHA256}"
  DOWNLOAD_EXTRACT_TIMESTAMP ON
  BUILD_IN_SOURCE ON
  CONFIGURE_COMMAND "./configure" "--prefix=${CMAKE_INSTALL_PREFIX}"
  BUILD_COMMAND "make"
  # TEST_COMMAND "make" "check"
  INSTALL_COMMAND "make" "install")

# dummy file for install target
install(FILES "README.md" DESTINATION "share/cmeel-${NAME}/")
