from setuptools import setup, find_packages

setup(
    name="pcalib",
    version="0.1.0",
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
        "pcalib": ["py/*.py", "cpp/*.so", "cpp/*.dll", "cpp/*.dylib"],
    },
    python_requires=">=3.8",
)