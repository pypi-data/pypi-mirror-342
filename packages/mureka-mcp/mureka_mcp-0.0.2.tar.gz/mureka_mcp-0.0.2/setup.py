from setuptools import setup, find_packages

setup(
    name='mureka-mcp',
    version='0.0.2',
    packages=find_packages(exclude=["test_api.py"]),
    include_package_data=True,
    install_requires=[
        "mcp>=1.6.0",
    ],
    author='wei.zhang',
    author_email='zhangwei@singularity-ai.com',
    description='The mcp server of Mureka.ai ',
    license='MIT',
    keywords='ai generate music mureka mcp',
    #url='https://github.com/yourusername/mypackage',
    python_requires='>=3.10',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
