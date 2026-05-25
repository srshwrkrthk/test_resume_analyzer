import re


def analyze_privacy(text):

    privacy_score = 0

    findings = {}

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'

    emails = re.findall(email_pattern, text)

    findings["emails"] = emails

    if emails:
        privacy_score += 15


    phone_pattern = r'\+?\d[\d\s\-]{8,12}\d'

    phone_numbers = re.findall(phone_pattern, text)

    findings["phone_numbers"] = phone_numbers

    if phone_numbers:
        privacy_score += 20


    linkedin_pattern = r'linkedin\.com/in/[^\s]+'

    linkedin_links = re.findall(linkedin_pattern, text)

    findings["linkedin"] = linkedin_links

    if linkedin_links:
        privacy_score += 5


    github_pattern = r'github\.com/[^\s]+'

    github_links = re.findall(github_pattern, text)

    findings["github"] = github_links

    if github_links:
        privacy_score += 5



    aadhaar_pattern = r'\b\d{4}\s\d{4}\s\d{4}\b'

    aadhaar_numbers = re.findall(aadhaar_pattern, text)

    findings["aadhaar"] = aadhaar_numbers

    if aadhaar_numbers:
        privacy_score += 40



    pan_pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'

    pan_numbers = re.findall(pan_pattern, text)

    findings["pan"] = pan_numbers

    if pan_numbers:
        privacy_score += 35


    dob_pattern = r'\b\d{2}[/-]\d{2}[/-]\d{4}\b'

    dob = re.findall(dob_pattern, text)

    findings["dob"] = dob

    if dob:
        privacy_score += 10


    if privacy_score >= 70:
        risk_level = "HIGH"

    elif privacy_score >= 40:
        risk_level = "MODERATE"

    else:
        risk_level = "LOW"

    findings["privacy_score"] = privacy_score
    findings["risk_level"] = risk_level

    return findings