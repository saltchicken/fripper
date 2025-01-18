import argparse
import sys
from .splitter import splitter
from .grabber import grabber

def main():
    parser = argparse.ArgumentParser(description="Frame analysis tool")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand for splitting frames
    split_parser = subparsers.add_parser("split", help="Split frames from a video")
    split_parser.add_argument("video_path", help="Path to the video to split")
    split_parser.add_argument("--nvidia", action="store_true", help="Use NVIDIA hardware acceleration")

    # Subcommand for grabbing frames
    grab_parser = subparsers.add_parser("grab", help="Grab a single frame from a video")
    grab_parser.add_argument("video_path", help="Path to the video")
    grab_parser.add_argument("timestamp", help="Timestamp to extract the frame (format: HH:MM:SS.mmm).")
    grab_parser.add_argument("--nvidia", action="store_true", help="Use NVIDIA hardware acceleration")

    args = parser.parse_args()

    if args.nvidia:
        print("Using NVIDIA acceleration")

    if args.command == "split":
        splitter(args.video_path, nvidia=args.nvidia)
    elif args.command == "grab":
        grabber(args.video_path, args.timestamp, nvidia=args.nvidia)
    else:
        print("Invalid command")
        sys.exit(1)

