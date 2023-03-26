# Email Cleaner

Email Cleaner is a Python script that verifies and cleans a list of emails provided in a CSV file.

## Requirements

To run the script, you need to have Python 3.x installed on your system, as well as the libraries specified in the `requirements.txt` file.

To install the required libraries, run the following command:

```pip install -r requirements.txt```


## Usage

1. Prepare a CSV file with a list of emails, one email per line.
2. Run the script from the command line:

```python email_cleaner.py input.csv```


Replace `input.csv` with the name of your input CSV file containing the email list.

The script will create two output CSV files:
- A file containing valid emails with the "-cleaned" suffix added to the input file name (e.g., `input-cleaned.csv`)
- A file containing invalid emails with the "-invalid" suffix added to the input file name (e.g., `input-invalid.csv`)

At the end of the script execution, you'll see a summary with the total number of emails verified, the number of valid and invalid emails, and a list of invalid emails.
