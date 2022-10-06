FROM nvidia/cuda:11.0-devel-ubuntu20.04

ENV TERM xterm-256color
ENV DEBIAN_FRONTEND=noninteractive

RUN rm /etc/apt/sources.list.d/cuda.list && \
    apt-key del 7fa2af80 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5 && \
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/7fa2af80.pub

RUN apt update && apt install -y --no-install-recommends --fix-missing \
    git \
    cmake \
    wget \
    curl \
    unzip \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libboost-test-dev \
    libeigen3-dev \
    libsuitesparse-dev \
    libfreeimage-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libatlas-base-dev \
    libsuitesparse-dev \
    libmetis-dev \
    libhdf5-dev \
    python-dev \
    python-setuptools \
    python3-pip \
    python3-dev \
    && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && rm -rf /tmp/* /var/tmp/*

# Eigen
WORKDIR /opt
RUN git clone --depth 1 --branch 3.4.0 https://gitlab.com/libeigen/eigen.git
RUN cd eigen && mkdir build && cd build && cmake .. && make install

# Ceres Solver
WORKDIR /opt
RUN git clone https://ceres-solver.googlesource.com/ceres-solver
WORKDIR /opt/ceres-solver
RUN git checkout 2.1.0rc2
RUN mkdir build
WORKDIR /opt/ceres-solver/build
RUN cmake .. -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF
RUN make -j
RUN make install

# Colmap
WORKDIR /opt
RUN git clone https://github.com/colmap/colmap.git
WORKDIR /opt/colmap
RUN git checkout dev
RUN mkdir build
WORKDIR /opt/colmap/build
RUN cmake ..
RUN make -j
RUN make install

# PixSfM
WORKDIR /
RUN git clone https://github.com/cvg/pixel-perfect-sfm --recursive
WORKDIR /pixel-perfect-sfm
RUN pip3 install -r requirements.txt
RUN git clone --recursive https://github.com/cvg/Hierarchical-Localization/
WORKDIR /pixel-perfect-sfm/Hierarchical-Localization
RUN pip3 install -e .
RUN git pull
RUN pip3 install -e . 
WORKDIR /pixel-perfect-sfm
RUN pip3 install -e .	


# Extra libraries you really need here
RUN pip3 install jupyter
RUN pip3 install -U pip>=20.3
RUN python3 -m pip install --user open3d
RUN pip3 install --upgrade git+https://github.com/colmap/pycolmap


WORKDIR /