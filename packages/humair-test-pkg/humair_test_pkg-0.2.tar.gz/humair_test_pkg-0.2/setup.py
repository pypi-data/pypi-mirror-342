import os
import re
from typing import List

import setuptools


def get_requirements(requirements_file: str) -> List[str]:
    """Read requirements from requirements.in."""

    file_path = os.path.join(os.path.dirname(__file__), requirements_file)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if not line.startswith('#') and line]
    return lines


def read_readme() -> str:
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path) as f:
        return f.read()
setuptools.setup(
    name='humair_test_pkg',
    version='v0.2',
    description='Kubeflow Pipelines SDK',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='The Kubeflow Authors',
    url='https://github.com/kubeflow/pipelines',
    project_urls={
        'Source':
            'https://github.com/kubeflow/pipelines/tree/master/sdk',
    },
    install_requires=get_requirements('requirements.in'),
    packages=setuptools.find_packages(exclude=['*test*']),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
    ],
    python_requires='>=3.7.0,<3.13.0',
    include_package_data=True,
)
