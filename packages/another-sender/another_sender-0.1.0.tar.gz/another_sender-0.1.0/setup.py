from setuptools import setup, find_packages

setup(
    name="another-sender",
    version="0.1.0",
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
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourname/another-sender",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
