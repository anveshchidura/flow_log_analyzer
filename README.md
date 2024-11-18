# Flow Log Analyzer

A Python-based tool that analyzes AWS VPC flow logs and maps them to tags based on destination port and protocol combinations. This tool processes flow log data and generates reports about tag matches and port/protocol combinations.

## Features

- Parses AWS VPC flow logs 
- Maps flows to tags using a configurable lookup table
- Generates tag match statistics and port/protocol combination counts
- Includes a utility to generate sample flow log data for testing

## Project Structure

```
flow_log_analyzer/
├── samples/
│   ├── flowlog.txt            # Sample flow log file
│   └── lookup_table.csv       # Sample lookup table
├── src/
│   ├── __init__.py
│   ├── analyzer.py            # Main analysis logic
│   ├── flow_parser.py         # Flow log parsing
│   ├── lookup_parser.py       # Lookup table parsing
│   └── flowlogs_generator.py  # Test data generator
└── main.py                    # Entry point
```

## Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/anveshchidura/flow_log_analyzer.git]
cd flow_log_analyzer
```

## Usage

### Using Sample Files

To analyze the provided sample files:
```bash
python main.py samples/flowlog.txt samples/lookup_table.csv
```

### Generating Test Data

To generate a 20MB flow log file with random data and analyze it:
```bash
python src/flowlogs_generator.py
python main.py flow_logs.txt samples/lookup_table.csv
```

### Using Custom Data

You can analyze your own flow logs and lookup tables by following these steps:

1. **Prepare Your Flow Log File**
   - Ensure your flow log file follows the AWS VPC Flow Log format 
   - Save it as `my_flow_logs.txt` file

2. **Prepare Your Lookup Table**
   - Create a CSV file with three columns: dstport, protocol, tag
   - Save it as a CSV file, for example: `my_lookup.csv`

3. **Run the Analysis**
   ```bash
   python main.py path/to/my_flow_logs.txt path/to/my_lookup.csv
   ```

### Output Files

The program generates two CSV files in the project directory:
- `tag_counts.csv`: Contains counts for each tag match
- `port_protocol_counts.csv`: Contains counts for each port/protocol combination


## Assumptions and Limitations

1. Flow Log Format:
   - Default format only (no custom log formats)
   - Input files must be ASCII encoded

2. Input Validation:
   - Port numbers must be between 0 and 65535
   - Protocols are limited to TCP (6), UDP (17), and ICMP (1)
   - Tag matching is case-insensitive

3. File Handling:
   - Files must be readable files

## Testing

The code includes basic error handling and validation for:
- Basic file format validation
- Port number range validation (0-65535)
- Protocol validation (TCP, UDP, ICMP)
- Version 2 flow log format validation
- Basic ASCII encoding validation

## Error Handling

The program implements error handling for:
- File not found errors (checks file existence before processing)
- Invalid port numbers (validates range 0-65535)
- Unsupported protocols (validates against known protocol list)
- Basic input validation (checks field count and format)
- ASCII encoding validation (ensures files are ASCII encoded)
- Malformed log entries (skips invalid entries with warnings)