from setuptools import setup, find_packages

setup(
    name='bonsai-ml',
    version='0.0.1',
    description='bonsai',
    author='MAPS',
    author_email='dongguk.maps@gmail.com',
    url='https://github.com/leecheolu/bonsai-ml.git',
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['DT'],
    python_requires='>=3.7',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)