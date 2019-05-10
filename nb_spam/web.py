from flask import Flask
from imageio import imread
from train import Model
from wordcloud import WordCloud
import click
import pickle
import os

app = Flask(__name__, static_folder='./static')
model: Model
chinese_font_path: str


def load_model(model_pickle_filepath):
    with open(model_pickle_filepath, 'rb') as f:
        return pickle.load(f)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/wordcloud/spam')
def spam_word_cloud():
    created_at = model.created_at
    filename = 'spam_wordcloud{}{}{}{}{}.png'.format(created_at.year, created_at.month, created_at.day, created_at.hour,
                                                     created_at.minute)
    filepath = os.path.join('./static/images', filename)
    if not os.path.exists(filepath):
        word_set = model.word_set
        PS = model.PS
        word_dict = {word: ps for word, ps in zip(word_set, PS)}
        image_mask = imread('./static/images/MailIcon.jpg')
        wc = WordCloud(font_path=chinese_font_path, mask=image_mask, max_words=2000).generate_from_frequencies(
            word_dict)
        wc.to_file(filepath)
    return app.send_static_file(os.path.join('images', filename))


@app.route('/wordcloud/ham')
def ham_word_cloud():
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


@click.command()
@click.option('-h', 'host', default='0.0.0.0', help='监听 Host，default \'0.0.0.0\'')
@click.option('-p', 'port', default=5000, help='监听端口，default 5000')
@click.option('-d', 'debug', is_flag=True, default=False, help='开启调试模式')
@click.option('-m', 'model_pickle_filepath', default='./model.pickle', help='模型pickle文件路径，default \'./model.pickle\'')
@click.option('-z', 'zh_font_path', help='中文字体文件路径')
def main(host, port, debug, model_pickle_filepath, zh_font_path):
    global model, chinese_font_path
    model = load_model(model_pickle_filepath)
    chinese_font_path = zh_font_path
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
