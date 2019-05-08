import pandas
import multiprocessing
import os
import click
from model import *
from process import *


class Worker(multiprocessing.Process):
    def __init__(self, queue, stop_words, process_num, mysql_config):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.stop_words = stop_words
        self.process_num = process_num
        self.mysql_config = mysql_config
        self.db = init_database(mysql_config=mysql_config)
        self.Mail = init_model(self.db)

    def run(self) -> None:
        print("starting worker process", self.process_num)
        while True:
            real_path, spam, path = self.queue.get()
            if real_path is None and spam is None and path is None:
                break
            try:
                mail, exists = get_or_create_mail(real_path, spam, path, self.stop_words, self.Mail)
                print(self.process_num, path, exists, spam, mail.content[:5], len(mail.words))
                if not exists:
                    mail.save()
            except Exception as e:
                print(real_path, e)


class Producer(multiprocessing.Process):
    def __init__(self, queue, index, worker_num):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.index = index
        self.worker_num = worker_num

    def run(self) -> None:
        print("starting producer process", len(self.index))
        for i, row in self.index.iterrows():
            self.queue.put((row.real_path, row.spam, row.path))
        for i in range(self.worker_num):
            self.queue.put((None, None, None))


def get_index(trec06c_path):
    index = pandas.read_csv(os.path.join(trec06c_path, 'full/index'), sep=' ', names=['spam', 'path'])
    index['real_path'] = index.path.apply(lambda x: os.path.join(trec06c_path, x[1:]))
    index.spam = index.spam.apply(lambda x: True if x == 'spam' else False)
    return index


def save_worker(queue):
    print("starting save process")
    while True:
        mail = queue.get()
        mail.save()


@click.command()
@click.option('-t', 'trec06c_path', help='trec06 数据集根路径')
@click.option('-s', 'stopwords_glob', help='禁用词表 GLOB')
@click.option('-d', 'mysql_db_name', default='nb_spam', help='MySQL 数据库名')
@click.option('-u', 'mysql_user', default='root', help='MySQL 用户')
@click.option('-p', 'mysql_password', default='', help='MySQL 密码')
@click.option('-h', 'mysql_host', default='localhost', help='MySQL Host')
@click.option('-P', 'mysql_port', default=3306, help='MySQL 端口')
@click.option('-n', 'worker_num', default=4, help='消费者进程数')
def run(trec06c_path, stopwords_glob, mysql_db_name, mysql_user, mysql_password, mysql_host, mysql_port, worker_num):
    mysql_config = MySQLConnConfig(mysql_db_name, mysql_user, mysql_password, mysql_host, mysql_port)
    queue = multiprocessing.Queue(12)
    # stop_words = load_stop_list('/home/vimsucks/JupyterNotebook/dataset/stopwords/*.txt')
    # index = get_index('/home/vimsucks/JupyterNotebook/dataset/trec06c')
    stop_words = load_stop_list(stopwords_glob)
    index = get_index(trec06c_path)
    processes = list()
    # worker_num = 6
    producer = Producer(queue, index, worker_num)
    producer.start()
    processes.append(producer)
    for i in range(worker_num):
        worker = Worker(queue, stop_words, i, mysql_config)
        worker.start()
        processes.append(worker)

    for process in processes:
        process.join()


if __name__ == '__main__':
    run()
