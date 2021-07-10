from setuptools import setup, find_packages

# read the contents of README.md file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.3.5'

# print(find_packages())


setup(
  name='coppertop',
  packages=[
    'coppertop',
    'coppertop.tests',
    'coppertop_',
    'coppertop_.pipe',
    'coppertop_.pipe.tests',
    'coppertop_.std',
    'coppertop_.std.tests',
  ],
  package_dir = {'': 'core'},
  # namespace_packages=['coppertop_'],
  version=version,
  python_requires='>=3.8',
  license='BSD',
  description = 'Some batteries Python didn\'t come with',
  long_description_content_type='text/markdown',
  long_description=long_description,
  author = 'David Briant',
  author_email = 'dangermouseb@forwarding.cc',
  url = 'https://github.com/DangerMouseB/coppertop',
  download_url = '',
  # download_url = f'https://github.com/DangerMouseB/coppertop/archive/{version}.tar.gz',
  keywords = ['piping', 'pipeline', 'pipe', 'functional'],
  install_requires=[],
  include_package_data=True,
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    'Topic :: Utilities',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  zip_safe=False,
)
