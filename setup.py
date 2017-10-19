from setuptools import setup, find_packages
import os
import codecs


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='django-cdnjs',
    packages=find_packages(),
    version='2017.10.19-0',
    license='MIT',
    description=(
        'Django template plugin to be used to simplify static CDN resources '
        'connecting.'
    ),
    long_description=read('README.rst'),
    author='Maxim Papezhuk',
    author_email='maxp.job@gmail.com',
    url='https://github.com/duverse/django-cdnjs',
    download_url='https://github.com/duverse/django-cdnjs/tarball/v2017.10.19-0',
    keywords=[
        'django',
        'cdn',
        'cdnjs',
        'templatetag'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
