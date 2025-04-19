from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

current_dir = os.path.dirname(os.path.abspath(__file__))
requirements_path = os.path.join(current_dir, "requirements.txt")

with open(requirements_path, "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="smolhub_download",
    version="0.1.4", # Incremented version
    author="SmolHub",
    author_email="contact@smolhub.com",
    description="A Python client for downloading models and datasets from SmolHub via Supabase", # Updated description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smolhub/smolhub_download",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "": ["requirements.txt"],
    },
)