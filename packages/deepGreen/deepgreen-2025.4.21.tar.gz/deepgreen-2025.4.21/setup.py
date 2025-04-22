from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='deepGreen',  # required
    version='2025.4.21',
    description='deepGreen: a machine learning based tree-ring width model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Feng Zhu',
    author_email='fengzhu@ucar.edu',
    url='https://github.com/fzhu2e/deepGreen',
    packages=find_packages(),
    include_package_data=True,
    license='BSD-3',
    zip_safe=False,
    keywords=['Machine Learning', 'Tree-ring Width', 'Proxy System Model'],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=[
        'colorama',
        'tqdm',
        'torch',
    ],
)
