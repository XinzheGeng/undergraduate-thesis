import email


def get_message(path):
    """
    根据邮件路径解析邮件
    :param path: 邮件路径
    :return message: message object
    """
    with open(path, 'r', encoding='gbk', errors='ignore') as f:
        content = f.read()
        return email.message_from_string(content)


def get_payload(message):
    """
    获取邮件正文
    :param message: 邮件
    :return payload: 邮件正文
    """
    payload = ''
    if message.is_multipart():
        for part in message.get_payload():
            payload += part.get_payload()
    else:
        payload = message.get_payload()
    return payload


def get_content(path):
    """
    根据邮件路径提取邮件中的文本数据
    :param path: 邮件路径
    :return content: 邮件文本
    """
    # 邮件数据是 gbk 编码, 忽略无法解码的内容
    with open(path, 'r', encoding='gbk', errors='ignore') as f:
        content = f.read()
        message = email.message_from_string(content)
        payload = ''
        if message.is_multipart():
            for part in message.get_payload():
                payload += part.get_payload()
        else:
            payload = message.get_payload()
        print(payload)
        lines = f.readlines()
    for i in range(len(lines)):
        if lines[i] == '\n':
            # 去除空行
            lines = lines[i:]
            break
    content = ''.join(''.join(lines).strip().split())
    return content


if __name__ == '__main__':
    print(get_payload(get_message('/home/vimsucks/JupyterNotebook/dataset/trec06c/data/001/002')))
