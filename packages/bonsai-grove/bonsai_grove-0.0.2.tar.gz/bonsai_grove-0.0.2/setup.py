from setuptools import setup, find_packages

setup(
    name='bonsai_grove',
    version='0.0.2',
    description='bonsai',
    author='MAPS',
    author_email='dongguk.maps@gmail.com',
    url='https://github.com/leecheolu',
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