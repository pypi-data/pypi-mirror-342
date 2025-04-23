from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='CalcOge',
  version='0.0.1',
  author='Scholoch',
  author_email='alf.201105@gmail.com',
  description='Simple calculation of OGE tasks',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Scholoch/oge-calc.git',
  packages=find_packages(),
  install_requires=[''],
  classifiers=[
    'Programming Language :: Python :: 3.13',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='oge calc ',
  project_urls={
    'GitHub': 'https://github.com/Scholoch'
  },
  python_requires='>=3.6'
)