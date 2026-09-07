import os
import json
import ffmpeg


def analyze_video(video_path):
    probe = ffmpeg.probe(video_path)

    format_info = probe.get("format", {})

    video_stream = None
    audio_stream = None

    for stream in probe.get("streams", []):
        if stream["codec_type"] == "video" and video_stream is None:
            video_stream = stream

        elif stream["codec_type"] == "audio" and audio_stream is None:
            audio_stream = stream

    report = {
        "file_name": os.path.basename(video_path),
        "file_size_bytes": os.path.getsize(video_path),

        "container": format_info.get("format_name"),
        "duration": format_info.get("duration"),

        "video": {
            "resolution": None,
            "frame_rate": None,
            "bit_rate": None,
            "codec": None
        },

        "audio": {
            "codec": None,
            "channels": None,
            "sampling_rate": None,
            "bit_rate": None
        },

        "metadata": format_info.get("tags", {})
    }

    if video_stream:
        width = video_stream.get("width")
        height = video_stream.get("height")

        report["video"]["resolution"] = f"{width}x{height}"

        frame_rate = video_stream.get("r_frame_rate")

        if frame_rate and frame_rate != "0/0":
            numerator, denominator = map(int, frame_rate.split("/"))
            report["video"]["frame_rate"] = round(
                numerator / denominator, 2
            )

        report["video"]["bit_rate"] = video_stream.get("bit_rate")
        report["video"]["codec"] = video_stream.get("codec_name")

    if audio_stream:
        report["audio"]["codec"] = audio_stream.get("codec_name")
        report["audio"]["channels"] = audio_stream.get("channels")
        report["audio"]["sampling_rate"] = audio_stream.get("sample_rate")
        report["audio"]["bit_rate"] = audio_stream.get("bit_rate")

    return report


def print_report(report):
    print("================================")
    print(" VIDEO METADATA REPORT")
    print("================================")

    print("File Name       :", report["file_name"])
    print("File Size       :", report["file_size_bytes"], "bytes")
    print("Container       :", report["container"])
    print("Duration        :", report["duration"], "seconds")

    print("\nVIDEO")
    print("--------------------------------")

    print("Resolution      :", report["video"]["resolution"])
    print("Frame Rate      :", report["video"]["frame_rate"], "FPS")
    print("Bit Rate        :", report["video"]["bit_rate"])
    print("Codec           :", report["video"]["codec"])

    print("\nAUDIO")
    print("--------------------------------")

    print("Codec           :", report["audio"]["codec"])
    print("Channels        :", report["audio"]["channels"])
    print("Sampling Rate   :", report["audio"]["sampling_rate"], "Hz")
    print("Bit Rate        :", report["audio"]["bit_rate"])

    print("\nMETADATA")
    print("--------------------------------")

    if report["metadata"]:
        for key, value in report["metadata"].items():
            print(f"{key}: {value}")
    else:
        print("No metadata found.")


if __name__ == "__main__":
    video_path = "samples/video.mp4"

    try:
        result = analyze_video(video_path)
        print_report(result)

    except FileNotFoundError:
        print("Error: Video file not found.")

    except ffmpeg.Error as e:
        print("Error while analyzing video:")
        print(e.stderr.decode() if e.stderr else "Unknown FFmpeg error.")

    except Exception as e:
        print("Error:", e)