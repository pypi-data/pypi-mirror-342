from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='meu_investimento_josemarinho',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='José Paulo Marinho',
    author_email='josepaulomarinho2@gmail.com',
    description='Uma biblioteca para cálculos de investimentos',
    url='https://github.com/jusemarinho/meu_investimento',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    long_description=long_description,
    python_requires='>=3.6',
    long_description_content_type='text/markdown',
)