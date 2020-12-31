#FROM tensorflow/tensorflow:latest-gpu-py3
#FROM nvidia/cuda:10.0-base
#FROM nvidia/cuda:10.0-runtime
#FROM nvidia/cuda:10.0-cudnn7-runtime
FROM nvidia/cuda:10.0-devel
FROM nvidia/cuda:10.0-cudnn7-devel
#FROM pytorch/pytorch:latest
RUN apt-get update ; apt-get install vim git wget unzip build-essential libboost-all-dev autotools-dev automake python-pip python3-pip -y
#RUN pip install --upgrade numpy scikit-image tqdm dival Cython matplotlib tensorflow==1.14 keras==2.2.4
RUN pip3 install --upgrade numpy matplotlib h5py tqdm Cython scikit-image scipy scikit-build

WORKDIR /
ENV C_INCLUDE_PATH=/usr/local/cuda/include/
ENV LIBRARY_PATH=/usr/local/cuda/lib64/
ENV CPATH=/usr/local/cuda/include/
#RUN ln -s /usr/local/cuda/lib64/libcudart.so /usr/local/lib/ && \
#    ln -s /usr/local/cuda/lib64/libcufft.so.10.0 /usr/local/lib/libcufft.so && \
RUN wget https://github.com/astra-toolbox/astra-toolbox/archive/master.zip && \
    unzip master.zip && \
    cd astra-toolbox-master/build/linux/ && \
    ./autogen.sh && \
    ./configure --with-cuda=/usr/local/cuda --with-python=/usr/bin/python3 --with-install-type=module && \
    make && \
    make install && \
    cd ../../.. && \
    pwd && \
    rm master.zip
ENV LD_LIBRARY_PATH="/usr/local/astra/lib:${LD_LIBRARY_PATH}"
ENV PYTHONPATH="/usr/local/astra/python:${PYTHONPATH}"

RUN pip3 install --upgrade cmake pathlib2
RUN wget https://github.com/dmpelt/foam_ct_phantom/archive/master.zip && \
    unzip master.zip && \
    cd foam_ct_phantom-master && \
    python3 setup.py install && \
    cd .. && \
    rm master.zip

