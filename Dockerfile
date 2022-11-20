FROM python:3.9

ADD * .
ADD main.py .
COPY requirements.txt requirements.txt
RUN pip install -i https://pypi.douban.com/simple --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]