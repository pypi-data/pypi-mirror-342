from setuptools import setup, find_packages

setup(
    name='vex_ast',
    version='0.2.0',
    description='A Python package for generating Abstract Syntax Trees for VEX V5 code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Chaze',
    author_email='chazelexander@example.com',
    url='https://github.com/heartx2/vex_ast',
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'mypy>=1.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
)
