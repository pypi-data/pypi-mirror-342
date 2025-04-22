from setuptools import setup, find_packages

setup(
    name='semban',                # the package name
    version='0.1.0',
    description='Simple wrapper for g4f chat client',
    author='sidh2690',
    author_email='you@example.com',
    packages=find_packages(),
    install_requires=[
        'g4f>=0.1.0',
    ],
    python_requires='>=3.7',
)
