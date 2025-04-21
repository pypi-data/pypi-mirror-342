from setuptools import setup, find_packages

setup(
    name='auditflow',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scipy'
    ],
    author='Ashwin',
    author_email='programmingashwin@gmail.com',
    description='A Python package to generate visual data quality audits.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
