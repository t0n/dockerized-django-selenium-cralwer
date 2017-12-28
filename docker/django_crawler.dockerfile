FROM python:3.5.2-slim

ARG DEBIAN_FRONTEND=noninteractive

# Update all and install additional tools
RUN \
  apt-get update && \
  apt-get install -y \
    gcc \
    apt-utils \
    apt-transport-https \
    wget \
    ca-certificates \
    bzip2 \
    vim \
    libfontconfig \
    python3-pip

# Install Node 6.*
RUN \
  echo "deb https://deb.nodesource.com/node_6.x jessie main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  apt-get update && \
  apt-get install -yqq nodejs && \
  rm -rf /var/lib/apt/lists/*

# Install PhantomJS
RUN \
    npm install -g phantomjs-prebuilt

RUN pip3 install --upgrade pip

WORKDIR /var/django-crawler
ADD ./requirements_base.txt /var/django-crawler
RUN pip3 install -b build/ --ignore-installed --no-cache-dir --upgrade -r /var/django-crawler/requirements_base.txt
RUN rm -rf build/
RUN mkdir logs

ADD . /var/django-crawler

CMD ["python", "manage.py", "runserver"]
