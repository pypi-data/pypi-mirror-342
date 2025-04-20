from setuptools import setup, find_packages

setup(
    name='intergen',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'tensorflow',
        'scikit-learn'
    ],
    author='Mustafa Ekmekci',
    description='INTERGEN: Interactive Neural Generalization Framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/intergen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)