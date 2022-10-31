import sys
if sys.version_info < (3,):
    print('Python 2 is not supported by CVD-risk-scores.')
    sys.exit(-1)
if sys.platform == 'win32' and sys.maxsize.bit_length() == 31:
    print('32-bit Windows Python runtime is not supported. Please switch to 64-bit Python.')
    sys.exit(-1)

import pathlib
import traceback
import logging
import platform
from setuptools import setup, find_packages

# make sure python system version is at leaast 3.7.2
python_min_v = (3, 7, 2)
python_min_v_str = '.'.join(map(str, python_min_v))
if sys.version_info < python_min_v:
    logging.error("Python version required is at least {}. Currently you have {}.".format(python_min_v_str, platform.python_version()))

# determine semantic release version
DIR = pathlib.Path(__file__).parent
SOURCE_DIR = "src"
PROJECT_NAME = "cvd_risk_scores"

def main():
    long_description = (DIR / 'README.md').read_text()

    try:
        changelog = (DIR / 'CHANGELOG.md').read_text()
        __version__, *_ = re.findall(r"\[([0-9.]+)]", changelog)
    except (FileNotFoundError, ValueError) as ex:
        __version__ = '1.0.2'
        logging.error(ex)
        logging.error(traceback.print_exc())
        logging.warning(f'Unable to get semantic release version. Setting version to {__version__}.')

    setup(
        name=PROJECT_NAME,
        version=__version__,
        description='A Python package for computing cardiovascular disease risk using clinically validated models.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='francesco-pisu',
        author_email='fra.pisu1@gmail.com',
        url='https://github.com/francescopisu/CVD-risk-scores',
        license='MIT',
        python_requires='>=3.7,<3.10',
        install_requires=[
            'numpy>=1.0.0,<2.0.0',
            'pandas>=1.0.0,<2.0.0',
            'typing-extensions>=3.0.0,<10.0.0',
            'pydantic>=1.0.0,<10.0.0'
        ],
        package_dir={f'{PROJECT_NAME}': f'{SOURCE_DIR}/{PROJECT_NAME}'},
        packages=find_packages(where=f'{SOURCE_DIR}', exclude=['tests']),
        # package_data={f'{PROJECT_NAME}': ['data/*.json']},
        include_package_data=True,
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Medical Science Apps.',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ]
    )        


if __name__ == "__main__":
    main()