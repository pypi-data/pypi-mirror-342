
import re
import os
from urllib.parse import urlparse
from email.utils import parseaddr
from confusables import is_confusable

def load_keywords(path="phishing_keywords.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

PHISHING_KEYWORDS = load_keywords()
SUSPICIOUS_TLDS = ['.ru', '.tk', '.xyz', '.top', '.club', '.cn', '.pw', '.buzz']
DANGEROUS_FILE_EXTENSIONS = ['.exe', '.scr', '.js', '.jar', '.vbs', '.docm', '.xlsm', '.bat', '.cmd']
URL_SHORTENERS = ["bit.ly", "tinyurl", "goo.gl", "t.co", "ow.ly"]

def contains_phishing_keywords(text):
    text = text.lower()
    matches = [kw for kw in PHISHING_KEYWORDS if kw in text]
    return matches, len(matches)

def has_suspicious_links(urls):
    reasons = []
    score = 0
    for url in urls:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()

        if not parsed.scheme.startswith("http"):
            reasons.append(f"Non-HTTP link: {url}")
            score += 1
        if re.match(r'https?://\d+\.\d+\.\d+\.\d+', url):
            reasons.append(f"IP-based URL: {url}")
            score += 2
        if any(tld in netloc for tld in SUSPICIOUS_TLDS):
            reasons.append(f"Suspicious TLD in link: {netloc}")
            score += 1
        if any(short in netloc for short in URL_SHORTENERS):
            reasons.append(f"Shortened URL: {url}")
            score += 1
        if looks_like_homoglyph(netloc):
            reasons.append(f"Homoglyph domain: {netloc}")
            score += 2
    return reasons, score

def is_suspicious_sender(sender):
    name, email_addr = parseaddr(sender)
    domain = email_addr.split("@")[-1].lower() if "@" in email_addr else ""
    return any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS)

def has_display_name_mismatch(sender):
    name, email_addr = parseaddr(sender)
    if not name or not email_addr:
        return False
    name = name.lower()
    domain = email_addr.split("@")[-1].lower()
    domain_keywords = domain.replace('.', ' ').replace('-', ' ').split()
    return not any(n in domain_keywords for n in name.split())

def looks_like_homoglyph(domain):
    known_brands = ["google", "paypal", "amazon", "apple", "microsoft", "outlook", "facebook"]
    for brand in known_brands:
        if is_confusable(domain, brand):
            return True
    return False

def check_reply_to_mismatch(headers):
    from_addr = parseaddr(headers.get("from", ""))[1]
    reply_to = parseaddr(headers.get("reply-to", ""))[1]
    return reply_to and reply_to != from_addr

def check_dangerous_attachments(msg):
    reasons = []
    for part in msg.walk():
        filename = part.get_filename()
        if filename:
            _, ext = os.path.splitext(filename)
            if ext.lower() in DANGEROUS_FILE_EXTENSIONS:
                reasons.append(f"Dangerous attachment: {filename}")
    return reasons

def detect_phishing(email_data, raw_msg=None, headers=None):
    score = 0
    reasons = []

    # Keyword detection
    keywords, count = contains_phishing_keywords(email_data.get("body", ""))
    if count >= 3:
        score += 3
        reasons.append(f"High number of phishing keywords: {', '.join(keywords)}")
    elif count > 0:
        score += 1
        reasons.append(f"Some phishing keywords found: {', '.join(keywords)}")

    # Link checks
    suspicious_links, link_score = has_suspicious_links(email_data.get("urls", []))
    if suspicious_links:
        score += link_score
        reasons.extend([f"Link issue: {reason}" for reason in suspicious_links])

    # Sender checks
    if is_suspicious_sender(email_data.get("sender", "")):
        score += 1
        reasons.append("Suspicious sender domain")
    if has_display_name_mismatch(email_data.get("sender", "")):
        score += 1
        reasons.append("Display name mismatch")

    # Attachments
    if raw_msg:
        attach_reasons = check_dangerous_attachments(raw_msg)
        if attach_reasons:
            score += 2
            reasons.extend(attach_reasons)

    # Header tricks
    if headers and check_reply_to_mismatch(headers):
        score += 1
        reasons.append("Reply-To address mismatch")

    # Verdict
    if score >= 6:
        verdict = "🚨 Phishing Likely"
    elif score >= 3:
        verdict = "⚠️ Suspicious"
    else:
        verdict = "✅ Looks Clean"

    return verdict, reasons
