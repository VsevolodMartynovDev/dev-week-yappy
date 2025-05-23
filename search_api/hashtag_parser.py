import re

def parse_hashtags(text):
    hashtags = re.findall(r'#(\w+)', text)
    
    if not hashtags:
        return text
    
    text_without_spaces = text.strip()
    text_without_hashtags = re.sub(r'#\w+', '', text_without_spaces).strip()
    
    if not text_without_hashtags:
        return ', '.join(hashtags)
    
    return text
