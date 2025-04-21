from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='Weather_API_MASI',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'selenium>=4.28.1',
        'geopy>=2.4.1',
        'webdriver_manager>=4.0.2',
        'argparse',
        'python-dotenv>=0.19.0',
        'beautifulsoup4>=0.0.2',
        'pandas>=2.2.3',
        'seaborn>=0.13.2',
        'matplotlib>=3.10.1',
    ],
    entry_points={
        "console_scripts": ["Weather-API-MASI = Weather_API_MASI.run_weather_tool:main"]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
