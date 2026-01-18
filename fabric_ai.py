


import argparse
import json
import re
import random

# Professional action verbs for resume enhancement
ACTION_VERBS = [
    "developed", "implemented", "managed", "optimized", "created",
    "led", "improved", "increased", "reduced", "designed",
    "built", "launched", "spearheaded", "transformed", "streamlined"
]

def enhance_content(resume, keywords, style="professional", keyword_density=0.05, max_length=800):
    """Enhance resume content with professional language and keywords"""
    # Convert to professional tone
    if style == "professional":
        for verb in ACTION_VERBS:
            resume = re.sub(
                rf'\b(?:made|did|worked on)\b(.*?{verb[:4]})', 
                verb + r'\1', 
                resume, 
                flags=re.IGNORECASE
            )
    
    # Strategic keyword placement
    keyword_list = list(keywords.keys())
    if keyword_list:
        # Calculate target keyword count
        word_count = len(re.findall(r'\b\w+\b', resume))
        target_count = max(1, int(word_count * keyword_density))
        
        # Add missing keywords in context
        added = 0
        for keyword in keyword_list:
            if keyword not in resume.lower() and added < target_count:
                # Find appropriate section to insert
                if re.search(r'(skills|experience|summary)', resume, re.I):
                    resume = re.sub(
                        r'(#+\s*Skills\b.*?)(?=#|$)',
                        r'\1\n- ' + keyword.capitalize(),
                        resume,
                        flags=re.IGNORECASE | re.DOTALL
                    )
                    added += 1
    
    # Trim to max length if needed
    if len(resume) > max_length:
        resume = resume[:max_length].rsplit(' ', 1)[0] + " [...]"
    
    return resume

def main():
    parser = argparse.ArgumentParser(description='Fabric AI: Content Enhancement')
    parser.add_argument('--input', required=True, help='Input file path (resume.md)')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--params', default='{}', help='JSON parameters')
    
    args = parser.parse_args()
    params = json.loads(args.params)
    
    # Read input file
    with open(args.input, 'r') as f:
        resume = f.read()
    
    # Get keywords if available (optional)
    keywords = {}
    try:
        with open('keywords.json', 'r') as f:
            keywords = json.load(f)
    except:
        pass
    
    # Enhance content
    enhanced = enhance_content(
        resume,
        keywords,
        style=params.get('style', 'professional'),
        keyword_density=params.get('keyword_density', 0.05),
        max_length=params.get('max_length', 800)
    )
    
    # Save output
    with open(args.output, 'w') as f:
        f.write(enhanced)
    
    print(f"Content enhancement complete. Output: {args.output}")

if __name__ == '__main__':
    main()


