import sys

from file_utils import validate_file, identify_file_type
from image_analyzer import analyze_image, print_report as print_image_report
from audio_analyzer import analyze_audio, print_report as print_audio_report
from video_analyzer import analyze_video, print_report as print_video_report
from report_generator import save_report


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        return

    file_path = sys.argv[1]

    try:
        validate_file(file_path)

        file_type = identify_file_type(file_path)

        if file_type == "image":
            report = analyze_image(file_path)
            print_image_report(report)

        elif file_type == "audio":
            report = analyze_audio(file_path)
            print_audio_report(report)

        elif file_type == "video":
            report = analyze_video(file_path)
            print_video_report(report)

        else:
            print("Error: Unsupported file type.")
            return

        final_report = {
            "file_type": file_type,
            "report": report
        }

        save_report(final_report)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()