# -*- coding:UTF-8 -*-
'''
Created on 2014年12月5日

@author: caifh
'''
import pytest
import unittest
import creditutils.str_util as utils
import chardet


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testName(self):
        pass


def test_escape():
    a = '123我们'
    b = utils.escape(a)
    print(b)
    c = ascii(a)
    print(c)


def test_decode_escape():
    src = 'abc我们'
    print(src)
    dst = utils.escape_entire(src)
    print(dst)
    dst = utils.escape(src)
    print(dst)
    thd = utils.decode_escape(dst)
    print(thd)


def test_detect_encoding():
    src_buf = 'abcdef'.encode(encoding='ascii')
    #     print(utils.detect_encoding(src_buf))
    print(utils.decode_to_unicode(src_buf))
    #     print(chardet.detect(src_buf))

    src_buf = 'abc我们'.encode(encoding='utf-8')
    #     print(utils.detect_encoding(src_buf))
    print(utils.decode_to_unicode(src_buf))

    src_buf = '我们在哪里啊afd'.encode(encoding='gb2312')
    #     print(utils.detect_encoding(src_buf))
    print(utils.decode_to_unicode(src_buf))

def test_get_time_info():
    label_begin = 'begin'
    label_end = 'end'
    label_expected = 'expected'
    src_cases = [
        {
            label_begin: 100,
            label_end: 159.56,
            label_expected: '1m0s'
        },
        {
            label_begin: 100,
            label_end: 179.56,
            label_expected: '1m20s'
        },
        {
            label_begin: 100,
            label_end: 179.36,
            label_expected: '1m19s'
        },
    ]
    for item in src_cases:
        resutl = utils.get_time_info(item[label_begin], item[label_end])
        assert item[label_expected] == resutl

def test_maint():
    #     test_escape()
    #     test_decode_escape()
    test_detect_encoding()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    #     unittest.main()

    # test_maint()
    
    # argv = None
    curr_file_path = __file__
    argv = ["-s", curr_file_path]
    # 调用pytest的main函数执行测试
    pytest.main(argv) 
