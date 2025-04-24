from setuptools import setup, find_packages

setup(
    name="create-tg-bot",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "jinja2"
    ],
    entry_points={
        "console_scripts": [
            "create-tg-bot=create_tg_bot.main:main",
        ],
    },
)
