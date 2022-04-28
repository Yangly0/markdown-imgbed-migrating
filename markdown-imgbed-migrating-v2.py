#!/usr/bin/env/python
# -*- encoding: utf-8 -*-
"""
################################################################################
@File              :   markdown-imgbed-migrating-v2.py
@Time              :   2022/4/27 21:54:13
@Author            :   Yangliuly1
@Email             :   yangliuly1993@gmail.com
@Version           :   1.0
@Desc              :   markdown云端图片迁移到云端
########################################s########################################
"""

# Built-in modules
import argparse
import os
import re
import glob
import shutil
import requests
import time

# Third-party modules
import oss2

# Customized Modules
# import tooltik


def oss2_init(access_key_id, access_key_secret, endpoint, bucket_name):

    endpoint = f"http://{endpoint}.aliyuncs.com"
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    return bucket


def oss2_updown_file(oss_bucket, object, new_file_name, is_file=True):

    if is_file:
        res = oss_bucket.put_object_from_file(new_file_name, object)
    else:
        res = oss_bucket.put_object(new_file_name, object)

    return res.status == 200


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


def process_img2oss(input_path, output_path, patterns, headers, remote_name, dir_path):

    for filename in glob.glob(os.path.join(input_path, '*.md')):
        print("Processing: ", filename)

        path, _ = os.path.split(filename)
        # 解析文本
        try:
            lines = read_md(filename)

            for idx, line in enumerate(lines):
                for pattern in patterns:
                    urls = match_img(line, pattern)

                    for url in urls:
                        # print("=======> ", url)
                        if url == '':
                            continue

                        # new_filename = os.path.join(output_path, 'assets', img_name)

                        if 'http' in url or 'https' in url:
                            ret, img = download_img(url, headers)
                            if not ret:
                                print(f"Error, {url} download fail.")
                                continue

                            # 保存图片，以时间戳为名字
                            img_name = str(
                                time.strftime('%Y%m%d%H%M%S', time.localtime(int(
                                    time.time())))) + ".png"
                            new_file_name = f'{dir_path}/{img_name}'
                            oss2_updown_file(oss_bucket, img, new_file_name, is_file=False)
                        else:  # 本地图片
                            # continue
                            if ':' in url:  # : 判断绝对路径和相对路径
                                file_name = url
                            else:
                                file_name = os.path.join(path, url)

                            _, img_name = os.path.split(file_name)  # 本地图片名字不变
                            new_file_name = f'{dir_path}/{img_name}'
                            oss2_updown_file(oss_bucket, file_name, new_file_name, is_file=True)

                        # 修改源文件
                        lines[idx] = line.replace(url, f'{remote_name}/{dir_path}/{img_name}')

                _, name = os.path.split(filename)
                new_md_filename = os.path.join(output_path, name)
                write_md(new_md_filename, lines)
        except Exception as e:
            print(e)


def parse_args():
    parser = argparse.ArgumentParser(description="Markdown imgbed migrating V2.0")
    parser.add_argument("-i",
                        "--input_path",
                        type=str,
                        default="./input",
                        help="Input path of markdown file.")
    parser.add_argument("-o",
                        "--output_path",
                        type=str,
                        default="./output_path",
                        help="Ouput path of markdown file.")
    return parser.parse_args()


if __name__ == '__main__':

    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
    }
    # 阿里云支持
    access_key_id = ''  # 你的 AccessKeyId
    access_key_secret = ''  # 你的 AccessKeySecret
    endpoint = ''  # oss-cn-chengdu
    bucket_name = ''  # 存储库名字
    dir_path = ''  # 存储库下的图片存储文件夹

    assert len(access_key_id) != 0, "请配置阿里云参数"

    # 初始化oss接口，指定Bucket实例，所有文件相关的方法都需要通过Bucket实例来调用。
    oss_bucket = oss2_init(access_key_id, access_key_secret, endpoint, bucket_name)
    remote_name = f'https://{bucket_name}.{endpoint}.aliyuncs.com/'

    # 参数初始化
    args = parse_args()

    # 匹配模式
    patterns = [r'<img src=(.*?) ', r'!\[.*?\][()](.*)[)]']

    # 文件位置
    input_path = args.input_path
    # 存储新文件位置
    output_path = args.output_path
    os.makedirs(output_path, exist_ok=True)

    process_img2oss(input_path, output_path, patterns, headers, remote_name, dir_path)
