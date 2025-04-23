from setuptools import setup, find_packages

setup(
    name="yolo_inference",
    version="2.0.0",
    description="A YOLO-based inference library for object detection, providing easy-to-use APIs for loading models and performing inference on images.",
    long_description="""
        yolo_inference is a Python library designed for object detection tasks using YOLO models. 
        It simplifies the process of loading pre-trained YOLO models and running inference on images. 
        The library is lightweight and easy to integrate into existing projects.

        Example Usage:
        ----------------
        from yolo_inference.detect import ObjectDetection

        # Initialize the model
        model = ObjectDetection(model_path="path/to/yolo_model.pt")

        # Perform inference on an image
        result = model.inference(image="path/to/image.jpg")

        # Process the result
        print(result)
    """,
    long_description_content_type="text/plain",
    author="Shubham Nayak",
    author_email="sn85076@outlook.com",
    packages=find_packages(),
    install_requires=[
        "torch",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)