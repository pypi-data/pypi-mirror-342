from setuptools import setup

setup(
    name="cloudcode",
    version="0.0.1",
    description="Code the thing that Codes the thing",
    author="Sean Sullivan",
    author_email="sean@lmsystems.ai",
    py_modules=["lmsys"],
    install_requires=[
        "aider-chat>=0.82.1",
        "e2b-code-interpreter"
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)