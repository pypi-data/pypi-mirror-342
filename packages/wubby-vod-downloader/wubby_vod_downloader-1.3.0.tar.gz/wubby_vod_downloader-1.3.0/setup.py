from setuptools import setup, find_packages

setup(
    name='wubby_vod_downloader',
    version='1.3.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tqdm',
    ],
    entry_points={
    'console_scripts': [
        'wubby-snatch=vod_downloader.vod_downloader:main',
    ],
},
    include_package_data=True,
    # package_data is typically for static files you want bundled with your package
    # if vod_downloads is your download folder, you might want to exclude it from package_data
    # You can use a MANIFEST.in file to handle specific packaging of files or assets.
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
