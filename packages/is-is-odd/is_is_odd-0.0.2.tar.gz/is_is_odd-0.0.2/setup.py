import pathlib as p
import re as regex

import setuptools

PACKAGE_NAME_SNAKE_CASE = "is_is_odd".replace("-", "_")
PACKAGE_NAME_KEBAB_CASE = PACKAGE_NAME_SNAKE_CASE.replace("_", "-")
DESCRIPTION = "check if the given module is is-odd"


def main():
	version_file = p.Path(f"./{PACKAGE_NAME_SNAKE_CASE}/_version.py")

	__version__ = regex.search(VERSION_REGEX, version_file.read_text()).group(1)

	setuptools.setup(
		name=PACKAGE_NAME_SNAKE_CASE,
		version=__version__,
		description=DESCRIPTION,
		long_description=p.Path("./README.md").read_text(),
		long_description_content_type="text/markdown",
		url=f"https://github.com/anamoyee/{PACKAGE_NAME_KEBAB_CASE}",
		author="anamoyee",
		license="WTFPLv2",
		project_urls={
			"Source": f"https://github.com/anamoyee/{PACKAGE_NAME_KEBAB_CASE}",
		},
		classifiers=[
			"Development Status :: 3 - Alpha",
			"Intended Audience :: Developers",
			"Programming Language :: Python :: 3.12",
			"Programming Language :: Python :: 3.13",
			"Programming Language :: Python :: 3 :: Only",
			"Topic :: Utilities",
			"Operating System :: POSIX",
			"Operating System :: POSIX :: Linux",
			"Operating System :: MacOS",
			"Operating System :: Microsoft :: Windows",
			"Operating System :: Microsoft :: MS-DOS",
		],
		python_requires=">=3",
		extras_require=find_all_extras(),
		install_requires=p.Path("./requirements.txt").read_text().strip().split(),
		packages=setuptools.find_packages(),
		include_package_data=True,
	)


VERSION_REGEX = r"__version__\s*=\s*[\"'](.*?)[\"']"


def find_all_extras():
	"""Rummage through ./extras/ and find all dependencies, return them in the correct format for setuptools.setup()."""
	extras_mapping = {}

	for req_file in p.Path("./extras/").glob("requirements-*.txt"):
		extra_name = req_file.stem.removeprefix("requirements-")

		with req_file.open() as f:
			dependencies = [line.strip() for line in f if line.strip()]

		extras_mapping[extra_name] = dependencies

	return extras_mapping


if __name__ == "__main__":
	main()
