FROM debian:9 as builder
ENV VERSION=19.16
WORKDIR /usr/src
# Install needed packages to build.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    bzip2 \
    curl \
    ca-certificates \
    checkinstall \
    python3-minimal \
    python3-setuptools \
    python3-dev \
    libopenblas-dev

# Install Neede Python Packages
RUN easy_install3 pip wheel 
    
# Download and Unpack dlib.
RUN curl -L --output dlib-${VERSION}.tar.bz2 http://dlib.net/files/dlib-${VERSION}.tar.bz2 && \
    tar xvvf dlib-${VERSION}.tar.bz2 && \
    mkdir -p dlib-${VERSION}/build

# Build C++ Dlib.
WORKDIR /usr/src/dlib-${VERSION}/build
RUN cmake .. -DUSE_AVX_INSTRUCTIONS=ON && \
    cmake --build . --config Release && \
    checkinstall -D --install=no -y --pkgname=dlib --pkgversion=${VERSION}

# Build Python Wheel
WORKDIR /usr/src/dlib-${VERSION}/
RUN python3 setup.py bdist_wheel --no DLIB_USE_CUDA --yes USE_AVX_INSTRUCTIONS

FROM debian:9
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 VERSION=19.16
WORKDIR /usr/src
COPY --from=builder /usr/src/dlib-19.16/build/*.deb .
COPY --from=builder /usr/src/dlib-19.16/dist/*.whl .

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-minimal \
    python3-setuptools \
    python3-dev \
    libopenblas-base \
    ca-certificates \
    chrpath

COPY requirements.txt .
RUN easy_install3 pip wheel && \
    dpkg -i *.deb && \
    pip install *.whl

RUN pip install --no-cache-dir -r requirements.txt && \
    ln -s /usr/bin/python3 /usr/bin/python

ADD src /usr/src/code/
WORKDIR /usr/src/code

CMD ["gunicorn","app_falcon:app","-c","gunicorn.py"]
