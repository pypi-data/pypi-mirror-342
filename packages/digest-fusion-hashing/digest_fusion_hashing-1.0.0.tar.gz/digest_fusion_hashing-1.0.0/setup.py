from setuptools import setup, find_packages

setup(
    name='digest-fusion-hashing',
    version='1.0.0',
    description='A secure data integrity reinforcement technique using dual digest fusion with randomized splitting.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Miguel Gobbi',
    url='https://github.com/mGobb1/digest-fusion-hashing',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',
    ],
    python_requires='>=3.8',
)
