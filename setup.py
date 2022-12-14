from setuptools import setup, find_packages

setup(
    name="captcha.rip-api",
    version="1.2",
    license="no-license",
    author="chaarlottte",
    #author_email="email@example.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/chaarlottte/captcha.rip-python",
    keywords="captcha funcaptcha captcha.rip roblox",
    install_requires=[
        "requests",
        "colorama",
    ],
)
