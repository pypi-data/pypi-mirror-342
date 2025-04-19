from setuptools import setup, find_packages

version = {}
with open("__version__ .py") as f:
    exec(f.read(), version)

setup(
    name="lakehouse-dataflow",
    version=version["__version__"],
    description="Pipeline de dados da Lakehouse",
    author="i9 Internet",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=1.0.0",
        "requests>=2.0.0",
    ],
    python_requires=">=3.8",
)
