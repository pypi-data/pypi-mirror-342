from setuptools import setup, find_packages

# Exclude the parser directory from installation
setup(
    name='pysmsl',
    version='0.1.0',
    packages=find_packages(exclude=['smsl.smsl_parser', 'smsl.smsl_parser.*']),
    install_requires=[
        'pyyaml',
        'networkx',
        'matplotlib',
    ],
    author='Yihao Liu',
    author_email='yihao.jhu@gmail.com',
    description='State Machine Serialization Language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SMSL-Project/pysmsl',
    license='MIT',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)