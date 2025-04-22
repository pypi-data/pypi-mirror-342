from setuptools import setup

setup(
    name="aiia_sdk",
    version="0.1.2",
    description="Official AIIA SDK for logging AI actions with legal and operational traceability",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="AIIA",
    author_email="javier.sanchez@aiiatrace.com",
    packages=["aiia_sdk"],
    package_dir={"aiia_sdk": "aiia_sdk"},
    package_data={
        "aiia_sdk": ["data/*.json", "cache/*.json"],
    },
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "cryptography>=39.0.0",
        "tldextract>=3.1.0",
        "sentence-transformers>=2.2.2"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)