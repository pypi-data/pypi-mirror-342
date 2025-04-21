from setuptools import setup, find_packages

setup(
    name='PyEasyDB',
    version='0.1.0',
    description='A simple and lightweight Python library for easy database management.',
    author='RedSnows',
    author_email='id.suzuya@email.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
