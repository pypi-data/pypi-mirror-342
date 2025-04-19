# jsoncons/cli.py - v0.3.0 includes encode/decode functionality
import json
import sys
import argparse
import os

# The core logic remains the same: read, validate, format, write.
# Both 'encode' and 'decode' subcommands will use this function.
def process_json(infile, outfile, indent=2, sort_keys=False):
    """Reads JSON from infile, validates, and writes formatted JSON to outfile."""
    try:
        data = json.load(infile)
        json.dump(data, outfile, indent=indent, sort_keys=sort_keys)
        outfile.write('\n') # Ensure newline at the end
    except json.JSONDecodeError as e:
        # Make error message more specific to the input source
        input_source = "stdin" if infile is sys.stdin else f"file '{infile.name}'"
        print(f"Error: Invalid JSON input from {input_source} - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during JSON processing: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Validate and format JSON data using subcommands."
    )

    # --- Subparsers setup ---
    # Use dest='command' to store which subcommand was called
    subparsers = parser.add_subparsers(dest="command", help='Available commands', required=True) # Make command required

    # --- 'encode' Subcommand ---
    parser_encode = subparsers.add_parser(
        'encode',
        help='Validate and pretty-print (encode) JSON data. Reads potentially compact or messy JSON and outputs formatted JSON.'
    )
    parser_encode.add_argument(
        "infile",
        nargs='?', # Makes it optional
        type=argparse.FileType('r'),
        default=sys.stdin,
        help="Input JSON file (default: stdin)"
    )
    parser_encode.add_argument(
        "outfile",
        nargs='?', # Makes it optional
        type=argparse.FileType('w'),
        default=sys.stdout,
        help="Output JSON file (default: stdout)"
    )
    parser_encode.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Indentation level for output JSON (use 0 or less for compact output, default: 2)"
    )
    parser_encode.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort the keys in the output JSON"
    )
    # Point this subcommand to call the process_json function (can be done via set_defaults, but we'll handle in main logic)

    # --- 'decode' Subcommand ---
    # For this tool, decode does the same as encode: reads any JSON, outputs formatted JSON
    # It essentially "decodes" from a string/file stream into a Python object (implicitly via json.load)
    # and then "encodes" back to a formatted string (via json.dump)
    parser_decode = subparsers.add_parser(
        'decode',
        help='Alias for encode. Reads JSON, validates, and outputs formatted JSON.'
    )
    # Add the same arguments as encode
    parser_decode.add_argument(
        "infile",
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help="Input JSON file (default: stdin)"
    )
    parser_decode.add_argument(
        "outfile",
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help="Output JSON file (default: stdout)"
    )
    parser_decode.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Indentation level for output JSON (use 0 or less for compact output, default: 2)"
    )
    parser_decode.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort the keys in the output JSON"
    )

    # --- Parse Arguments ---
    args = parser.parse_args()

    # --- Execute Logic ---
    # Ensure indent is None if 0 or negative is requested for compact output
    output_indent = args.indent if args.indent > 0 else None

    # Guard against reading and writing to the same file
    # This check needs to be done carefully now that args depends on the subcommand
    if (hasattr(args, 'infile') and args.infile is not sys.stdin and
            hasattr(args, 'outfile') and args.outfile is not sys.stdout and
            hasattr(args.infile, 'name') and hasattr(args.outfile, 'name') and
            os.path.abspath(args.infile.name) == os.path.abspath(args.outfile.name)):
        print(f"Error: Input file '{args.infile.name}' and output file '{args.outfile.name}' cannot be the same.", file=sys.stderr)
        sys.exit(1)

    # Call the core processing function regardless of encode/decode command
    # The arguments (infile, outfile, etc.) are correctly parsed based on the subcommand used
    if args.command in ["encode", "decode"]:
        process_json(args.infile, args.outfile, indent=output_indent, sort_keys=args.sort_keys)
    else:
        # Should not happen if subparsers are required=True, but good practice
        print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()