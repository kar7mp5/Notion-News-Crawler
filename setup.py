from setuptools import setup, find_packages

setup(
    name='notion-news-crawler',
    version='0.0.1',
    url='https://github.com/kar7mp5/korean-news-scraper.git',
    author='MinSup Kim',
    author_email='tommy1005a@gmail.com',
    description='Notion news mecro',
    packages=find_packages(),
    install_requires=['python-dotenv', 'tqdm', 'selenium', 'pytz', 'requests', 'retrying'],
)