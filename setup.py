import setuptools

setuptools.setup(
    name="nbpuller",
    version='0.1.9',
    url="https://github.com/data-8/nbpuller",
    author="Data 8 @ UC Berkeley",
    description="Simple Jupyter extension to update files with remote git repository.",
    packages=setuptools.find_packages(),
    install_requires=[
        'notebook', 'pytest', 'webargs', 'requests', 'gitpython', 'toolz'
    ],
    package_data={'nbpuller': ['static/*']},
)
.12
