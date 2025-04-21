from setuptools import setup, find_packages

setup(
    name='expdl',
    version='0.1.0',
    packages=find_packages(),
    description='A simple deep learning experiment function',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Kimino namae',
    author_email='expvpn235@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
