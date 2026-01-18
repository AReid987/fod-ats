



import argparse
import json
import re
from collections import Counter

def calculate_match(job_desc, resume, required_skills=90, preferred_skills=70):
    """Calculate match between job description and resume"""
    # Extract skills from job description
    jd_skills = re.findall(r'\b(?:required|preferred):?\s*([\w\s]+)\.?', job_desc, re.I)
    jd_skills = [skill.strip().lower() for skill in jd_skills if skill.strip()]
    
    # Classify skills as required/preferred
    required = []
    preferred = []
    for skill in jd_skills:
        if 'required' in skill or 'must' in skill:
            required.append(skill.replace('required:', '').replace('must', '').strip())
        else:
            preferred.append(skill)
    
    # Find matches in resume
    resume_text = resume.lower()
    required_matches = [skill for skill in required if skill in resume_text]
    preferred_matches = [skill for skill in preferred if skill in resume_text]
    
    # Calculate match percentages
    req_percent = len(required_matches) / len(required) * 100 if required else 100
    pref_percent = len(preferred_matches) / len(preferred) * 100 if preferred else 100
    
    # Generate report
    report = f"# Job Match Report\n\n"
    report += f"## Required Skills Match: {req_percent:.1f}%\n"
    report += f"- **Matched:** {', '.join(required_matches) or 'None'}\n"
    report += f"- **Missing:** {', '.join(set(required) - set(required_matches)) or 'None'}\n\n"
    
    report += f"## Preferred Skills Match: {pref_percent:.1f}%\n"
    report += f"- **Matched:** {', '.join(preferred_matches) or 'None'}\n"
    report += f"- **Missing:** {', '.join(set(preferred) - set(preferred_matches)) or 'None'}\n\n"
    
    report += f"## Overall Recommendation: "
    if req_percent >= required_skills:
        report += "Strong Match" if pref_percent >= preferred_skills else "Qualified"
    else:
        report += "Needs Improvement"
    
    return report

def main():
    parser = argparse.ArgumentParser(description='OpenHands: Job Description Cross-Reference')
    parser.add_argument('--input', nargs='+', required=True, help='Input files: job_description.txt enhanced_resume.md')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--params', default='{}', help='JSON parameters')
    
    args = parser.parse_args()
    params = json.loads(args.params)
    
    # Read input files
    with open(args.input[0], 'r') as f:
        job_desc = f.read()
    
    with open(args.input[1], 'r') as f:
        resume = f.read()
    
    # Generate match report
    report = calculate_match(
        job_desc,
        resume,
        required_skills=params.get('required_skills', 90),
        preferred_skills=params.get('preferred_skills', 70)
    )
    
    # Save output
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"Job match analysis complete. Output: {args.output}")

if __name__ == '__main__':
    main()



