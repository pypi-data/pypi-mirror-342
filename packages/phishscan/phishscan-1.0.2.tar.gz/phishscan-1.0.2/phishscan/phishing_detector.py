import re
import os
from urllib.parse import urlparse
from email.utils import parseaddr
from confusables import is_confusable

import importlib.resources

def load_keywords():
    with importlib.resources.open_text('phishscan', 'phishing_keywords.txt', encoding='utf-8') as f:
        return [line.strip().lower() for line in f if line.strip()]

PHISHING_KEYWORDS = load_keywords()
SUSPICIOUS_TLDS = ['.ru', '.tk', '.xyz', '.top', '.club', '.cn']
DANGEROUS_FILE_EXTENSIONS = ['.exe', '.scr', '.js', '.jar', '.vbs', '.docm', '.xlsm', '.bat']
URL_SHORTENERS = ["bit.ly", "tinyurl", "goo.gl", "t.co"]

def contains_phishing_keywords(text):
    text = text.lower()
    return [kw for kw in PHISHING_KEYWORDS if kw in text]

def has_suspicious_links(urls):
    reasons = []
    for url in urls:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()

        if not parsed.scheme.startswith("http"):
            reasons.append(f"Non-HTTP link: {url}")
        if re.match(r'https?://\d+\.\d+\.\d+\.\d+', url):
            reasons.append(f"IP-based URL: {url}")
        if any(tld in netloc for tld in SUSPICIOUS_TLDS):
            reasons.append(f"Suspicious TLD in link: {netloc}")
        if any(short in netloc for short in URL_SHORTENERS):
            reasons.append(f"Shortened URL: {url}")
        if looks_like_homoglyph(netloc):
            reasons.append(f"⚠️ Homoglyph domain: {netloc}")
    return reasons

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
    common_domains = ["google", "paypal", "amazon", "apple", "microsoft"]
    for legit in common_domains:
        if is_confusable(domain, legit):
            return True
    return False

def check_reply_to_mismatch(headers):
    from_addr = parseaddr(headers.get("from", ""))[1]
    reply_to = parseaddr(headers.get("reply-to", ""))[1]
    if reply_to and reply_to != from_addr:
        return True
    return False

def check_dangerous_attachments(msg):
    reasons = []
    for part in msg.walk():
        filename = part.get_filename()
        if filename:
            _, ext = os.path.splitext(filename)
            if ext.lower() in DANGEROUS_FILE_EXTENSIONS:
                reasons.append(f"⚠️ Dangerous attachment: {filename}")
    return reasons

def detect_phishing(email_data, raw_msg=None, headers=None):
    score = 0
    reasons = []

    found_keywords = contains_phishing_keywords(email_data.get("body", ""))
    if found_keywords:
        score += 2
        reasons.append(f"⚠️ Phishing phrases: {', '.join(found_keywords)}")

    suspicious_links = has_suspicious_links(email_data.get("urls", []))
    if suspicious_links:
        score += 2
        reasons.extend([f"🔗 {reason}" for reason in suspicious_links])

    if is_suspicious_sender(email_data.get("sender", "")):
        score += 1
        reasons.append("📬 Suspicious sender domain")

    if has_display_name_mismatch(email_data.get("sender", "")):
        score += 1
        reasons.append("👻 Display name mismatch")

    if raw_msg:
        attach_issues = check_dangerous_attachments(raw_msg)
        if attach_issues:
            score += 2
            reasons.extend([f"📎 {issue}" for issue in attach_issues])

    if headers and check_reply_to_mismatch(headers):
        score += 1
        reasons.append("📤 Reply-To mismatch")

    if score >= 5:
        verdict = "🚨 Phishing Likely"
    elif score >= 2:
        verdict = "⚠️ Suspicious"
    else:
        verdict = "✅ Looks Clean"

    return verdict, reasons
