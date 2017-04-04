import setuptools

setuptools.setup(
    name="nbinteract",
    version='0.0.24',
    url="https://github.com/data-8/nbinteract",
    author="Data 8",
    description="Simple Jupyter extension to use interact.",
    packages=setuptools.find_packages(),
    install_requires=[
        'notebook', 'pytest', 'webargs', 'requests', 'gitpython', 'toolz'
    ],
    package_data={'nbinteract': ['static/*']},
)
