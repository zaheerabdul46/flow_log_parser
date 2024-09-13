# Flow Log Parser 
- Flow log parser that maps logs based on port and protocol

## Project Description
This project contains a Python script (`flow_log_parser.py`) that parses flow logs, maps each log entry to a tag based on port and protocol combinations from a lookup table (`lookup_table.csv`), and generates an output file (`output_results.txt`) with tag counts and port/protocol combination counts.

### Assumptions Made
- The lookup table (`lookup_table.csv`) must contain valid mappings of ports and protocols to tags.
- The program does not account for source port tagging (though the code includes an option for future implementation).

### How to Run the Program

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/flow_log_parser.git

3. **Navigate to the Project Directory:**
   ```bash
   cd flow_log_parser

5. **Ensure Python 3.x is Installed: Make sure you have Python 3.x installed. You can check this by running:**
   ```bash
   python3 --version

6. **Run the Python Script: Execute the program using the following command:**
   ```bash
   python3 flow_log_parser.py

7. **View the Output: The results will be written to output_results.txt. This file will contain:**

    - Tag Counts: Counts of how many logs were tagged with each tag.
    - Port/Protocol Combination Counts: Counts of logs for each destination port/protocol combination.

**Files Included**
- **flow_log_parser.py**: The Python script to parse and process flow logs.
- **lookup_table.csv**: A sample lookup table that maps destination ports and protocols to tags.
- **flow_logs.txt**: A sample log file containing flow log entries.
- **output_results.txt**: The output file generated after parsing and processing the logs.

**Tests Performed**
- **Tag Matching:** Verified that logs with valid port and protocol combinations were correctly tagged.
- **Untagged Logs:** Tested with logs containing ports not present in the lookup table to ensure they were counted as "Untagged".
