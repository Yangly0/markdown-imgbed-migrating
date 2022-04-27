#!/usr/bin/env/python
# -*- encoding: utf-8 -*-
"""
################################################################################
@File              :   markdown-imgbed-migrating.py
@Time              :   2022/4/27 21:54:13
@Author            :   Yangliuly1
@Email             :   yangliuly1993@gmail.com
@Version           :   1.0
@Desc              :   markdown云端图片迁移到本地
########################################s########################################
"""

# Built-in modules
import argparse
import os
import re
import glob
import requests
import time

# Third-party modules
# import numpy as np

# Customized Modules
# import tooltik


def download_img(url, headers):
    img = requests.get(url, headers=headers)

    return img.status_code == 200, img.content


def match_img(line, pattern):

    url = re.findall(pattern, line, re.S)

    return url


def read_md(filename):

    with open(filename, mode="r", encoding='utf-8') as fp:
        lines = fp.readlines()

    return lines


def write_md(filename, lines):

    with open(filename, mode='w', encoding='utf-8') as fp:
        fp.writelines(lines)


def save_img(filename, img):
    fp = open(filename, 'ab')
    fp.write(img)
    fp.close()


def process_url2local(input_path, output_path, patterns, headers):
    for filename in glob.glob(os.path.join(input_path, '*.md')):
        print("processing: ", filename)

        # 解析文本
        lines = read_md(filename)

        for idx, line in enumerate(lines):
            for pattern in patterns:
                urls = match_img(line, pattern)

                for url in urls:
                    # print("=======> ", url)
                    if url == '':
                        continue

                    ret, img = download_img(url, headers)
                    if not ret:
                        print("Download fail.")
                        continue

                    # 保存图片，以时间戳为名字
                    img_name = str(time.strftime('%Y%m%d%H%M%S', time.localtime(int(
                        time.time())))) + ".png"
                    new_filename = os.path.join(output_path, 'assets', img_name)
                    save_img(new_filename, img)

                    # 修改源文件
                    lines[idx] = line.replace(url, os.path.join('assets', img_name))

            _, name = os.path.split(filename)
            new_md_filename = os.path.join(output_path, name)
            write_md(new_md_filename, lines)

def parse_args():
    parser = argparse.ArgumentParser(description="Markdown imgbed migrating V1.0")
    parser.add_argument("-i",
                        "--input_path",
                        type=str,
                        default="./input",
                        help="Input path of image.")
    parser.add_argument("-o",
                        "--output_path",
                        type=str,
                        default="./output_path",
                        help="Ouput path of image.")
    return parser.parse_args()


if __name__ == '__main__':

    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
    }

    args = parse_args()

    # 匹配模式
    patterns = [r'<img src=(.*?) ', r'!\[.*?\][()](.*)[)]']

    # 文件位置
    input_path = args.input_path
    # 存储新文件位置
    output_path = args.output_path

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join(output_path, 'assets'), exist_ok=True)
    process_url2local(input_path, output_path, patterns, headers)
