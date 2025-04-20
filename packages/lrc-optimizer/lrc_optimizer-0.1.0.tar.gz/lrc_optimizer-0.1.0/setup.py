from setuptools import setup, find_packages
setup(
    name='lrc-optimizer',
    version='0.1.0',
    author='Your Name',
    author_email='you@example.com',
    description='Learning Rate of Change (LRC) tracking for PyTorch models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/lrc-optimizer',
    project_urls={'Source': 'https://github.com/yourusername/lrc-optimizer'},
    license='MIT',
    packages=find_packages(),
    install_requires=['torch'],
    python_requires='>=3.6',
)
