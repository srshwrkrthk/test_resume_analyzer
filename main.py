import pdfplumber
import re

em_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'
numpat = r'\+?\d[\d\s\-]{8,12}\d'

text = ""

with pdfplumber.open("functionalsample.pdf") as pdf:
    for page in pdf.pages:
        a = page.extract_text()

        if a:
            text += a + "\n"

emails = re.findall(em_pattern, text)
numbers = re.findall(numpat, text)

print("Emails:", emails)
print("Numbers:", numbers)

software_engineer_skills = [
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "typescript",
    "dsa",
    "algorithms",
    "data structures",
    "oop",
    "operating systems",
    "dbms",
    "computer networks",
    "sql",
    "git",
    "github",
    "react",
    "node.js",
    "express",
    "mongodb",
    "mysql",
    "api",
    "rest api",
    "linux",
    "docker"
]

data_science_skills = [
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "machine learning",
    "deep learning",
    "pandas",
    "numpy",
    "matplotlib",
    "data visualization",
    "statistics",
    "tensorflow",
    "scikit-learn",
    "data analysis"
]

cybersecurity_skills = [
    "network security",
    "ethical hacking",
    "penetration testing",
    "wireshark",
    "linux",
    "kali linux",
    "cryptography",
    "owasp",
    "nmap",
    "burp suite",
    "firewalls",
    "incident response",
    "vulnerability assessment",
    "python",
    "security analysis"
]

ch = input(
    "Enter Job Role you are looking for\n"
    "1. SOFTWARE ENGINEER\n"
    "2. DATA SCIENCE\n"
    "3. CYBERSEC\n"
    "Choice: "
)

if ch == "1":
    required_skills = software_engineer_skills
    selected_role = "Software Engineer"

elif ch == "2":
    required_skills = data_science_skills
    selected_role = "Data Science"

elif ch == "3":
    required_skills = cybersecurity_skills
    selected_role = "Cybersecurity"

else:
    print("Invalid choice")
    required_skills = []
    selected_role = "Unknown"

role_scores = {
    "software engineer": 0,
    "data science": 0,
    "cybersecurity": 0
}

text = text.lower()

found_skills = []

for skill in required_skills:
    if skill.lower() in text:
        found_skills.append(skill)

total_required = len(required_skills)
total_found = len(found_skills)
if total_required > 0:
    match_score = (total_found / total_required) * 100
else:
    match_score = 0
print(f"\nMATCH SCORE: {match_score:.2f}%")
print("\nSELECTED ROLE:", selected_role)
print("\nSKILLS FOUND:")
print(found_skills)

missing_skills = []

for skill in required_skills:
    if skill not in found_skills:
        missing_skills.append(skill)

print("\nMISSING SKILLS:")
print(missing_skills)

if match_score >= 80:
    print("Excellent profile match!")

elif match_score >= 60:
    print("Good profile match!")

elif match_score >= 40:
    print("Average profile match.")

else:
    print("Low profile match. Skill improvement recommended.")


privacy_score = 0

if emails:
    privacy_score += 20

if numbers:
    privacy_score += 30

linkedin_pattern = r'linkedin\.com/in/[^\s]+'
linkedin_links = re.findall(linkedin_pattern, text)
if linkedin_links:
    privacy_score += 10
github_pattern = r'github\.com/[^\s]+'
github_links = re.findall(github_pattern, text)
if github_links:
    privacy_score += 5
print(f"\nPRIVACY RISK SCORE: {privacy_score}/100")
if privacy_score >= 50:
    print("⚠️ High privacy exposure detected!")

elif privacy_score >= 30:
    print("Moderate privacy exposure.")

else:
    print("Low privacy exposure.")
