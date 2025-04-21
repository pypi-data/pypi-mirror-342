

## 🐍 The `jsoncons` Package 🐛❇️🐉 
## 🚙🦖 COBOL-to-JSON CLI Utility in Python 🦕🐍

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![PyPI version](https://badge.fury.io/py/jsoncons.svg)](https://badge.fury.io/py/jsoncons)



The `jsoncons` package is designed to provide a basic command-line interface for handling JSON data. This can be useful for simple scripting or interoperability tasks (e.g., having a COBOL program generate a text file that this tool converts to JSON, or vice versa). 
COBOL-to-JSON parsing features were added in v1.0.0 and will be extended in future versions of ``jsoncons``.

### **Installation:**

```bash
pip install jsoncons
```

### **Basic Usage for Pretty-Print JSON:**
*   **Create Input File If Necessary:** In your project directory, verify there is a file named 
    input.json with the following content:
    ```bash
    {"key":"value", "items":[1,2]}
    ```

*   **Validate & Pretty-print JSON:** Read from stdin, write to stdout. (Linux Command)
    ```bash
    echo '{"key":"value", "items":[1,2]}' | jsoncons encode
    ```
    **Windows Powershell Command:** Read from stdin, write to stdout.
    ```bash
    echo {"\"key\"":"\"value\"", "\"items\"":[1,2]} | jsoncons encode
    ```

*   **Validate & Pretty-print JSON from file to file:** (Tested on Windows 10)
    ```bash
    jsoncons encode input.json output_pretty.json
    ```
*   *(The `decode` command might be an alias or offer slightly different formatting if needed)*

## **Tested Release ``jsoncons``v1.0.4**
### Bug Fixed: f-string Issue in ``COBOL-to-JSON`` function
-  Jupyter Notebook Tutorial
-  COBOL-to-JSON function tested in 3.11.1,3.11.2, 3.12.1
-  Compatibility expected with Python v3.8>=
### **Features In Development for v1.1.0**
-  Improved FP COBOL-to-JSON functionality
-  Template Python Function using ``jsoncons``
### **Roadmap to v2.0.0
-  Integration with IBM zOS 

## 🤝 Contributing 🖥️

Contributions are welcome! If you find errors, have suggestions for improvements, or want to add more examples, please feel free to:

1.  Open an issue to discuss the change.
2.  Fork the repository.
3.  Create a new branch (`git checkout -b feature/your-feature-name`).
4.  Make your changes and commit them (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## 📝 License ⚖️

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🧪 Unit Test Explanation For `jsoncons` Package ✅

1.  **Imports:** Imports necessary modules like `unittest`, `sys` (for patching argv/streams), `io` (for capturing streams), `os`, `json`, `tempfile`, `shutil`, and `unittest.mock.patch`. It also imports the `cli` module from the package.
2.  **`TestJsonConsCLI` Class:** Inherits from `unittest.TestCase`.
3.  **`setUp`:**
    *   Creates a temporary directory using `tempfile.mkdtemp()` to isolate test files.
    *   Defines paths for input, output, and invalid files within the temp directory.
    *   Creates sample valid and invalid JSON strings and data structures.
    *   Writes the sample valid and invalid JSON to the respective temporary files.
4.  **`tearDown`:** Cleans up by removing the temporary directory and all its contents using `shutil.rmtree()`.
5.  **`run_cli` Helper:**
    *   Takes a list of arguments (`args_list`) and optional `stdin_data`.
    *   Prepends the script name (`'serial-json'`) to the arguments list as `sys.argv[0]`.
    *   Uses `unittest.mock.patch` as a context manager to temporarily replace `sys.argv`, `sys.stdout`, and `sys.stderr` with test-controlled objects (`io.StringIO` for streams).
    *   If `stdin_data` is provided, `sys.stdin` is also patched.
    *   Calls the actual `cli.main()` function within the patched context.
    *   Catches `SystemExit` (which `sys.exit()` raises) to get the exit code.
    *   Returns the captured stdout string, stderr string, and the exit code.
6.  **Test Methods (`test_...`)**:
    *   Each method tests a specific scenario (stdin/stdout, file I/O, options, errors).
    *   They call `run_cli` with appropriate arguments and/or stdin data.
    *   They use `self.assertEqual`, `self.assertNotEqual`, `self.assertTrue`, `self.assertIn`, etc., to verify:
        *   The exit code (0 for success, non-zero for errors).
        *   The content of captured `stderr` (should be empty on success, contain error messages on failure).
        *   The content of captured `stdout` (when output is expected there).
        *   The existence and content of output files (when file output is expected).
7.  **`if __name__ == '__main__':`**: Allows running the tests directly using `python -m unittest tests.test_cli` or `python tests/test_cli.py`.


## ⛰️ Extending ``jsoncons`` to COBOL 👀

**How COBOL could interact:**

A COBOL program could:

1.  **Write data to a temporary text file** (e.g., `input.txt`).
2.  **Use `CALL 'SYSTEM'`** (or equivalent OS call) to execute the Python script:
    ```cobol
    CALL 'SYSTEM' USING 'jsoncons input.txt output.json'.
    ```
3.  **Read the resulting `output.json` file** from COBOL.

Alternatively:

1.  COBOL generates simple key-value pairs or a structured text format.
2.  A more sophisticated `jsoncons` `encode` command could be written to parse this specific text format and produce JSON.
3.  A `jsoncons` `decode` command could parse JSON and output a simple text format readable by COBOL.

The provided CLI keeps things simple and standard, relying on JSON as the interchange format, which COBOL would interact with via file I/O and system calls.

