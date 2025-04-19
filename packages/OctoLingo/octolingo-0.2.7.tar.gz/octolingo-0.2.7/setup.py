from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='OctoLingo',
    version='0.2.7',  # Bumped version for new functionality
    description='A Python package for translating large texts with advanced features including OCR support.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Birhan Tamiru',
    author_email='birhantamiru281@gmail.com',
    packages=find_packages(),
    install_requires=[
        'googletrans==4.0.0-rc1',
        'easyocr>=1.6.2',
        'python-magic>=0.4.27',
        'pillow>=9.5.0',
        'pdfplumber>=0.9.0',
        'python-docx>=0.8.11',
        'asyncio>=3.4.3',
    ],
    extras_require={
        'windows': ['python-magic-bin>=0.4.14'],
        'linux': ['python-magic>=0.4.27'],
        'mac': ['python-magic>=0.4.27'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    keywords='translation ocr language text-processing'
)