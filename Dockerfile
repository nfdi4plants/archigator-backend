FROM python:3.9

#COPY ./push /
COPY . /
COPY requirements.txt /


RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY app/ /archigator/app
COPY init.sh /archigator
COPY main.py /archigator
COPY requirements.txt /archigator

WORKDIR /archigator

COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh

EXPOSE 8000 1111

ENTRYPOINT ["init.sh"]

