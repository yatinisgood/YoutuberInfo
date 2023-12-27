from setuptools import setup, find_packages

setup(
    name='YoutuberInfo',
    version='0.1.0',
    packages=find_packages(),
    description='A Python package to fetch information about YouTube channels',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yatinisgood/YoutuberInfo',
    install_requires=[
        # 依赖列表，例如:
        'requests',
        'beautifulsoup4',
    ],
)
