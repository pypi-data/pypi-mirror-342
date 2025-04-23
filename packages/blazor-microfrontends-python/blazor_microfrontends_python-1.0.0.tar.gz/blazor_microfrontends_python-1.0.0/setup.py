from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blazor-microfrontends-python",
    version="1.0.0",
    author="Blazor Microfrontends Team",
    author_email="support@blazor-microfrontends.com",
    description="Python SDK for Blazor Microfrontends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WonderBoyHub/BlazorMicrofrontends",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.1.0",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "flask>=2.3.3",
        "flask-cors>=4.0.0",
        "django>=4.2.5",
        "djangorestframework>=3.14.0",
        "django-cors-headers>=4.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "blazor-mf=blazor_microfrontends.cli:main",
        ],
    },
) 