import setuptools

setuptools.setup(
    name="link-quality",
    version="0.0.7",
    author="daoya",
    license="MIT",
    python_requires=">=3.6",
    description="link-quality",
    install_requires=[
        "tldextract",
        "urllib3",
        "aioredis",
        "aiocache",
        "loguru",
        "multipledispatch"
    ],
    py_modules=[
        "spiders.realtime.link_filter",
        "spiders.realtime.normalize",
        "spiders.realtime.rt_logger",
    ],
    classifiers=["Programming Language :: Python :: 3"],
)
