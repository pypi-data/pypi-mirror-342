from setuptools import setup

setup(
    name='the_agreement',
    version='0.1.1',
    py_modules=['the_agreement'],
    description='A package that demonstrates a decorator for simulating a small part of female consent in China',
    author='Huang Hao Hua',
    author_email='13140752715@163.com',
    url='https://github.com/Locked-chess-official/the_agreement',
    python_requires='>=3.8',
    long_description=open('readme.md', encoding='utf-8').read() + '\n\n' + open('CHANGELOG.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license=open('LICENSE', encoding='utf-8').read()
)
