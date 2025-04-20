from setuptools import setup, find_packages

setup(
    name='litleparser',
    version='0.1',
    packages=find_packages(),
    description='Библиотека для получения статических и динамических html страниц',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Ilia Miheev',
    author_email='statute-wasp-frisk@duck.com',
    install_requires=[
        'requests',
        'selenium'
    ],
    license='MIT',
)
