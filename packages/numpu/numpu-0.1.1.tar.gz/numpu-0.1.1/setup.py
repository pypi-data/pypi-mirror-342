from setuptools import setup, find_packages

setup(
    name='numpu',                # the package name
    version='0.1.1',
    description='',
    author='aaaroo',
    author_email='you@example.com',
    packages=find_packages(),
    install_requires=[
        'g4f>=0.1.0',
    ],
    python_requires='>=3.7',
)
