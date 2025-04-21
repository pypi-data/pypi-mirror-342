from setuptools import setup

setup(
    name='SetDB',
    version='0.1',
    author='Kayra Aça',
    author_email='kayraaca@gmail.com',
    description='The simplest way to set up a Python database',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/SetDB/',
    packages=['setdb'],  # folder name
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
