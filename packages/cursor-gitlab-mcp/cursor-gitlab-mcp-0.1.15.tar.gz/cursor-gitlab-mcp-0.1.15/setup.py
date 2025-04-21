from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cursor-gitlab-mcp",
    version="0.1.15",
    author="ansonglin",
    author_email="songlin.an@dmall.com",
    description="一个用于Cursor IDE的GitLab操作服务",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gitlab-mcp",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
        "python-gitlab>=3.0.0",
        "typer>=0.9.0",
        "urllib3>=2.0.0"
    ],
    entry_points={
        "mcp.plugins": [
            "cursor-gitlab-mcp=gitlab_mcp.server:main",
        ],
    },
) 
