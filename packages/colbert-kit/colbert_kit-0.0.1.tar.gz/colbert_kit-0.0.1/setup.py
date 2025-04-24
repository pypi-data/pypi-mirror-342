from setuptools import setup, find_packages

setup(
    name="colbert-kit",
    version="0.0.1",
    packages=find_packages(),

    install_requires=[
        "pandas >= 2.2.3",
        "numpy >= 1.26.4, <2.0.0",
        "torch >= 2.4.1",
        "transformers >= 4.44.2",
        "sentence-transformers >= 3.2.0",
        "rank-bm25 >= 0.2.2",
        "stop-words == 2018.7.23"
    ],

    extras_require={
        "cpu": ["faiss-cpu >= 1.10.0"],
        "gpu-cu11": ["faiss-gpu-cu11"],
        "gpu-cu12": ["faiss-gpu-cu12"]
    },

    author="Thuong Dang, Qiqi Chen",
    author_email="dangtuanthuong@gmail.com",
    description="Package for ColBERT models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/thuongtuandang/colbert-kit",
    license_files=['LICENSE'],
    license='MIT',
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
