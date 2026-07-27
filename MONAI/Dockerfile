##The 3-Clause BSD License
#
## Copyright (c) 2026 MetaX Integrated Circuits (Shanghai) Co., Ltd. All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

FROM cr.metax-tech.com/public-library/maca-pytorch:3.8.0.11-torch2.6-py310-ubuntu24.04-amd64 AS base
ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai
RUN apt update && apt install tzdata -y && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && rm -rf /var/lib/apt/lists/* && echo $TZ > /etc/timezone
RUN apt update && apt install -y libssl-dev build-essential openssh-server vim gdb git wget curl ca-certificates unzip && \
    apt clean && rm -rf  /var/lib/apt/lists/* /tmp/* /var/tmp/*
ENV MACA_PATH=/opt/maca
ENV CUCC_PATH=/opt/maca/tools/cu-bridge
ENV PATH=$PATH:${CUCC_PATH}/tools:${CUCC_PATH}/bin
ENV CUCC_CMAKE_ENTRY=2        
ENV CUDA_PATH=${CUCC_PATH} 
ENV PYTORCH_DEFAULT_NDHWC=1
WORKDIR /opt
RUN git clone https://github.com/Project-MONAI/MONAI.git MONAI && cd MONAI && git checkout 1.5.2
COPY monai_muxi.patch monai_muxi.patch
RUN cd MONAI && git apply monai_muxi.patch
COPY maca-onnxruntime-1.12.0-py310-3.8.0.10-linux-x86_64.tar.xz maca-onnxruntime-1.12.0-py310-3.8.0.10-linux-x86_64.tar.xz
RUN tar -xJf maca-onnxruntime-1.12.0-py310-3.8.0.10-linux-x86_64.tar.xz && pip install maca-onnxruntime-3.8.0.10/wheel/onnxruntime_gpu*.whl
RUN cp MONAI/requirements.txt MONAI/requirements-min.txt MONAI/requirements-dev.txt /tmp/
RUN awk '!/torch/' /tmp/requirements.txt > /tmp/tmp && mv /tmp/tmp /tmp/requirements.txt 
RUN awk '!/torchvision/' /tmp/requirements-dev.txt > /tmp/tmp && awk '!/MetricsReloaded/' /tmp/tmp > /tmp/requirements-dev.txt && awk '!/cucim/' /tmp/requirements-dev.txt > /tmp/tmp  && awk '!/onnxruntime/' /tmp/tmp > /tmp/requirements-dev.txt
RUN python -m pip install --upgrade --no-cache-dir pip 
RUN python -m pip install --no-cache-dir -r /tmp/requirements-dev.txt
RUN git clone https://github.com/Project-MONAI/MetricsReloaded && cd MetricsReloaded && git checkout monai-support && pip install --no-build-isolation .  
ENV TORCH_CUDA_ARCH_LIST=8.0+PTX BUILD_MONAI=1 FORCE_CUDA=1
RUN cd MONAI  && BUILD_MONAI=1 FORCE_CUDA=1 python setup.py install && rm -rf build __pycache__

# Copyright (c) 2026 MetaX Integrated Circuits (Shanghai) Co., Ltd. All rights reserved.