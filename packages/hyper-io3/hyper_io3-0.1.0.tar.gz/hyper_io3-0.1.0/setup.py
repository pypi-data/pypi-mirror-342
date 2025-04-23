from setuptools import setup, find_packages

setup(
    name='hyper-io3',  # Name of the package
    version='0.1.0',  # Initial version
    author='imAnesYT Dev',  # Your name or company
    author_email='imanesytdev.contact@gmail.com',  # Your email
    description='A fast and flexible HTTP client for Python with sync and async support.',
    long_description=open('README.md').read(),  # Read from the README file
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/hyperio',  # Your GitHub or project URL
    packages=find_packages(),  # Automatically find all packages in the project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',  # Minimum Python version
    install_requires=[
        'requests>=2.25.0',
        'aiohttp>=3.7.0',
        'beautifulsoup4>=4.9.0',
    ],
    entry_points={},
)
