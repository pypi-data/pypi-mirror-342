from setuptools import setup, find_packages

setup(
    name="floorplan-epc-detector",  # Changed package name
    version="1.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "onnxruntime>=1.12.0",
        "numpy>=1.19.0",
        "requests>=2.25.0",
        "Pillow>=10.0.0"
    ],
    author="Oliver Brown",
    description="A package for making predictions using a custom-trained ONNX floorplan/epc/proprty_image model",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Resipedia/domusview_epc_floorplan_image_detection",
    project_urls={
        "Bug Tracker": "https://github.com/Resipedia/domusview_epc_floorplan_image_detection/issues",
        "Source": "https://github.com/Resipedia/domusview_epc_floorplan_image_detection",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.7",
)