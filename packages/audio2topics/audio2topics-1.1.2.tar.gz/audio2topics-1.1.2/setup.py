from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="audio2topics",
    version="1.1.2",
    description="Extract topics directly from audio or text and text files",
    author="Mohsen Askar",
    author_email="ceaser198511@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.11",
        "numpy>=1.20.0",
        "pandas>=1.2.0",
        "matplotlib>=3.4.0",
        "openai-whisper==20240930",
        "nltk>=3.8.0,<3.10.0",
        "spacy>=3.1.0",
        "bertopic>=0.16.4",
        "wordcloud>=1.8.0",
        "scikit-learn==1.3.2",
        "python-docx>=0.8.10",
        "requests>=2.28.0",
        "torch==2.6.0",
        "sentence-transformers==3.4.1",              
        "pyLDAvis==3.4.1",
        "gensim==4.3.3",
        "PyQtWebEngine==5.15.7",
        "PyQtWebEngine-Qt5==5.15.2",
        "umap-learn==0.5.7",
        "seaborn>=0.12.0",
        "hdbscan==0.8.40",
        "scipy>=1.10.0",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    package_data={
        'audio2topics': ['resources/icons/*.png', 'resources/*/*'],
    },
    entry_points={
        "console_scripts": [
            "audio2topics=audio2topics.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
)