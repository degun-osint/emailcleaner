import argparse
import csv
import re
import os
import pyfiglet
from termcolor import colored


# Function to check if an email is valid
def is_valid_email(email):
    # Define the regular expression for a valid email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check for the ".@" pattern in the email
    if ".@" in email:
        return False

    # Match the email against the regex
    return re.match(regex, email) is not None


# Main function
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Verify and clean a list of emails in a CSV file.')
    parser.add_argument('input_csv', help='Path to the input CSV file containing emails.')
    args = parser.parse_args()

    # Get input and output file names
    input_csv = args.input_csv
    output_csv_cleaned = os.path.splitext(input_csv)[0].rstrip('.csv') + '-cleaned.csv'
    output_csv_invalid = os.path.splitext(input_csv)[0].rstrip('.csv') + '-invalid.csv'

    # Initialize counters and lists
    total_emails = 0
    valid_emails = 0
    invalid_emails = 0
    invalid_email_list = []

    # Process the input and output files
    with open(input_csv, 'r') as input_file, \
            open(output_csv_cleaned, 'w', newline='') as output_cleaned_file, \
            open(output_csv_invalid, 'w', newline='') as output_invalid_file:

        reader = csv.reader(input_file)
        writer_cleaned = csv.writer(output_cleaned_file)
        writer_invalid = csv.writer(output_invalid_file)
        next(reader)  # Skip the first line (header)

        # Iterate through the input file rows
        for row in reader:
            if not row:  # Skip empty rows
                continue
            email = row[0].lower()
            total_emails += 1

            # Check if the email is valid and write it to the corresponding output file
            if is_valid_email(email):
                valid_emails += 1
                writer_cleaned.writerow([email])
            else:
                invalid_emails += 1
                invalid_email_list.append(email)
                writer_invalid.writerow([email])

    # Generate and print the summary
    asciiCleaned = pyfiglet.figlet_format("Cleaned!")
    print(colored(f'{asciiCleaned}', 'white'))
    print(f'Total email verified: {total_emails}')
    print(colored(f'✅ Total valid emails: {valid_emails}. \n   File as been saved to {output_csv_cleaned}\n', 'green'))
    print(
        colored(f'❌ Total invalid emails: {invalid_emails}. \n   File as been saved to {output_csv_invalid}\n', 'red'))
    print(colored(f'Invalid email list:', 'white', 'on_red'))
    for invalid_email in invalid_email_list:
        print(invalid_email)


# Run the main function
if __name__ == '__main__':
    main()
