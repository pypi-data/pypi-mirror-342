from setuptools import setup, find_packages

setup(name='neurony',
      version='0.0.1',
      url='https://github.com/dogman0121/neurony',
      license='MIT',
      author='Ivan Vasilev',
      author_email='vasilevib@yandex.ru',
      description='Manage configuration files',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,)