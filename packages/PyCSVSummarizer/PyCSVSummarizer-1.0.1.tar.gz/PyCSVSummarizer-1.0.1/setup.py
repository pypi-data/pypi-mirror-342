from setuptools import setup, find_packages

setup(
    name='PyCSVSummarizer',
    version='1.0.1',
    description='A lightweight tool to summarize CSV files using various features.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Md. Ismiel Hossen Abir',
    author_email='ismielabir1971@gmail.com',
    packages=find_packages(),
    install_requires=[],  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
