FROM python:3.7.3-stretch

COPY *.py requirements.txt model.pickle /nb_spam/
ADD static stopwords /nb_spam/
RUN cd /nb_spam && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

EXPOSE 8080

WORKDIR /nb_spam
CMD gunicorn -b 0.0.0.0:8080 -k gevent -w 2 web:app
