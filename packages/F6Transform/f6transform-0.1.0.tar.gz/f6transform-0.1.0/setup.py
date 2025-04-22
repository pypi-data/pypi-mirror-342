from setuptools import setup, find_packages

setup(
    name='F6Transform',
    version='0.1.0',
    author='Xiangxing-Xu',  # 这里填你的名字或英文昵称
    author_email='iamxuxx@outlook.com',  # 这里填你的邮箱
    description='F6 Transform: A minimal library for 3D rigid transformations.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/iamxuxx/F6Transform',  # 以后如果有GitHub可以补上
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
