from setuptools import setup, find_packages

setup(
    name='vex_ast',
    version='0.1.0',
    description='A Python package for generating Abstract Syntax Trees for VEX V5 code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Chaze',  # Replace with your actual name
    author_email='chazelexander@example.com',  # Replace with your actual email
    url='https://github.com/teowy/vex_ast',  # Replace with your actual repository URL
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        # Add runtime dependencies here if any
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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