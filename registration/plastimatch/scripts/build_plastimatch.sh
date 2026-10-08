# All or portions of this licensed product (such portions are the "Software")
# have been obtained under license from MGH and are subject to the terms and
# conditions of the Plastimatch Software License.
# See LICENSE file for the full Plastimatch Software License text.

# Copyright (c) 2026 MetaX Integrated Circuits (Shanghai) Co., Ltd. All rights reserved.

#!/usr/bin/env bash
# Build and install Plastimatch from source.
set -euo pipefail

SOURCE_DIR="${PLASTIMATCH_SOURCE_DIR:-$PWD/plastimatch-src}"
BUILD_DIR="${PLASTIMATCH_BUILD_DIR:-$PWD/plastimatch-build}"
INSTALL_PREFIX="${PLASTIMATCH_INSTALL_PREFIX:-$PWD/plastimatch-install}"
PLASTIMATCH_REF="${PLASTIMATCH_REF:-69e57cf}"
JOBS="${PLASTIMATCH_BUILD_JOBS:-$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf '2')}"

if [[ ! -d "$SOURCE_DIR/.git" ]]; then
    git clone https://gitlab.com/plastimatch/plastimatch.git "$SOURCE_DIR"
fi
if ! git -C "$SOURCE_DIR" rev-parse --verify --quiet "$PLASTIMATCH_REF^{commit}" >/dev/null; then
    git -C "$SOURCE_DIR" fetch --tags --depth 1 origin
fi
git -C "$SOURCE_DIR" checkout --detach "$PLASTIMATCH_REF"

# Plastimatch's optional SIFT command depends on ITK review headers that are
# not shipped by newer distribution ITK packages.  The tutorial does not use
# SIFT, so keep the source build reproducible by excluding that optional
# command and its utility translation unit.  The upstream checkout itself is
# left intact; this small, explicit build-tree adaptation is re-applied on
# every build.
sed -i '/^[[:space:]]*sift\.cxx[[:space:]]*$/d' "$SOURCE_DIR/src/util/CMakeLists.txt"
sed -i '/^[[:space:]]*pcmd_sift\.cxx[[:space:]]*$/d' "$SOURCE_DIR/src/cli/CMakeLists.txt"
sed -i '/^[[:space:]]*#include "pcmd_sift\.h"[[:space:]]*$/d' "$SOURCE_DIR/src/cli/plastimatch_main.cxx"
sed -i '/^[[:space:]]*"  sift[[:space:]]*"[[:space:]]*$/d' "$SOURCE_DIR/src/cli/plastimatch_main.cxx"
sed -i '/^[[:space:]]*else if (!strcmp (command, "sift")) {/{N;N;d;}' "$SOURCE_DIR/src/cli/plastimatch_main.cxx"

command -v cmake >/dev/null || { echo "cmake is required" >&2; exit 2; }
command -v git >/dev/null || { echo "git is required" >&2; exit 2; }

# The upstream 1.10 build uses CMake's FindCUDA module.  The approved CUDA
# compatibility compiler can be selected with CUDA_NVCC_EXECUTABLE.
CUDA_ARGS=()
if [[ "${PLASTIMATCH_ENABLE_CUDA:-ON}" == "ON" ]]; then
    CUDA_ARGS+=("-DPLM_CONFIG_ENABLE_CUDA=ON")
    if [[ -n "${CUDA_TOOLKIT_ROOT_DIR:-}" ]]; then
        CUDA_ARGS+=("-DCUDA_TOOLKIT_ROOT_DIR=${CUDA_TOOLKIT_ROOT_DIR}")
    fi
    if [[ -n "${CUDA_NVCC_EXECUTABLE:-}" ]]; then
        CUDA_ARGS+=("-DCUDA_NVCC_EXECUTABLE=${CUDA_NVCC_EXECUTABLE}")
    fi
else
    CUDA_ARGS+=("-DPLM_CONFIG_ENABLE_CUDA=OFF")
fi

DEPENDENCY_ARGS=()
if [[ -n "${ITK_DIR:-}" ]]; then
    DEPENDENCY_ARGS+=("-DITK_DIR=${ITK_DIR}")
fi
if [[ -n "${DCMTK_DIR:-}" ]]; then
    DEPENDENCY_ARGS+=("-DDCMTK_DIR=${DCMTK_DIR}")
fi

# YES requires dependencies supplied by the host/container and avoids an
# implicit download of the old upstream ExternalProject archives.
cmake -S "$SOURCE_DIR" -B "$BUILD_DIR" -G "${CMAKE_GENERATOR:-Ninja}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX" \
    -DPLM_CONFIG_ENABLE_QT=OFF \
    -DPLM_CONFIG_ENABLE_OPENCL=OFF \
    -DPLM_CONFIG_ENABLE_MATLAB=OFF \
    -DPLM_CONFIG_ENABLE_CSHARP=OFF \
    -DPLM_CONFIG_ENABLE_PYTHON=OFF \
    -DPLM_CONFIG_ENABLE_PLASTIMATCH=ON \
    -DPLM_BUILD_TESTING=OFF \
    -DPLM_CONFIG_ENABLE_OPENMP=ON \
    -DPLM_CONFIG_ENABLE_DCMTK="${PLM_CONFIG_ENABLE_DCMTK:-ON}" \
    -DPLM_SYSTEM_ITK="${PLM_SYSTEM_ITK:-YES}" \
    -DPLM_SYSTEM_DCMTK="${PLM_SYSTEM_DCMTK:-YES}" \
    "${DEPENDENCY_ARGS[@]}" \
    "${CUDA_ARGS[@]}"

cmake --build "$BUILD_DIR" --parallel "$JOBS"
cmake --install "$BUILD_DIR"

BIN="$INSTALL_PREFIX/bin/plastimatch"
[[ -x "$BIN" ]] || { echo "install did not create $BIN" >&2; exit 1; }
# Plastimatch prints the command synopsis for --help but returns status 1;
# --version is the successful, side-effect-free installation check.
VERSION="$("$BIN" --version)"
printf '%s\n' "$VERSION"
printf 'Installed Plastimatch at %s\n' "$BIN"
