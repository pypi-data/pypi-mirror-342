from setuptools import setup

from setuptools_rust import RustExtension


setup(
    name="pyawabi",
    version="0.3.0",
    description='A morphological analyzer using mecab dictionary.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url='http://github.com/nakagami/pyawabi/',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Rust",
        "Operating System :: POSIX",
    ],
    keywords=['MeCab'],
    license='MIT',
    author='Hajime Nakagami',
    author_email='nakagami@gmail.com',
    packages=["pyawabi"],
    scripts=['bin/pyawabi'],
    rust_extensions=[RustExtension("pyawabi.awabi")],
    zip_safe=False,
    test_suiete="tests",
)
