from setuptools import setup, find_packages

setup(
    name="embzip",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "torch",
        "faiss-cpu",
    ],
    description="A tool for compressing and decompressing embeddings using Product Quantization",
    author="embzip",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 