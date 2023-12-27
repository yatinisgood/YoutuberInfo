from setuptools import setup

setup(
    name='YoutuberInfo',
    version='0.1.0',
    py_modules=['YoutuberInfo_Grap'],
    description='A Python package to fetch information about YouTube channels',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yatinisgood/YoutuberInfo',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)