from setuptools import setup, find_packages

setup(
    name='borsaiti',
    version='0.8.6',
    description='Kick yayinlari icin AI destekli asistan',
    author='Aytunc',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'mtranslate',
        'ollama',
        'selenium',
        'soundcard',
        'soundfile',
        'speechrecognition',
        'undetected-chromedriver',
        'certifi'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
