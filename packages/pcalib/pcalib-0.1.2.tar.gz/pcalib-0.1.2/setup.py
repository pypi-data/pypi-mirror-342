from setuptools import setup, find_packages

setup(
    name="pcalib",
    version="0.1.2",
    description="PCA and linear algebra library with C++ backend",
    author="Selim Poladov",
    author_email="main@netherite.ru",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "scikit-learn"
    ],
    include_package_data=True,
    package_data={
        "pcalib": ["py/*.py", "py/*.dylib"],
    },
    python_requires=">=3.8",
)