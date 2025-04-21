from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='carrier_integrations1', 
    version='0.1.3',
    packages=find_packages(include=["carriers", "carriers.*"]),
    install_requires=[
        'blinker==1.8.2',
        'boto==2.49.0',
        'certifi==2024.8.30',
        'charset-normalizer==3.4.0',
        'click==8.1.7',
        'colorama==0.4.6',
        'python-dateutil',
        'dnspython==2.6.1',
        'Flask==3.0.3',
        'idna==3.10',
        'importlib_metadata==8.5.0',
        'itsdangerous==2.2.0',
        'Jinja2==3.1.5',
        'MarkupSafe==2.1.5',
        'pdfkit==1.0.0',
        'pymongo==4.10.1',
        'pypdf==5.1.0',
        'pytz==2024.2',
        'PyYAML==6.0.2',
        'requests==2.32.3',
        'strgen==1.3.1',
        'typing_extensions==4.12.2',
        'urllib3==2.2.3',
        'Werkzeug==3.0.6',
        'zipp==3.20.2',
        'curlify'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
)
