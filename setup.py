import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '1.0.0'


def readme():
    with open('README.rst') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(name='text2num',
      version=VERSION,
      description='Parse and convert numbers written in french into their digit representation.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Filters',
        'Natural Language :: French'
      ],
      keywords='french NLP words-to-numbers',
      url='https://github.com/allo-media/text2num',
      author='Allo-Media',
      author_email='contact@allo-media.fr',
      license='MIT',
      packages=find_packages(),
      # install_requires=[
      #     'markdown',
      # ],
      python_requires='>=3',
      test_suite='text_to_num.tests',
      include_package_data=True,
      zip_safe=False,
      cmdclass={'verify': VerifyVersionCommand})
