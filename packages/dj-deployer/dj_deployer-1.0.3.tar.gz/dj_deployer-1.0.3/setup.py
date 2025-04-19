from setuptools import setup, find_packages

setup(
    name='dj-deployer',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        'fabric>=3.0',
        'click>=8.0',
        'pyyaml>=6.0',
    ],
    entry_points={
        'console_scripts': [
            '   dj-deployer=django_deployer.cli:main',
            'deploy=django_deployer.cli:main',
        ],
    },
    author='Mohammad Namdar',
    description='A simple CLI tool to deploy Django projects via SSH',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
