from flask import Flask, request, jsonify
from flask_cors import CORS
from imageio import imread
from wordcloud import WordCloud
from train import *
from preprocess import *

app = Flask(__name__, static_folder='./static')
CORS(app)  # allow CORS for all domains on all routes
model: Model
chinese_font_path: str
stop_words: set


def api_response(success=True, data={}, code=0, message=''):
    return {
        'success': success,
        'data': data,
        'code': code,
        'message': message
    }


def load_model(model_pickle_filepath):
    with open(model_pickle_filepath, 'rb') as f:
        return pickle.load(f)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/wordcloud/spam')
def spam_word_cloud():
    """
    垃圾邮件词云
    :return:
    """
    created_at = model.created_at
    filename = 'spam_wordcloud{}{}{}{}{}.png'.format(created_at.year, created_at.month, created_at.day, created_at.hour,
                                                     created_at.minute)
    filepath = os.path.join('./static/images', filename)
    if not os.path.exists(filepath):
        word_set = model.word_set
        PS = model.PS
        word_dict = {word: ps for word, ps in zip(word_set, PS)}
        image_mask = imread('./static/images/MailIcon.jpg')
        wc: WordCloud = WordCloud(font_path=chinese_font_path, mask=image_mask,
                                  max_words=2000).generate_from_frequencies(word_dict)
        wc.to_file(filepath)
    return app.send_static_file(os.path.join('images', filename))


@app.route('/wordcloud/ham')
def ham_word_cloud():
    """
    正常邮件词云
    :return:
    """
    created_at = model.created_at
    filename = 'ham_wordcloud{}{}{}{}{}.png'.format(created_at.year, created_at.month, created_at.day, created_at.hour,
                                                    created_at.minute)
    filepath = os.path.join('./static/images', filename)
    if not os.path.exists(filepath):
        word_set = model.word_set
        PH = model.PH
        word_dict = {word: ps for word, ps in zip(word_set, PH)}
        image_mask = imread('./static/images/MailIcon.jpg')
        wc = WordCloud(font_path=chinese_font_path, mask=image_mask, max_words=2000).generate_from_frequencies(
            word_dict)
        wc.to_file(filepath)
    return app.send_static_file(os.path.join('images', filename))


@app.route('/identify', methods=['POST'])
def identify_mail():
    """
    判断邮件为垃圾邮件还是正常邮件
    POST /identify
    {
        "content": "邮件正文"
    }
    :return:
    {
        "success": true,
        "data": {
            "type": "spam",  // 或者 ham
            "warnMessage": "结果可能不正确：..."  // 当分词得到的词过少时会携带警告信息
        }
        message: ''
    }
    """
    data = request.get_json()
    content = data['content']
    if len(content) == 0:
        return jsonify(api_response(success=False, message='内容为空'))
    words = create_string_word_list(content, stop_words)
    vector = words2vector(model.word_set, words, model.word_dict)
    vectors = numpy.zeros((1, vector.shape[0]), dtype=numpy.uint8)
    vectors[0] = vector
    result = predictNB(vectors, model.Pspam, model.Pham, model.PS, model.PH, show_progress_bar=False)[0]
    ret_data = {'type': 'spam' if result == 1 else 'ham'}
    if len(set(words)) < 20:
        ret_data['warnMessage'] = '结果可能不正确：分词并去重后仅得到{}个词'.format(len(set(words)))
    return jsonify(api_response(data=ret_data))


@click.command()
@click.option('-h', 'host', default='0.0.0.0', help='监听 Host，default \'0.0.0.0\'')
@click.option('-p', 'port', default=5000, help='监听端口，default 5000')
@click.option('-d', 'debug', is_flag=True, default=False, help='开启调试模式')
@click.option('-m', 'model_pickle_filepath', default='./model.pickle', help='模型pickle文件路径，default \'./model.pickle\'')
@click.option('-z', 'zh_font_path', help='中文字体文件路径')
@click.option('-s', 'stopwords_glob', default='./stopwords/*.txt', help='禁用词表 GLOB，default ./stopwords/*.txt')
def main(host, port, debug, model_pickle_filepath, zh_font_path, stopwords_glob):
    global model, chinese_font_path, stop_words
    model = load_model(model_pickle_filepath)
    model.word_dict = {word: i for i, word in enumerate(model.word_set)}
    chinese_font_path = zh_font_path
    stop_words = load_stop_words(stopwords_glob)
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
