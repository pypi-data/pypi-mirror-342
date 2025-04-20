from setuptools import setup, find_packages

setup(
    name='phishscan',
    version='1.0.1',
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
    long_description=open('README.md').read(),  # Optional: Readme file for description
    long_description_content_type='text/markdown',  # Optional: Readme format
    author="Makara_Chann",  # Replace with your name
    author_email="makara.chann.work@gmail.com",  # Replace with your email
    description="Phishing Email Scanner",  # Short description of the package
    license="MIT",  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update if using a different license
        'Operating System :: OS Independent',
    ],
)
