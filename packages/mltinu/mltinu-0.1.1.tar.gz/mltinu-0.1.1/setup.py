from setuptools import setup, find_packages

setup(
    name='mltinu',  
    version='0.1.1',
    description='Generate end‑to‑end ML pipeline code via TINU AI',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Tinu',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/mltinu',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0',
        'langchain_openai>=0.1',  # or the exact package name/version you’re using
    ],
    entry_points={
        'console_scripts': [
            'mltinu = mltinu.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
