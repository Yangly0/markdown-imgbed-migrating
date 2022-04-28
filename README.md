# markdown-imgbed-migrating

Created by 2022-04-27 22:19:22

markdown-imgbed-migrating is a python script for dealing with markdown imgbed migrating.

Markdown文件中图床迁移到本地。

## Installation - 安装

- oss2

## Requirements - 必要条件

- python 3.x

## Usage - 用法

1. 云端图片下载到本地。

```bash
$ git clone https://github.com/Yangliuly1/markdown-imgbed-migrating.git
$ cd markdown-imgbed-migrating
$ python markdown-imgbed-migrating.py -i ./input -o ./output
```

2. 云端图片迁移到阿里云图床，需要配置参数：`access_key_id`, `access_key_secret`, `endpoint`, `bucket_name`和`dir_path`。

```bash
$ git clone https://github.com/Yangliuly1/markdown-imgbed-migrating.git
$ pip install oss2
$ cd markdown-imgbed-migrating
$ python markdown-imgbed-migrating-v2.py -i ./input -o ./output1
```

## Changelog - 更新日志

- [x] 2022.04.28 Mardkwon文件中图片从云端迁移到阿里云。

- [x] 2022.04.27 修复bug，本地图片无法转移。

- [x] 2022.04.27 Mardkwon文件中图片从云端下载到本地。

## License - 版权信息

License：[MIT](https://choosealicense.com/licenses/mit/)。
