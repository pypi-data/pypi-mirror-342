# jsoncons/cli.py
import json
import sys
import argparse
import os

def process_json(infile, outfile, indent=2, sort_keys=False):
    """Reads JSON from infile, validates, and writes formatted JSON to outfile."""
    try:
        data = json.load(infile)
        json.dump(data, outfile, indent=indent, sort_keys=sort_keys)
        outfile.write('\n') # Ensure newline at the end
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during JSON processing: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Validate and format JSON data. Reads from stdin if INFILE is omitted, writes to stdout if OUTFILE is omitted."
    )
    # Using positional arguments for infile/outfile makes it pipe-friendly
    parser.add_argument(
        "infile",
        nargs='?', # Makes it optional
        type=argparse.FileType('r'),
        default=sys.stdin,
        help="Input JSON file (default: stdin)"
    )
    parser.add_argument(
        "outfile",
        nargs='?', # Makes it optional
        type=argparse.FileType('w'),
        default=sys.stdout,
        help="Output JSON file (default: stdout)"
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Indentation level for output JSON (use 0 for compact output, default: 2)"
    )
    parser.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort the keys in the output JSON"
    )
    # Add 'decode' as an alias for 'encode' functionality in this simple tool
    # More complex tools might have distinct encode/decode actions
    # We use subparsers if we add more distinct commands later
    # For now, keeping it simple. If needed:
    # subparsers = parser.add_subparsers(dest="command", help='Sub-command help')
    # parser_encode = subparsers.add_parser('encode', help='Validate and format JSON')
    # ... add args to parser_encode ...

    args = parser.parse_args()

    # Ensure indent is None if 0 is requested for compact output
    output_indent = args.indent if args.indent > 0 else None

    # Guard against reading and writing to the same file (can truncate input)
    # This check is basic and might not cover all edge cases (symlinks, etc.)
    if (args.infile is not sys.stdin and args.outfile is not sys.stdout and
            hasattr(args.infile, 'name') and hasattr(args.outfile, 'name') and
            os.path.abspath(args.infile.name) == os.path.abspath(args.outfile.name)):
        print(f"Error: Input file '{args.infile.name}' and output file '{args.outfile.name}' cannot be the same.", file=sys.stderr)
        sys.exit(1)

    process_json(args.infile, args.outfile, indent=output_indent, sort_keys=args.sort_keys)

if __name__ == "__main__":
    main()