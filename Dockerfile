FROM clipper/py-rpc:develop

RUN apt-get update --fix-missing \ 
    && apt-get install -y build-essential \
    && pip install fasttext

COPY fasttext-docker-test.py /container/

CMD ["python", "/container/fasttext-docker-test.py"]
