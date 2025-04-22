from setuptools import setup, find_packages

setup(
    name='New_AI_smvec',
    version='0.1',
    packages=find_packages(),
    install_requires=['nltk', 'scikit-learn'],
    author='Your Name',
    description='A simple chatbot using NLP',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
