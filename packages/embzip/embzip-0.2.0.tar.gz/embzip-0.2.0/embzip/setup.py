from setuptools import setup, find_packages

setup(
    name="embzip",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "torch>=1.0.0",
        "faiss-cpu>=1.7.0; platform_system!='Darwin' or platform_machine!='arm64'",
        "faiss-cpu-noavx2>=1.7.0; platform_system=='Darwin' and platform_machine=='arm64'",
    ],
    extras_require={
        "dev": [
            "faker",
            "pytest",
            "sentence-transformers",
        ],
    },
    description="A tool for compressing and decompressing embeddings using Product Quantization",
    author="embzip",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 