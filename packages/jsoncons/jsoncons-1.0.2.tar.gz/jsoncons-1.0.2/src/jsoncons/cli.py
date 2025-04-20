# jsoncons/cli.py - v0.3.0 includes encode/decode functionality
import json
import sys
import argparse
import os
import logging
import decimal

# (Add this near the top of cli.py or in a separate helper file)


class CobolParsingError(ValueError):
    """Custom error for COBOL parsing issues."""
    pass

def parse_cobol_line(line, layout_config, line_num):
    """Parses a single line of fixed-width data based on the layout."""
    record = {}
    expected_len = layout_config.get("record_length")
    if expected_len and len(line.rstrip('\n\r')) != expected_len:
        logging.warning(f"Line {line_num}: Expected length {expected_len}, got {len(line.rstrip('\n\r'))}. Processing anyway.")
        # Decide if you want to raise an error here instead:
        # raise CobolParsingError(f"Line {line_num}: Expected length {expected_len}, got {len(line.rstrip('\n\r'))}")


    for field in layout_config.get("fields", []):
        name = field["name"]
        # Adjust start_pos to be 0-based index for Python slicing
        start_index = field["start_pos"] - 1
        length = field["length"]
        end_index = start_index + length
        cobol_type = field.get("type", "PIC X").upper()
        should_strip = field.get("strip", False)
        implied_decimals = field.get("decimals", 0)
        is_signed = field.get("signed", False)

        # Slice the data, handle potential short lines gracefully
        raw_value = line[start_index:end_index] if start_index < len(line) else ""
        # Pad if the slice was shorter than expected (due to short line)
        raw_value = raw_value.ljust(length)


        processed_value = None

        try:
            if cobol_type == "PIC X":
                processed_value = raw_value
                if should_strip:
                    processed_value = processed_value.strip()
            elif cobol_type == "PIC 9":
                if not raw_value.strip(): # Handle empty numeric fields
                    processed_value = None
                elif implied_decimals > 0:
                    # Insert decimal point
                    decimal_str = raw_value[:-implied_decimals] + "." + raw_value[-implied_decimals:]
                    processed_value = decimal.Decimal(decimal_str)
                else:
                    processed_value = int(raw_value)
            elif cobol_type == "PIC S9":
                 if not raw_value.strip(): # Handle empty numeric fields
                    processed_value = None
                 else:
                    num_str = raw_value
                    sign = '+' # Default sign
                    # Basic sign handling (assumes sign is overpunched or leading/trailing)
                    # This is a SIMPLIFICATION. Real COBOL has many sign conventions.
                    # Assuming trailing sign for simplicity here.
                    if is_signed:
                        # Example: Very simple trailing sign check - adjust as needed
                        if raw_value.endswith(('-', '}', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R')):
                             sign = '-'
                             num_str = raw_value[:-1] # Remove sign character if trailing
                        elif raw_value.endswith(('+', '{', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')):
                             sign = '+'
                             num_str = raw_value[:-1] # Remove sign character if trailing
                        elif raw_value.startswith('-'):
                            sign = '-'
                            num_str = raw_value[1:]
                        elif raw_value.startswith('+'):
                            sign = '+'
                            num_str = raw_value[1:]

                    if implied_decimals > 0:
                         # Ensure num_str has enough digits before inserting decimal
                        if len(num_str) >= implied_decimals:
                             decimal_str = num_str[:-implied_decimals] + "." + num_str[-implied_decimals:]
                        else: # Handle cases like '50' for PIC S9(2)V99 -> 0.50
                            decimal_str = "0." + num_str.zfill(implied_decimals)

                        # Combine sign and number
                        full_decimal_str = sign + decimal_str.lstrip('0') # Avoid things like '+0.50' -> keep '+.50' by lstrip? Better: Decimal handles this
                        processed_value = decimal.Decimal(sign + decimal_str)

                    else:
                        processed_value = int(sign + num_str)

            # Add more types here if needed (COMP-3 is complex)

            else:
                 logging.warning(f"Line {line_num}, Field '{name}': Unsupported COBOL type '{cobol_type}'. Treating as string.")
                 processed_value = raw_value
                 if should_strip:
                     processed_value = processed_value.strip()

            record[name] = processed_value

        except (ValueError, decimal.InvalidOperation) as e:
             raise CobolParsingError(
                 f"Line {line_num}, Field '{name}': Error converting value '{raw_value}' "
                 f"using type '{cobol_type}' (Decimals: {implied_decimals}, Signed: {is_signed}). Original error: {e}"
             ) from e

    return record

def process_cobol_to_json(layout_file, infile, outfile):
    """Loads layout, reads COBOL data, parses lines, and writes JSON."""
    try:
        with open(layout_file, 'r', encoding='utf-8') as f_layout:
            layout_config = json.load(f_layout)
    except FileNotFoundError:
        logging.error(f"Layout file not found: {layout_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON layout file '{layout_file}': {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading layout file '{layout_file}': {e}", exc_info=True)
        sys.exit(1)

    records = []
    line_num = 0
    try:
        for line in infile:
            line_num += 1
            # Skip empty lines
            if not line.strip():
                continue
            try:
                record = parse_cobol_line(line, layout_config, line_num)
                records.append(record)
            except CobolParsingError as e:
                logging.error(str(e)) # Log parsing error for the specific line
                # Optionally decide whether to skip the line or exit entirely
                # sys.exit(1) # Uncomment to make it fatal
                logging.warning(f"Skipping line {line_num} due to parsing error.")

        # Use Decimal encoder for output
        class DecimalEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, decimal.Decimal):
                    # Convert Decimal to string to preserve precision
                    # Or convert to float: float(obj), but risk precision loss
                    return str(obj)
                # Let the base class default method raise the TypeError
                return super(DecimalEncoder, self).default(obj)

        json.dump(records, outfile, indent=2, cls=DecimalEncoder) # Use indent=2 for pretty print
        outfile.write('\n')
        if outfile is not sys.stdout:
            logging.info(f"Successfully converted COBOL data to JSON in {outfile.name}")

    except FileNotFoundError:
        # This is already handled by argparse FileType, but as fallback
        logging.error(f"Input data file not found: {infile.name}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred during COBOL data processing: {e}", exc_info=True)
        sys.exit(1)

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

# --- Main CLI Logic ---
def main():
    # Set up basic logging to stderr
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stderr)
    # To make errors more visible:
    # logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s', stream=sys.stderr)


    parser = argparse.ArgumentParser(
        prog="jsoncons",
        description="Validate/format JSON or convert fixed-width COBOL data to JSON."
    )

    # --- Subparsers setup ---
    subparsers = parser.add_subparsers(
        title='Available Commands',
        dest="command",
        help='Use a command to process data.',
        required=True
    )

    # --- Define arguments shared between encode & decode ---
    common_parser_json = argparse.ArgumentParser(add_help=False)
    common_parser_json.add_argument(
        "infile", nargs='?', type=argparse.FileType('r', encoding='utf-8'),
        default=sys.stdin, help="Input JSON file (reads from stdin if omitted)"
    )
    common_parser_json.add_argument(
        "outfile", nargs='?', type=argparse.FileType('w', encoding='utf-8'),
        default=sys.stdout, help="Output JSON file (writes to stdout if omitted)"
    )
    common_parser_json.add_argument(
        "--indent", type=int, default=2,
        help="Indentation level for output JSON (use 0 or less for compact, default: 2)"
    )
    common_parser_json.add_argument(
        "--sort-keys", action="store_true", help="Sort the keys in the output JSON"
    )

    # --- 'encode' Subcommand ---
    parser_encode = subparsers.add_parser(
        'encode',
        help='Validate and pretty-print (encode) JSON data.',
        parents=[common_parser_json]
    )

    # --- 'decode' Subcommand ---
    parser_decode = subparsers.add_parser(
        'decode',
        help='Alias for encode. Reads JSON, validates, and outputs formatted JSON.',
        parents=[common_parser_json]
    )

    # --- 'cobol_to_json' Subcommand ---
    parser_c2j = subparsers.add_parser(
        'cobol_to_json',
        help='Convert fixed-width COBOL data file to JSON using a layout file.'
    )
    parser_c2j.add_argument(
        "--layout-file",
        metavar='LAYOUT_JSON',
        required=True,
        help="Path to the JSON file describing the COBOL record layout."
    )
    parser_c2j.add_argument(
        "infile",
        # Note: Not defaulting to stdin here, usually COBOL data comes from specific files
        type=argparse.FileType('r', encoding='utf-8'), # Or 'latin-1' / 'cp037' etc. if EBCDIC
        help="Input fixed-width COBOL data file."
    )
    parser_c2j.add_argument(
        "outfile",
        nargs='?', # Make output file optional, defaulting to stdout
        type=argparse.FileType('w', encoding='utf-8'),
        default=sys.stdout,
        help="Output JSON file (writes to stdout if omitted)."
    )

    # --- Parse Arguments ---
    try:
        args = parser.parse_args()
    except Exception as e:
        logging.error(f"Error parsing arguments: {e}")
        parser.print_help(sys.stderr)
        sys.exit(2)

    # --- Execute Logic based on command ---

    # Guard against reading and writing to the same file (can corrupt input)
    # Check needs to be conditional on args existing
    if hasattr(args, 'infile') and hasattr(args, 'outfile'):
         if (args.infile is not sys.stdin and args.outfile is not sys.stdout and
             hasattr(args.infile, 'name') and hasattr(args.outfile, 'name') and
             os.path.abspath(args.infile.name) == os.path.abspath(args.outfile.name)):
            logging.error(f"Input file '{args.infile.name}' and output file '{args.outfile.name}' cannot be the same.")
            sys.exit(1)

    # Call the appropriate function based on the command
    if args.command in ["encode", "decode"]:
        output_indent = args.indent if args.indent > 0 else None
        process_json(args.infile, args.outfile, indent=output_indent, sort_keys=args.sort_keys)
    elif args.command == "cobol_to_json":
        process_cobol_to_json(args.layout_file, args.infile, args.outfile)
    else:
        # Should not happen if subparsers are required=True
        logging.error(f"Error: Unknown command '{args.command}' encountered.")
        parser.print_help(sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()