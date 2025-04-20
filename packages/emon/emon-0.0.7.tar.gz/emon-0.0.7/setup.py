from setuptools import setup, find_packages

setup(
    name='emon',
    version='0.0.7',
    packages=find_packages(include=['emon', 'emon.*']),
    include_package_data=True,
    package_data={
        'emon': ['*'],
    },
    install_requires=[
        'numpy',
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        'xgboost>=1.5.0',  # Added XGBoost requirement
        'joblib>=1.1.0',
        'seaborn>=0.11.0',
        'matplotlib>=3.4.0',
        'tqdm>=4.62.0',
        'tensorflow>=2.6.0'  # Optional: Consider making this an extra requirement
    ],
    author='ABS EMON',
    author_email='iotandrobotics@gmail.com',
    description='Easy AutoML package to clean, train and export models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ABS-EMON/emon',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'emon=emon.cli:main',  # Optional: Add CLI support if needed
        ],
    }
)