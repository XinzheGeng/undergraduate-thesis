# nb_spam 基于朴素贝叶斯的垃圾邮件过滤（识别）

## 准备工作
- Python 版本：3.7
- 创建 VirtualEnv：`virtualenv venv`
- 激活 VirtualEnv：`source venv/bin/activate`
- 安装依赖：`pip install -r requirements.txt`
- 解压数据集：`tar xvf trec06c.tgz`
- 安装词云（wordcloud）的依赖 `tk`（或者叫`libtk`）


## 运行

### 提前分词
```shell
# python3 preprocess.py --help
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
python3 preprocess.py -t ./trec06c -s 'stopwords/\*.txt' -T ./data -n 6
```

### 运行训练集、测试集，得到模型
```shell
# python3 train.py --help                            
Usage: predict.py [OPTIONS]

Options:
  -r FLOAT  读取数据集比例，default 1.0
  -t FLOAT  训练集集比例，default 0.67
  -d TEXT   dataset pickle 文件路径，程序在读取数据集时会自动生成/读取 pickle 文件以加快读取速度，default ''
  --help    Show this message and exit.
```
例如：
```shell
python3 predict.py -r 1 -t 0.67 -d ./dataset.pickle
```

### 启动开发/调试 Web 服务器
拷贝 `web_config.py.example` 为 `web_config.py` 并修改配置项

然后：
```shell
python3 web.py
```

### 启动本地正式服务器
```shell
gunicorn -b 0.0.0.0:8080 -k gevent -w 2 web:app
```

### 打包 Docker 镜像
该步骤需要写完成 `运行训练集、测试集，得到模型` 部分
```shell
docker build [镜像名称]:[版本号] .
```


### 运行 Docker 镜像
```shell
docker run -p 8080:8080 [镜像名称]:[版本号]
```


### 测试方法
运行 `preprocess.py`，删除dataset.pickle，开启过滤停用词，切分原数数据集，然后运行`test.py`测试。
运行 `preprocess.py`，删除dataset.pickle，关闭过滤停用词，切分原数数据集，然后运行`test.py`测试。
