from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bgral",
    version="0.2.0",
    author="Bhavya Gujral",
    author_email="bhavya.gujral2608@gmail.com",
    description="A Python library for video style transfer and utility functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bhavyagujral26/bgral",
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.8.0",
        "tensorflow-hub",
        "opencv-python",
        "pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries"
    ],
    python_requires=">=3.6",
    license="MIT",
)
