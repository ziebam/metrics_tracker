from setuptools import setup, find_packages

setup(
    name="Metrics Tracker",
    version=1.0,
    author="ziebam",
    author_email="ziebamichal@tutanota.com",
    license="MIT",
    description="A command-line metrics tracker.",
    url="https://github.com/ziebam/metrics_tracker",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={"console_scripts": ["mt=metrics_tracker.__main__:main",]},
)
