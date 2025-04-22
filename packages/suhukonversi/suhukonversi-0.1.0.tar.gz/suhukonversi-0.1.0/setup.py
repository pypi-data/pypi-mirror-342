from setuptools import setup, find_packages

setup(
    name='suhukonversi',
    version='0.1.0',
    author='Tikature',
    author_email='detikaa10@gmail.com',
    description='Library Python untuk konversi suhu antara Celsius, Fahrenheit, dan Kelvin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)
