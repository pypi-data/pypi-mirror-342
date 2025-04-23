from setuptools import setup, find_packages

setup(
    name='mp3lyrics',
    version='0.1.0',
    description='Fetch lyrics from Genius and embed into MP3 metadata',
    author='Odhran McElhinney',
    author_email='odhranmcelhinney@hotmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'html2text',
        'eyed3',
        'fuzzywuzzy',
        'python-Levenshtein',
        'alive-progress'
    ],
    entry_points={
        'console_scripts': [
            'mp3lyrics=mp3lyrics.mp3lyrics:main_cli',
        ],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
