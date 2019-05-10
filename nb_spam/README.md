# nb_spam 基于朴素贝叶斯的垃圾邮件过滤（识别）

## 准备工作
- 安装依赖：`pip install -r requirements.txt`
- 解压数据集：`tar xvf trec06c.tgz`
- 安装词云（wordcloud）的依赖 `tk`（或者叫`libtk`）


## 运行

### 提前分词
```shell
# python preprocess.py --help
Usage: preprocess.py [OPTIONS]

Options:
  -t TEXT     trec06 数据集根路径，default ./trec06c
  -s TEXT     禁用词表 GLOB，default ./stopwords/\*.txt
  -T TEXT     输出文件目标目录，default ./data
  -n INTEGER  消费者进程数，default 4
  --help      Show this message and exit.
```
例如：
```shell
python preprocess.py -t ./trec06c -s 'stopwords/\*.txt' -T ./data -n 6
```

### 运行训练集、测试集
```shell
# python train.py --help                            
Usage: predict.py [OPTIONS]

Options:
  -r FLOAT  读取数据集比例，default 1.0
  -t FLOAT  训练集集比例，default 0.67
  -d TEXT   dataset pickle 文件路径，程序在读取数据集时会自动生成/读取 pickle 文件以加快读取速度，default ''
  --help    Show this message and exit.
```
例如：
```shell
python predict.py -r 1 -t 0.67 -d ./dataset.pickle
```

### 启动 Web 服务器
```shell
# python web.py --help                                                        
Usage: web.py [OPTIONS]

Options:
  -h TEXT     监听 Host，default '0.0.0.0'
  -p INTEGER  监听端口，default 5000
  -d          开启调试模式
  -m TEXT     模型pickle文件路径，default './model.pickle'
  -z TEXT     中文字体文件路径
  --help      Show this message and exit.
```
例如：
```shell
python web.py -z /usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc -d
```