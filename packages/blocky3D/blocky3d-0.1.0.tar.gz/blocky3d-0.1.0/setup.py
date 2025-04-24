from setuptools import setup, find_packages

setup(
    name='blocky3D',  # PyPI에 올릴 때 사용할 이름
    version='0.1.0',  # 첫 버전이니까 이렇게!
    description='A fun and easy 3D block-building module for beginners!',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='너의이름',
    author_email='youremail@example.com',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
