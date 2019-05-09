"""
多进程分词 trec06 数据集
"""
import glob
import pkuseg
import re
import pandas
import threading
from queue import Queue
import os
import click
from mail import *
from tqdm import tqdm

segmentation = pkuseg.pkuseg()


class Worker(threading.Thread):
    """
    消费者，分词数据集，并存入 MySQL
    """

    def __init__(self, queue, stop_words, spam_dir, ham_dir, thread_num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.stop_words = stop_words
        self.spam_dir = spam_dir
        self.ham_dir = ham_dir
        self.thread_num = thread_num

    def run(self) -> None:
        print('starting worker thread', self.thread_num)
        while True:
            path, spam = self.queue.get()
            if path is None and spam is None:
                break
            try:
                output_filename = '{}{}.txt'.format(path.split('/')[-2], path.split('/')[-1])
                output_file_path = os.path.join(self.spam_dir if spam else self.ham_dir, output_filename)
                if os.path.exists(output_file_path):
                    continue
                mail_content = get_mail_content(path)
                word_list = create_string_word_list(mail_content, self.stop_words)
                output_text = ','.join(word_list)
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(output_text)
            except Exception as e:
                print(path, e)


class Producer(threading.Thread):
    """
    生产者，读取 full/index 文件并发送给消费者
    """

    def __init__(self, queue, index, worker_num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.index = index
        self.worker_num = worker_num

    def run(self) -> None:
        print("starting producer thread, total:", len(self.index))
        pbar = tqdm(total=len(self.index))  # CLI 进度条
        pcount = 0  # 进度条统计
        for i, row in self.index.iterrows():
            self.queue.put((row.path, row.spam))
            pcount += 1
            if pcount == 100:
                pbar.update(pcount)
                pcount = 0
        pbar.update(pcount)
        pbar.close()
        print('done')
        for i in range(self.worker_num):
            self.queue.put((None, None))


def load_stop_list(file_glob):
    """
    加载停用词列表
    """
    stop_words = []
    for path in glob.glob(file_glob):
        with open(path, 'r') as f:
            lines = f.readlines()
        stop_words = stop_words + [i.strip() for i in lines]
    return set(stop_words)


def create_string_word_list(string, stop_words, seg=segmentation):
    """
    根据文本内容，创建这条文本的词表
    :param string: 字符串
    :param stop_words: 停用词列表
    :param seg: 分词器，如果为 None 则用全局实例
    :return
    """
    # 去除非中文字符
    string = re.findall(u'[\u4E00-\u9FD5]', string)
    string = ''.join(string)

    word_list = []
    # pkuseg 分词
    seg_list = seg.cut(string)
    for word in seg_list:
        if word != '' and word not in stop_words:
            word_list.append(word)
    return word_list


def get_index(trec06c_path):
    index = pandas.read_csv(os.path.join(trec06c_path, 'full/index'), sep=' ', names=['spam', 'path'])
    index.path = index.path.apply(lambda x: os.path.join(trec06c_path, x[1:]))
    index.spam = index.spam.apply(lambda x: True if x == 'spam' else False)
    return index


def make_data_dir(target_dir):
    spam_dir, ham_dir = os.path.join(target_dir, 'spam'), os.path.join(target_dir, 'ham')
    if not os.path.exists(spam_dir):
        os.makedirs(spam_dir)
        os.makedirs(ham_dir)
    return spam_dir, ham_dir


@click.command()
@click.option('-t', 'trec06c_path', default='./trec06c', help='trec06 数据集根路径，default ./trec06c')
@click.option('-s', 'stopwords_glob', default='./stopwords/\\*.txt', help='禁用词表 GLOB，default ./stopwords/\\*.txt')
@click.option('-T', 'target_dir', default='./data', help='输出文件目标目录，default ./data')
@click.option('-n', 'worker_num', default=4, help='消费者进程数，default 4')
def run(trec06c_path, stopwords_glob, target_dir, worker_num):
    queue = Queue(worker_num * 4)
    stop_words = load_stop_list(stopwords_glob)
    index = get_index(trec06c_path)
    spam_dir, ham_dir = make_data_dir(target_dir)

    threads = list()
    producer = Producer(queue, index, worker_num)
    producer.start()
    threads.append(producer)
    for i in range(worker_num):
        worker = Worker(queue, stop_words, spam_dir, ham_dir, i)
        worker.start()
        threads.append(worker)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    run()
