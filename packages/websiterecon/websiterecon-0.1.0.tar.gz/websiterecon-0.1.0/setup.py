from setuptools import setup, find_packages

setup(
    name="websiterecon",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.9.3",
        "rich>=13.7.0",
        "beautifulsoup4>=4.12.3",
        "dnspython>=2.6.1",
        "aiohttp-client-cache>=0.8.2",
        "aiodns>=3.1.1",
        "aiosocks>=0.2.6",
        "validators>=0.22.0",
        "asyncio>=3.4.3",
        "aiofiles>=23.2.1",
        "tld>=0.13.0"
    ],
    entry_points={
        'console_scripts': [
            'websiterecon=websiterecon.cli:main',
        ],
    },
    author="WebsiteRecon",
    author_email="websiterecon@example.com",
    description="A comprehensive website reconnaissance and scanning tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/websiterecon/websiterecon",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 