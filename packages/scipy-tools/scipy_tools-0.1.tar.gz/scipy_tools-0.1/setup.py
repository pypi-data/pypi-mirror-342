from setuptools import setup, find_packages

setup(
    name='scipy-tools',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    author='Your Name',
    author_email='your@email.com',
    description='A package that includes a scientific notebook',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/scipy-tools',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
