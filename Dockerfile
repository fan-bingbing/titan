FROM python:3
ENV PYTHONUNBUFFERED 1

# add build user
RUN useradd -ms /bin/bash build

# switch to build user
USER build
ENV HOME /home/build
WORKDIR /home/build/


# download conda
RUN ["/bin/bash", "-c", "wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $HOME/miniconda.sh"]
RUN chmod 0755 $HOME/miniconda.sh
RUN ["/bin/bash", "-c", "$HOME/miniconda.sh -b -p $HOME/conda"]
ENV PATH="$HOME/conda/bin:$PATH"
RUN rm $HOME/miniconda.sh

# update conda
RUN conda update --all

# prepare environment

RUN pip install Django==2.2.4
RUN pip install pyvisa==1.10.0
RUN pip install sounddevice
RUN pip install pyserial
RUN pip install libportaudio2
RUN pip install numpy

RUN conda list


RUN conda info --envs


COPY . /home/build/
CMD ["python", "./manage.py", "runserver"]
