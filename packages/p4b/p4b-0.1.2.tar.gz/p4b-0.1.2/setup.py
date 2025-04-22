from setuptools import setup, find_packages

setup(
    name="p4b",
    version="0.1.2",
    description="god bless you",
    python_requires=">=3.11",
    packages=find_packages(),
    install_requires=[
        "cython",
        "google-generativeai",
        "keyboard",
        "pillow",
        "pyarmor",
        "pyautogui",
        "pygame",
        "pyperclip",
        "setuptools",
        # "cython>=3.0.12",
        # "google-generativeai>=0.8.5",
        # "keyboard>=0.13.5",
        # "pillow>=11.2.1",
        # "pyarmor>=9.1.4",
        # "pyautogui>=0.9.54",
        # "pygame>=2.6.1",
        # "pyperclip>=1.9.0",
        # "setuptools>=78.1.1",
    ],
    entry_points={
        "console_scripts": [
            "p4b=p4b:main",
        ],
    },
    package_data={
        "p4b": ["*.pyd", "*.py"],
        "p4b.pyarmor_runtime_000000": ["*.pyd", "*.py"],
    },
    include_package_data=True,
    zip_safe=False,
)