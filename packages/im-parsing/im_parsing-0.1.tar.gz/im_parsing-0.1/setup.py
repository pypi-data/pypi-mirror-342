from setuptools import setup, find_packages

setup(
    name='im-parsing',
    version='0.1',
    packages=find_packages(),
    description='Библиотека для получения статических и динамических html страниц',
    author='Ilia Miheev',
    author_email='statute-wasp-frisk@duck.com',
    install_requires=[
        'requests',
        'selenium'
    ],
    license='MIT'
)
