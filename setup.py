from setuptools import setup, find_packages


VERSION = "2.5.2"


def readme():
    with open("README.rst", encoding="utf-8") as f:
        return f.read()


setup(
    name="text2num",
    version=VERSION,
    description="Parse and convert numbers written in French, Spanish, English, Portuguese, German, Catalan or Russion into their digit representation.",
    long_description=readme(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: Filters",
        "Natural Language :: French",
        "Natural Language :: English",
        "Natural Language :: Spanish",
        "Natural Language :: Portuguese",
        "Natural Language :: German",
        "Natural Language :: Catalan",
        "Natural Language :: Russian"
    ],
    keywords="French Spanish English Portuguese German Catalan Russion NLP words-to-numbers",
    url="https://github.com/allo-media/text2num",
    author="Allo-Media",
    author_email="contact@allo-media.fr",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    test_suite="tests",
    include_package_data=True,
    zip_safe=False,
)
