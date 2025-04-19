from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='delgado_logger',
    version='0.1.1',
    author='Delgado',
    description='A lightweight and human-readable logging and CSV utility',
    long_description=long_description,
    long_description_content_type='text/markdown',  # <-- THIS IS CRITICAL
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    url='https://github.com/pyrometheous/Delgado-Logger',
    license='MIT'
)
