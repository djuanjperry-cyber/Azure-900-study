import json
from pathlib import Path
import re

def is_quality_flashcard(flashcard):
    """Check if flashcard has quality content."""
    question = flashcard.get('question', '')
    option_a = flashcard.get('options', [''])[0]
    explanation = flashcard.get('explanation', '')
    
    # Check for obvious issues
    bad_patterns = [
        r'would recommend you',
        r'youtube',
        r'subscribe',
        r'channel',
        r'watch this',
        r'hit the Bell',
        r'like and subscribe',
    ]
    
    for pattern in bad_patterns:
        if re.search(pattern, option_a, re.IGNORECASE):
            return False
        if re.search(pattern, explanation, re.IGNORECASE):
            return False
    
    # Check for reasonable length
    if len(option_a) < 20 or len(option_a) > 250:
        return False
    
    if len(explanation) < 40:
        return False
    
    # Check if option A looks like a real definition (not just fragments)
    word_count = option_a.count(' ')
    if word_count < 3:
        return False
    
    # Check for excessive repetition (same phrase 4+ times)
    words = option_a.split()
    if len(words) > 15:
        # Check if same 4-word phrase repeats 4+ times
        for i in range(len(words) - 3):
            phrase = ' '.join(words[i:i+4])
            if option_a.count(phrase) > 3:
                return False
    
    return True

def clean_flashcard(flashcard):
    """Clean up flashcard content."""
    option_a = flashcard['options'][0]
    
    # Remove repetitive phrases (handle multiple patterns)
    patterns_to_remove = [
        (r'which gives you some nice\s+', ''),
        (r'(\w+)\s+\1\s+\1', r'\1'),
        (r'So I could say, well, okay, this is a\s+', ''),
        (r'financially backed guarantee around what\s+financially backed guarantee around what\s+', 'financially backed guarantee around what '),
        (r'lesson we\'re going to explore in this\s+lesson we\'re going to explore in this\s+', ''),
        (r'this is a\s+this is a\s+', ''),
        (r'subscription which gives you some nice subscription which gives you some nice', 'subscription'),
        (r'(\w+\s+){3,}\1', r'\1'),  # Remove repeated word sequences
        # Remove repeated phrases (2+ times)
        (r'(\w+\s+\w+\s+\w+\s+)\1+', r'\1'),  # 3-word phrases
        (r'(\w+\s+\w+\s+)\1+', r'\1'),  # 2-word phrases
    ]
    
    for pattern, replacement in patterns_to_remove:
        option_a = re.sub(pattern, replacement, option_a, flags=re.IGNORECASE)
    
    # Clean up explanation
    explanation = flashcard['explanation']
    service_name = flashcard['question'].replace('What is ', '').replace('What are ', '').replace('?', '')
    
    # Extract the actual definition part
    if service_name in explanation:
        parts = explanation.split(service_name, 1)
        if len(parts) > 1:
            definition = parts[1].strip()
            # Remove repetitive text
            for pattern, replacement in patterns_to_remove:
                definition = re.sub(pattern, replacement, definition, flags=re.IGNORECASE)
            
            explanation = f"{service_name} {definition[:200]}. This information comes directly from John Savill's AZ-900 YouTube course."
    
    # Clean repetitive text
    for pattern, replacement in patterns_to_remove:
        explanation = re.sub(pattern, replacement, explanation, flags=re.IGNORECASE)
    
    # Final cleanup
    option_a = re.sub(r'\s+', ' ', option_a).strip()
    explanation = re.sub(r'\s+', ' ', explanation).strip()
    
    flashcard['options'][0] = option_a[:150].strip()
    flashcard['explanation'] = explanation[:350].strip()
    
    return flashcard

def main():
    azure_dir = Path('/Users/djuanperry/study-buddy/Azure 900')
    input_file = azure_dir / 'azure-900-youtube-only.json'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        flashcards = json.load(f)
    
    print(f"Loaded {len(flashcards)} flashcards")
    
    # Clean all flashcards first
    cleaned_flashcards = []
    for flashcard in flashcards:
        cleaned = clean_flashcard(flashcard)
        # Keep flashcards with basic structure (question, options, answer)
        if cleaned.get('question') and cleaned.get('options') and len(cleaned.get('options', [])) >= 4:
            # Only filter out obviously broken ones
            option_a = cleaned['options'][0]
            if len(option_a) > 10 and not any(bad in option_a.lower() for bad in ['youtube', 'subscribe', 'hit the bell']):
                cleaned_flashcards.append(cleaned)
    
    # Re-number flashcards
    for i, flashcard in enumerate(cleaned_flashcards, 1):
        flashcard['id'] = i
    
    output_file = azure_dir / 'azure-900-youtube-only.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_flashcards, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Kept {len(cleaned_flashcards)} quality flashcards")
    print(f"📁 Saved to: {output_file}")

if __name__ == '__main__':
    main()

