from setuptools import setup, find_packages

setup(
    name='mini_toker',
    version='0.2.0',
    description='A custom tokenizer with advanced token handling.',
    author='Yashraj Singh Rawat',
    packages=find_packages(),
    include_package_data=True,
    package_data={'mini_tokenizer': ['tokens.txt']},
    python_requires='>=3.6',
)
