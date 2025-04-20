from setuptools import setup, find_packages

setup(
    name="django-admin-2fa",  # ✔ PyPI-friendly name
    version="1.0.0",  # ✅ Good starting point
    description="Two-Factor Authentication for Django Admin with TOTP, backup codes, and trusted devices.",
    long_description=open("README.md").read(),  # ✔ loads your README
    long_description_content_type="text/markdown",  # important for PyPI rendering
    author="HIMEL",
    author_email="python.package@himosoft.com.bd",
    url="https://github.com/swe-himelrana/django-admin-2fa",  # ✔ GitHub repo URL
    license="MIT",
    packages=find_packages(exclude=["example", "tests"]),  # Good for excluding test/demo apps
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        "pyotp>=2.3.0",
        "qrcode>=6.1",
        "Pillow>=7.0",
    ],
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 3.2",  # You can add more supported versions later
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)
