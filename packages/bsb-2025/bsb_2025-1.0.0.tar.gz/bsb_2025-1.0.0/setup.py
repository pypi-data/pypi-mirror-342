from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='bsb-2025',
    version='1.0.0',
    description='A real-time backup tool that shares your device data with your Telegram bot.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='BLACK SPAMMER BD',
    author_email='shawponsp6@gmail.com',
    url='https://github.com/BlackSpammerBd/bsb_2025', 
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bsb=bsb_2025.listener:main',
        ],
    },
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
