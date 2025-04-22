from setuptools import setup, find_packages

setup(
    name='gyatModule',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'gyat_module': ['file1.txt', 'file2.txt', 'file3.txt'],
    },
    author='Your Name',
    description='A sample package that prints text file content',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
