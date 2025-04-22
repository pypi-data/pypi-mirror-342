from setuptools import setup, find_packages

setup(
    name='Salman-Ganteng-Banget',
    version='0.1.0',
    author='Nama Kamu',
    author_email='email@contoh.com',
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
