import argparse
import csv
import re
import os
import pyfiglet
import chardet
import codecs
import time
from termcolor import colored


# Function to check if an email is valid

def is_valid_email(email):

    # Check if an email address is valid.
    if not email:
        return False

    # Define the regular expression for a valid email
    regex = r"^[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)*@[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)*(\.[a-zA-Z]{2,6})$"

    # Check for the ".@" pattern in the email
    if ".@" in email:
        return False

    # Match the email against the regex
    return re.match(regex, email) is not None


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Verify and clean a list of emails in a CSV file.')
    parser.add_argument('input_csv', help='Path to the input CSV file containing emails.')
    args = parser.parse_args()

    # Get input and output file names
    input_csv = args.input_csv
    output_csv_cleaned = os.path.splitext(input_csv)[0].rstrip('.csv') + '-cleaned.csv'
    output_csv_invalid = os.path.splitext(input_csv)[0].rstrip('.csv') + '-invalid.csv'
    with open(input_csv, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']

    # Initialize counters and lists
    total_emails = 0
    valid_emails = 0
    invalid_emails = 0
    invalid_email_list = []

    # Process the input and output files
    with open(input_csv, 'rb') as input_file:
        encoding = chardet.detect(input_file.read())['encoding']
        input_file.seek(0)
        input_data = input_file.read().decode(encoding, errors='ignore')
        dialect = csv.Sniffer().sniff(input_data[:1024])
        input_file.seek(0)
        reader = csv.reader(codecs.iterdecode(input_file, encoding), dialect)

        try:
            header = next(reader, None)
        except StopIteration:
            raise ValueError("CSV file is empty")

        # Find the email column index
        email_index = None
        if header:
            for col in ['email', 'emails']:
                if col in header:
                    email_index = header.index(col)
                    break
        else:
            # If there's no header, assume that the only column is the email column
            if len(next(reader)) == 1:
                email_index = 0

        if email_index is None:
            raise ValueError("No 'email' or 'emails' column found in the CSV file.")

        with open(output_csv_cleaned, 'w', newline='') as output_cleaned_file, \
                open(output_csv_invalid, 'w', newline='') as output_invalid_file:

            writer_cleaned = csv.writer(output_cleaned_file, dialect, quoting=csv.QUOTE_NONNUMERIC, escapechar='\\')
            writer_invalid = csv.writer(output_invalid_file, dialect, quoting=csv.QUOTE_NONNUMERIC, escapechar='\\')

            if header:
                writer_cleaned.writerow(header)
                writer_invalid.writerow(header)
            start_time = time.time()
            for row in reader:
                if not row:  # Skip empty rows
                    continue
                email = row[email_index].lower()  # Convert email to lowercase
                total_emails += 1

                if is_valid_email(email):
                    valid_emails += 1
                    writer_cleaned.writerow(row)
                else:
                    invalid_emails += 1
                    invalid_email_list.append(email)
                    writer_invalid.writerow(row)

    # Generate and print the summary
    time_elapsed = time.time() - start_time
    ascii_cleaned = pyfiglet.figlet_format("Cleaned!")
    print(colored(f'{ascii_cleaned}', 'cyan'))
    print(colored(f'by Degun - https://github.com/degun-osint\n\n', 'cyan'))
    print(f'➡️  Total email verified: {total_emails} in {time_elapsed:.2f} seconds.\n')
    print(colored(f'✅ Total valid emails: {valid_emails}. \n   File as been saved to {output_csv_cleaned}\n', 'green'))
    print(
        colored(f'❌ Total invalid emails: {invalid_emails}. \n   File as been saved to {output_csv_invalid}\n', 'red'))
    print(colored(f'Invalid email list:', 'white', 'on_red'))
    for invalid_email in invalid_email_list:
        print(invalid_email)


# Run the main function
if __name__ == '__main__':
    main()
