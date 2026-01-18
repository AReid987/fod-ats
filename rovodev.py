


import argparse
import json
import re
from difflib import SequenceMatcher

def calculate_ats_score(resume, keywords, threshold=85, strict_mode=False):
    """Calculate ATS compatibility score"""
    # Normalize text
    resume = resume.lower()
    keyword_list = [k.lower() for k in keywords]
    
    # Calculate keyword coverage
    found_keywords = []
    for keyword in keyword_list:
        if re.search(rf'\b{re.escape(keyword)}\b', resume):
            found_keywords.append(keyword)
    
    # Calculate section completeness
    sections = ['experience', 'education', 'skills']
    section_score = sum(1 for section in sections if re.search(fr'#+\s*{section}', resume, re.I)) / len(sections)
    
    # Calculate overall score
    keyword_score = len(found_keywords) / len(keyword_list) * 100 if keyword_list else 0
    overall_score = (keyword_score * 0.7) + (section_score * 30)
    
    # Apply strict mode penalty
    if strict_mode and overall_score < threshold:
        overall_score *= 0.8
    
    return {
        'score': round(overall_score, 1),
        'threshold': threshold,
        'keywords_found': found_keywords,
        'keywords_missing': list(set(keyword_list) - set(found_keywords)),
        'section_completeness': round(section_score * 100, 1)
    }

def main():
    parser = argparse.ArgumentParser(description='Rovodev: ATS Simulation & Scoring')
    parser.add_argument('--input', nargs='+', required=True, help='Input files: resume.md keywords.json')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--params', default='{}', help='JSON parameters')
    
    args = parser.parse_args()
    params = json.loads(args.params)
    
    # Read input files
    with open(args.input[0], 'r') as f:
        resume = f.read()
    
    with open(args.input[1], 'r') as f:
        keywords = json.load(f)
    
    # Process and score
    result = calculate_ats_score(
        resume,
        keywords,
        threshold=params.get('threshold', 85),
        strict_mode=params.get('strict_mode', False)
    )
    
    # Save output
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"ATS scoring complete. Score: {result['score']}/100")

if __name__ == '__main__':
    main()


