from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="another-sender",
    version="0.1.1",
    packages=find_packages(),  # <-- must include another_sender
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'another-sender=another_sender.cli:main',
        ],
    },
    author="Nolan Manteufel",
    description="CLI to send command files over UDP, SPI, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minipcb/another-sender",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
