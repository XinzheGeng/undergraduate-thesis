"""
web.py
分类模块，Web 后端
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from imageio import imread
from wordcloud import WordCloud
from train import *
from preprocess import *
from web_config import config

app = Flask(__name__, static_folder='./static')
CORS(app)  # allow CORS for all domains on all routes
model: Model
chinese_font_path: str
stop_words: set


def load_model(model_pickle_filepath):
    with open(model_pickle_filepath, 'rb') as f:
        return pickle.load(f)


def setup_app(app: Flask):
    """
    进行一些初始化工作
    :param app:
    :return:
    """
    app.debug = config['debug']
    global model, chinese_font_path, stop_words
    model = load_model(config['model_pickle_filepath'])
    model.word_dict = {word: i for i, word in enumerate(model.word_set)}
    chinese_font_path = config['zh_font_filepath']
    stop_words = load_stop_words(config['stopwords_file_glob'])


setup_app(app)


def api_response(success=True, data={}, code=0, message=''):
    return {
        'success': success,
        'data': data,
        'code': code,
        'message': message
    }


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
    results, probabilities = predict_nb(vectors, model.Pspam, model.Pham, model.PS, model.PH, show_progress_bar=False)
    pspam, pham = probabilities[0]
    ret_data = {'type': 'spam' if results[0] == 1 else 'ham', "pspam": pspam, "pham": pham}
    if len(set(words)) < 20:
        ret_data['warnMessage'] = '结果可能不正确：分词并去重后仅得到{}个词'.format(len(set(words)))
    return jsonify(api_response(data=ret_data))


@app.route('/stat')
def stat():
    return jsonify(api_response(data={
        "wordSetCount": len(model.word_set),
        "stopWordsCount": len(stop_words),
        "Pspam": model.Pspam,
        "Pham": model.Pham,
    }))


@app.route('/stat/wordset')
def word_set():
    return jsonify(model.word_set)


@app.route('/stat/stopwords')
def stopwords():
    return jsonify(list(stop_words))


@app.route('/stat/PS')
def PS():
    return jsonify(model.PS.tolist())


@app.route('/stat/PH')
def PH():
    return jsonify(model.PH.tolist())


if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'], debug=config['debug'])
