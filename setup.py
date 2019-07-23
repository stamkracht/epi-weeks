from setuptools import setup, find_packages


def get_here():
    try:
        import pathlib
    except ImportError:
        import pathlib2 as pathlib

    here = pathlib.Path(__file__).parent
    return here


class LongDescription(object):
    def __str__(self):
        here = get_here()
        readme = (here / "README.rst").read_text(encoding="utf-8")
        changelog = (here / "CHANGELOG.rst").read_text(encoding="utf-8")
        return readme + "\n" + changelog

    def __unicode__(self):
        raise Exception('unicode')


class PyModules(object):
    @property
    def data(self):
        here = get_here()
        return [module.stem for module in here.glob("src/*.py")]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)




setup(
    name="epiweeks",
    version="1.0.0",
    description="Epidemiological weeks by US CDC and WHO calculation methods.",
    long_description=LongDescription(),
    url="",
    project_urls={
        "Source Code": "https://github.com/dralshehri/epi-weeks",
        "Documentation": "https://epiweeks.readthedocs.io/en/latest",
    },
    author="Mohammed Alshehri",
    author_email="",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
    keywords="epidemiology epi weeks date calendar cdc who",
    py_modules=PyModules(),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=['typing;python_version<"3.5"'],
    setup_requires=['pathlib2;python_version<"3"'],
)
