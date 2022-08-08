FROM ubuntu

RUN apt -y update

RUN apt install -y git
RUN apt install -y python3
RUN apt install -y python3.10-venv

ADD . projects

RUN git clone https://github.com/matheuscogo/sistematcc.flask.git 

RUN python3 -m venv .venv
