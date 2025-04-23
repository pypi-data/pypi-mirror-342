from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='NDL-MITB',
    version='0.5.0',
    description='All codes for NDL labs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Vedant Raikar',
    author_email='vedantraikar117@gmail.com',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0.0',
        'numpy',
        'matplotlib',
        'opencv-python',
        'scikit-learn',
        'seaborn',
        'scipy',
        'pandas',
        'keras',
        'torch',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
)
