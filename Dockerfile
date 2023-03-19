# this is a docker file for ailive
# it starts from python 3.10 or higher and installs all the dependencies
# it also installs the ailive package

FROM python:3.10

# copy ai live package
COPY . /ailive

# install ailive package
RUN pip install /ailive

# run ailive
WORKDIR /ailive/apps/funny_news_reactor

CMD ["python", "jerry_seinfeld_reactor.py"]
