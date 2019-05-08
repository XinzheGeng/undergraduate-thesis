from mail import *
import glob
import pkuseg
import re
import pickle
import peewee

segmentation = pkuseg.pkuseg()


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


def word_count_dict(words):
    """
    统计词语次数，转成 dict
    """
    dic = {}
    for word in words:
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1
    return dic


def create_string_word_dict(string, stop_list, seg=segmentation):
    """
    根据文本内容，创建这条文本的词典
    :param string: 字符串
    :param stop_list: 停用词列表
    :param seg: 分词器，如果为 None 则用全局实例
    :return
    """
    string = re.findall(u'[\u4E00-\u9FD5]', string)
    string = ''.join(string)

    word_list = []
    # pkuseg 分词
    seg_list = seg.cut(string)
    for word in seg_list:
        if word != '' and word not in stop_list:
            word_list.append(word)
    word_dict = word_count_dict(word_list)
    return word_dict


def get_or_create_mail(real_path, spam, path, stop_words, Mail):
    """
    根据文本内容，创建这条文本的词典
    :param real_path: 文件路径
    :param spam: 是否是垃圾邮件
    :param stop_words: 禁用词
    :return Mail
    """
    try:
        mail = Mail.get(Mail.path == path)
        mail.message = pickle.loads(mail.message_blob)
        mail.words = pickle.loads(mail.words_blob)
        return mail, True
    except peewee.DoesNotExist:
        message = get_message(real_path)
        content = get_payload(message)
        words = create_string_word_dict(content, stop_words)
        mail = Mail.create(path=path, spam=spam, content=content, message_blob=pickle.dumps(message),
                           words_blob=pickle.dumps(words))
        mail.message = message
        mail.words = words
        return mail, False


if __name__ == '__main__':
    print(load_stop_list('/home/vimsucks/JupyterNotebook/dataset/stopwords/*.txt'))
    print(word_count_dict(['test', 'test', 'hello']))
