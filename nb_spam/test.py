"""
测试模块
"""
import click
import numpy
from train import run


@click.command()
@click.option('-t', 'train_size', default=40000, help='训练集集大小，default 40000')
@click.option('-T', 'test_size', default=20000, help='测试集大小, default 20000')
@click.option('-n', 'run_times', default=10)
def main(train_size, test_size, run_times):
    word_set_length_vec = numpy.zeros(run_times, dtype=numpy.float64)
    accuracy_vec = numpy.zeros(run_times, dtype=numpy.float64)
    precision_vec = numpy.zeros(run_times, dtype=numpy.float64)
    recall_vec = numpy.zeros(run_times, dtype=numpy.float64)
    for i in range(run_times):
        print('====第{}次运行'.format(i + 1))
        word_set, accuracy, precision, recall = run(train_size, test_size, './dataset.pickle', '.model.pickle')
        word_set_length_vec[i], accuracy_vec[i], precision_vec[i], recall_vec[i] = len(
            word_set), accuracy, precision, recall
    word_set_length_mean = numpy.mean(word_set_length_vec)
    accuracy_mean = numpy.mean(accuracy_vec)
    precision_mean = numpy.mean(precision_vec)
    recall_mean = numpy.mean(recall_vec)
    print('训练集大小 {}，测试集大小 {}，运行 {} 次平均值词集长度 {}，准确率 {}，精确率 {}，召回率 {}'.format(train_size, test_size, run_times,
                                                                            word_set_length_mean, accuracy_mean,
                                                                            precision_mean, recall_mean))


if __name__ == '__main__':
    main()
