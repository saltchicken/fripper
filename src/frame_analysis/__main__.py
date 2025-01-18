import argparse
import sys
from .splitter import splitter
from .ffmpeg_cmd import grab_frame

def main():
    parser = argparse.ArgumentParser(description="Frame analysis tool")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand for splitting frames
    split_parser = subparsers.add_parser("split", help="Split frames from a video")
    split_parser.add_argument("video_path", help="Path to the video to split")
    split_parser.add_argument("--fps", default=4, help="Frames per second to extract")
    split_parser.add_argument("--start", default=None, help="Position in video to start split")
    split_parser.add_argument("--nvidia", action="store_true", help="Use NVIDIA hardware acceleration")

    # Subcommand for grabbing frames
    grab_parser = subparsers.add_parser("grab", help="Grab a single frame from a video")
    grab_parser.add_argument("video_path", help="Path to the video")
    grab_parser.add_argument("timestamp", help="Timestamp to extract the frame (format: HH:MM:SS.mmm).")
    grab_parser.add_argument("--output-path", default=None, help="Output path of extracted frame")

    args = parser.parse_args()


    if args.command == "split":
        if args.nvidia:
            print("Using NVIDIA acceleration")
        splitter(args.video_path, fps=args.fps, start=args.start, nvidia=args.nvidia)
    elif args.command == "grab":
        grab_frame(args.video_path, args.timestamp, args.output_path)
    else:
        print("Invalid command")
        sys.exit(1)

