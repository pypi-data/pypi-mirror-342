from setuptools import setup
setup(
    name="simple-dh",
    version="0.1",
    description="Simple Animation Maker",
    author="None1",
    py_modules=["dh"],
    keywords=["animation"],
    install_requires=["opencv-python","imageio"],
    url="https://github.com/none-None1/simple_dh",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown"
)
