from setuptools import setup, find_packages

setup(
    name='stukk',
    version='0.0.1_dev1',
    author='WipoDev',
    author_email='ajwipo@gmail.com',
    description='Library for designing graphical interfaces with Tkinter in a simple and stylized way.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wipodev/stukk',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
