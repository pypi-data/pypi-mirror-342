from setuptools import setup, find_packages

setup(
    name='datav_client',
    version='1.1.0.9',
    description='datav爬取数据通用组件客户端',
    author='python之父·博思之光·杨瑞',
    packages=['datav_client'],
    install_requires=[
        'pypinyin',
        'Style',
        'loguru==0.7.2',
        'Flask'
    ],
)
