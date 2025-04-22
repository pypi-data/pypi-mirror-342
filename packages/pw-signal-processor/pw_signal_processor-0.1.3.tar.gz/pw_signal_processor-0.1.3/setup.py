import setuptools

setuptools.setup(
    name="pw-signal-processor",
    version="0.1.3",
    author="PinkWink",
    author_email="pinkwink@pinklab.art",
    description="A lightweight Python library offering moving average, first-order low-pass filtering, FFT, and STFT analysis.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pinklab-art/signal_processor",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.16.0",
        "matplotlib>=3.0.0",
        "scipy>=1.2.0"
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
