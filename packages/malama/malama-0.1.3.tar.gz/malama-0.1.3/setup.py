from setuptools import setup, find_packages

setup(
    name='malama',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'pymupdf',
        'google-generativeai',
    ],
    author='Manoj Prajapati',
    author_email='manojbittu161@gmail.com',
    description='PDF assistant using Gemini API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
