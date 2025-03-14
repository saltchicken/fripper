import argparse
import sys
from .splitter import VideoSplitter
from .preview import preview_frame, preview_thumbnails
from .ffmpeg_cmd import grab_frame, grab_thumbnails

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
    grab_parser.add_argument("--timestamp", default="00:00:00.000", help="Timestamp to extract the frame (format: HH:MM:SS.mmm).")
    grab_parser.add_argument("--output-path", default=None, help="Output path of extracted frame")
    grab_parser.add_argument("--thumbnails", action="store_true", help="Grab thumbnails")

    preview_parser = subparsers.add_parser("preview", help="Preview a single frame of a video")
    preview_parser.add_argument("video_path", help="Path to the video")
    preview_parser.add_argument("--timestamp", default="00:00:00.000", help="Timestamp to extract the frame (format: HH:MM:SS.mmm).")
    preview_parser.add_argument("--thumbnails", action="store_true", help="Display thumbnails")

    args = parser.parse_args()


    if args.command == "split":
        if args.nvidia:
            print("Using NVIDIA acceleration")
        splitter = VideoSplitter(args.video_path, fps=args.fps, start=args.start, nvidia=args.nvidia)
        splitter.setup()
        splitter.run()
    elif args.command == "grab":
        if args.thumbnails:
            grab_thumbnails(args.video_path)
        else:
            grab_frame(args.video_path, args.timestamp, args.output_path)
    elif args.command == "preview":
        if args.thumbnails:
            preview_thumbnails(args.video_path)
        else:
            preview_frame(args.video_path, args.timestamp)
    else:
        print("Invalid command")
        sys.exit(1)

