from setuptools import setup, find_packages

setup(
    name="tbs",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/michaelkubiak/tbs",
    author="Michael Kubiak, Peter Kubiak(hopefully)",
    author_email="michaelaskubiak@bath.edu",
    description="Turn based strategy game with time travel",
    python_requires=">=3.7",
    tests_require=["pytest", "pytest_it"],
    script="bin/tbs",
)
