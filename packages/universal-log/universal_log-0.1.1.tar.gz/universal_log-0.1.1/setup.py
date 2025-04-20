from setuptools import setup, find_packages

setup(
    name="universal-log",
    version="0.1.1",
    description="Universal logger that adds console.log, System.out.println, and more globally to Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/yourusername/universal-log",
    packages=find_packages(),
    include_package_data=True,
    package_data={"universal_log": ["py.typed", "*.pyi"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Typing :: Typed",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
