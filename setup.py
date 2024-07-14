from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='notion-news-crawler',
    version='0.0.9',
    url='https://github.com/kar7mp5/Notion-News-Crawler.git',
    author='MinSup Kim',
    author_email='tommy1005a@gmail.com',
    description='Notion news mecro',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['python-dotenv', 'tqdm', 'selenium', 'pytz', 'requests', 'retrying'],
    include_package_data=True,
)
