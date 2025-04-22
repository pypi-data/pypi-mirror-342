from setuptools import setup, find_packages
import re

def get_version():
    with open("phishscan/__init__.py", "r", encoding="utf-8") as f:
        content = f.read()
    return re.search(r"__version__\s*=\s*['\"](.+?)['\"]", content).group(1)

setup(
    name='phishscan',
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'confusables',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'phishscan=phishscan.cli:main',
        ],
    },
    package_data={
        'phishscan': ['phishing_keywords.txt'],
    },
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author="Makara_Chann",
    author_email="makara.chann.work@gmail.com",
    description="Phishing Email Scanner",
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
