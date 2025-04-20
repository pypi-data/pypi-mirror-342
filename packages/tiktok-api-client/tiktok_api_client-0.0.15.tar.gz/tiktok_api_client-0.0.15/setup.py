from setuptools import setup, find_packages

setup(
    name="tiktok_api_client",
    version="0.0.15",
    description="A Python project for TikTok content publishing",
    author="Emmanuel Anthony",
    author_email="mymi14s@hotmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
    install_requires=[
        # "requests>=2.25",
    ],
    extras_require={
        "dev": ["black", "bumpver", "isort", "pip-tools", "pytest"],
    },
    entry_points={
        # "console_scripts": [
        #     "tiktok_api_client=tiktok_api_client.main:main",
        # ],
    },
    keywords=["tiktok", "api", "video"],
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mymi14s/tiktok_api_client",
)
