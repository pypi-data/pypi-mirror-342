from setuptools import setup, find_packages

setup(
    name="ai-security-toolkit",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tensorflow",
        "matplotlib",
        "numpy",
        "pandas",
        "cleverhans"
    ],
    entry_points={
        'console_scripts': [
            'ai-toolkit=ai_toolkit.run:main'
        ]
    },
    author="Neha",
    description="AI Red Team Toolkit with adversarial attacks, model stealing, inversion, and more.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
)
