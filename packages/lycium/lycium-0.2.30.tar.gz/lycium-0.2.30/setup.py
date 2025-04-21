import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="lycium",
    version="0.2.30",
    author="kevinyjn",
    author_email="kevinyjn@foxmail.com",
    description="Common python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/starview/lycium",
    packages=setuptools.find_packages(exclude=[".tests", ".tests.", "tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pycrypto",
        "blinker",
        "pika",
        "redis",
        "gunicorn",
        "mongoengine",
        "elasticsearch==7.12.0",
        "sqlalchemy==1.4.25",
        "sshtunnel",
        "Cython",
        "IPy",
        "requests",
        "tornado",
        "zeep[async]",
        "motor",
        "aredis",
        "pyopenssl",
        "rsa",
        "cx_Oracle",
        "asyncpg",
        "aiomysql",
        "aiosqlite",
        "pymssql",
        "protobuf==3.14.0",
        "confluent-kafka",
        "PyJWT",
        "pymongo==3.12.1"
    ]
)
