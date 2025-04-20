from setuptools import setup, find_packages

setup(
    name='phishscan',
    version='0.1.4',
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
    long_description=open('README.md').read(),
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
