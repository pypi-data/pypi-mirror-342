from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11

ext_modules = [
    Extension(
        "textcpp.text_utils",
        [
            "src/textcpp/text_utils/bindings_text_utils.cpp",
            "src/textcpp/text_utils/count_words.cpp",
            "src/textcpp/text_utils/frequency_count.cpp",
            "src/textcpp/text_utils/word_frequency_count.cpp",
        ],
        include_dirs=[pybind11.get_include(), "src/textcpp"],
        language="c++",
    ),
    Extension(
        "textcpp.others",
        [
            "src/textcpp/others/bindings_others.cpp",
            "src/textcpp/others/add.cpp",
            "src/textcpp/others/sub.cpp",
        ],
        include_dirs=[pybind11.get_include(), "src/textcpp"],
        language="c++",
    ),
    Extension(
        "textcpp.preprocessing",
        [
            "src/textcpp/preprocessing/bindings_preprocessing.cpp",
            "src/textcpp/preprocessing/extract_ngrams.cpp",
        ],
        include_dirs=[pybind11.get_include(), "src/textcpp"],
        language="c++",
    ),
]

setup(
    name="textcpp",
    version="0.0.9",
    author="PierPierPy",
    description="package utils for textual analysis in C++",
    packages=["textcpp"],
    package_dir={"": "src"},
    package_data={"textcpp": ["**/*.h"]},
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=["pybind11>=2.6"],
)
