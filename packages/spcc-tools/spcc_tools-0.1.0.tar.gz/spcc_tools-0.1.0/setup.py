from setuptools import setup, find_packages

setup(
    name="spcc-tools",
    version="0.1.0",
    author="Vivek Yadav",
    author_email="example@example.com",
    description="System Programming and Compiler Construction tools and experiments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/spcc-tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "ply",  # For lexical analysis
    ],
    entry_points={
        "console_scripts": [
            "spcc-assembler=spcc_tools.assembler.two_pass:main",
            "spcc-macro=spcc_tools.macro.expander:main",
            "spcc-follow=spcc_tools.cfg.follow:main",
            "spcc-first=spcc_tools.cfg.first:main",
            "spcc-lexcount=spcc_tools.lexical.counter:main",
        ],
    },
)