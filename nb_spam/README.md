# nb_spam 基于朴素贝叶斯的垃圾邮件过滤（识别）

## 准备工作
- 解压数据集：`tar xvf trec06c.tgz`

## 提前分词
```shell
python async_cut_words.py -t [trec06c数据集路径] -s [禁用词表GLOB] -d [MySQL数据库名] -u [MySQL用户名] -p [MySQL密码] -h [MySQLHost] -P [MySQL端口] -n [用于分词的进程数目]
```
例如：
```shell
python async_cut_words.py -t trec06c -s 'stopwords/\*.txt' -d nb_spam -u root -p root -h localhost -P 3306 -n 6
```