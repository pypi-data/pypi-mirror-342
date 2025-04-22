from setuptools import setup, find_packages

setup(
    name='ll_kugou_lyric_api',              # 包名
    version='0.1.3',
    packages=find_packages(),       # 自动找到子包
    install_requires=[],            # 如果有依赖包，写这里
    author='刘龙',
    author_email='1053278842@qq.com',
    description='酷狗音乐相关API开发包',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
