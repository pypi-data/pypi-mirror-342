import argparse
import os
from phishscan.email_processor import extract_content
from phishscan.phishing_detector import detect_phishing
from email import policy
from email.parser import BytesParser
from phishscan import __version__


def main():
    # Set up argument parser to accept the file input
    parser = argparse.ArgumentParser(description="Phishing Email Scanner")
    parser.add_argument('-f', '--file', type=str, help="Path to the suspicious .eml file")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args()

    # Check if the version flag is set
    if args.version:
        print(f"phishscan version {__version__}")
        return
    

    # If no file argument is given, display a helpful message
    if not args.file:
        print("❌ You must provide a file using the -f flag.")
        print("Usage: phishscan -f path_to_email_file.eml")
        exit()

    file_path = args.file  # Get file path from command-line argument

    if not os.path.isfile(file_path):
        print("❌ The file does not exist. Please check the path and try again.")
        exit()

    try:
        email_data = extract_content(file_path)
        print("📧 Email Data Extracted Successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        exit()

    # Display extracted data and URLs
    print("\n📧 Extracted Email Data:")
    print(f"Sender: {email_data['sender']}")
    print(f"Subject: {email_data['subject']}")
    print("\n📨 Body:\n")
    print(email_data['body'])

    # Display URLs
    def shorten_url(url, max_len=80):
        return url if len(url) <= max_len else url[:max_len] + "..."

    print("\n🔗 URLs Found:")
    for i, url in enumerate(email_data['urls'], 1):
        print(f"{i}. {shorten_url(url)}")

    # Phishing Detection
    with open(file_path, 'rb') as f:
        raw_msg = BytesParser(policy=policy.default).parse(f)

    verdict, reasons = detect_phishing(email_data, raw_msg=raw_msg, headers=raw_msg)

    # ✅ Verdict + Reasoning Display
    print("\n🔍 Phishing Detection Result:")
    print(f"Verdict: {verdict}")
    if reasons:
        print("Reasons:")
        for reason in reasons:
            print(f"- {reason}")

    print("\n✅ Email processing complete!")
