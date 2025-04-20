from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eet-toolkit",
    version="1.0.1",
    author="Script1337",
    author_email="your.email@example.com",
    description="Email Enumeration Toolkit with GUI and CLI interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/script1337/eet-toolkit",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "eet_toolkit": ["samples/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "PyQt6",
        "imaplib2",
        "jinja2",
        "pyyaml",
        "PySocks",
    ],
    entry_points={
        "console_scripts": [
            "eet-send=eet_toolkit.redmail:send_emails_cli",
            "eet-read=eet_toolkit.redmail:read_emails_cli",
            "eet=eet_toolkit.redmailer_gui:main",
        ],
    },
) 