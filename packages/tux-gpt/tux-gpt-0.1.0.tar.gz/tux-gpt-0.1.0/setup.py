from setuptools import setup, find_packages

setup(
    name="tux-gpt",
    version="0.1.0",
    description="An interactive terminal tool using GPT",
    author="Fábio Berbert de Paula",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'openai>=0.27.0',
        'rich>=10.0.0'
    ],
    extras_require={
        'dev': [
            'pytest',
            'mypy',
            'flake8',
        ],
    },
    entry_points={
        'console_scripts': [
            'tux-gpt=terminal_gpt.terminal_gpt:main'
        ]
    }
)

