from mutagen import File
import os


def analyze_audio(audio_path):
    audio = File(audio_path)

    if audio is None:
        raise ValueError("Unsupported or invalid audio file.")

    info = audio.info

    report = {
        "file_name": os.path.basename(audio_path),
        "file_size_bytes": os.path.getsize(audio_path),
        "format": os.path.splitext(audio_path)[1].replace(".", "").upper(),
        "duration_seconds": getattr(info, "length", None),
        "bit_rate": getattr(info, "bitrate", None),
        "channels": getattr(info, "channels", None),
        "sampling_rate": getattr(info, "sample_rate", None),
        "metadata": {}
    }

    if audio.tags:
        for key, value in audio.tags.items():
            report["metadata"][str(key)] = str(value)

    return report


def print_report(report):
    print("================================")
    print(" AUDIO METADATA REPORT")
    print("================================")

    print("File Name       :", report["file_name"])
    print("File Size       :", report["file_size_bytes"], "bytes")
    print("Format          :", report["format"])
    print("Duration        :", report["duration_seconds"], "seconds")
    print("Bit Rate        :", report["bit_rate"], "bps")
    print("Channels        :", report["channels"])
    print("Sampling Rate   :", report["sampling_rate"], "Hz")

    print("\nMETADATA")
    print("--------------------------------")

    if report["metadata"]:
        for key, value in report["metadata"].items():
            print(f"{key}: {value}")
    else:
        print("No metadata found.")


audio_path = "samples/song.mpeg"

try:
    result = analyze_audio(audio_path)
    print_report(result)
except FileNotFoundError:
    print("Error: Audio file not found.")
except Exception as e:
    print("Error:", e)