import re
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup

def extract_content(file_path):
    """
    Parses an eml file and extracts sender, subject, body and URLs.
    """
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # Extract sender and subject
    sender = msg['from'] or "Unknown"
    subject = msg['subject'] or "No Subject"

    # Extract body
    body = ""
    urls = []

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body += part.get_content()
            elif part.get_content_type() == 'text/html':
                html = part.get_content()
                soup = BeautifulSoup(html, 'html.parser')
                body += soup.get_text(separator="\n")
                urls += [a['href'] for a in soup.find_all('a', href=True)]
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain':
            body = msg.get_content()
        elif content_type == 'text/html':
            html = msg.get_content()
            soup = BeautifulSoup(html, 'html.parser')
            body = soup.get_text(separator="\n")

            # ✅ Extract <a href="..."> links
            urls += [a['href'] for a in soup.find_all('a', href=True)]
    
    # 📤 Extract and remove <https://...> style links from the plain text body
    angle_links = re.findall(r'<(https?://[^>]+)>', body)
    urls += angle_links
    body = re.sub(r'<https?://[^>]+>', '', body)

     # Clean the body text
    lines = body.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    clean_body = "\n".join(cleaned_lines)

    return{
        "sender": sender,
        "subject": subject,
        "body": clean_body,
        "urls": list(set(urls))  # Remove duplicates
    }
    