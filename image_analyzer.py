from PIL import Image
from PIL.ExifTags import TAGS
import os


def analyze_image(image_path):
    image = Image.open(image_path)

    # Extract EXIF metadata
    exif_data = {}
    exif = image.getexif()

    for tag_id, value in exif.items():
        tag_name = TAGS.get(tag_id, tag_id)
        exif_data[tag_name] = str(value)

    # Create report
    report = {
        "file_name": os.path.basename(image_path),
        "file_size_bytes": os.path.getsize(image_path),
        "format": image.format,
        "width": image.width,
        "height": image.height,
        "color_mode": image.mode,
        "metadata": exif_data
    }

    return report


def print_report(report):
    print("================================")
    print(" IMAGE METADATA REPORT")
    print("================================")

    print("File Name   :", report["file_name"])
    print("File Size   :", report["file_size_bytes"], "bytes")
    print("Format      :", report["format"])
    print("Resolution  :", report["width"], "x", report["height"])
    print("Color Mode  :", report["color_mode"])

    print("\nMETADATA")
    print("--------------------------------")

    if report["metadata"]:
        for key, value in report["metadata"].items():
            print(f"{key}: {value}")
    else:
        print("No EXIF metadata found.")


# Test
image_path = "samples/image.jpg"

try:
    result = analyze_image(image_path)
    print_report(result)
except FileNotFoundError:
    print("Error: Image file not found.")
except Exception as e:
    print("Error:", e)