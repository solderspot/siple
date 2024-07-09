from setuptools import setup, find_packages

setup(
    name='siple',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'spacy>=3.7.5,<4.0.0',
        'numpy>=1.26.4,<2.0.0',
        'scikit-learn>=1.5.1,<2.0.0',
    ],
    description='A command/action parsing library/framework for use in traditional texted based games.',
    author='Tom Rolfs',
    author_email='trolfs@gametoolworks.com',
    url='https://github.com/trolfs/siple',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.md files, include them:
        '': ['*.txt', '*.md'],
    },
    entry_points={
        'console_scripts': [
            'myparser=myparser.cli:main',  # Example of a command-line script entry point
        ],
    },
)
