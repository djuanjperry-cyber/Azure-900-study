#!/usr/bin/env python3
"""
Analyze Azure flashcards to identify questions that could be split into multiple cards
"""

import json
import re

def analyze_flashcards():
    """Analyze flashcards for splitting opportunities"""
    
    # Load the main flashcard file
    with open('azure-900-ultimate-randomized.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"Total flashcards: {len(flashcards)}")
    print("\nAnalyzing for splitting opportunities...\n")
    
    split_candidates = []
    
    for card in flashcards:
        question = card['question']
        options = card['options']
        explanation = card['explanation']
        
        # Look for questions that mention multiple services/concepts
        if any(word in question.lower() for word in ['services', 'features', 'benefits', 'capabilities', 'components']):
            split_candidates.append({
                'id': card['id'],
                'question': question,
                'category': card['category'],
                'reason': 'Mentions multiple services/features'
            })
        
        # Look for explanations that list multiple items
        if ';' in explanation or 'and' in explanation.lower():
            split_candidates.append({
                'id': card['id'],
                'question': question,
                'category': card['category'],
                'reason': 'Explanation lists multiple items'
            })
    
    print(f"Found {len(split_candidates)} potential candidates for splitting:\n")
    
    for i, candidate in enumerate(split_candidates[:10]):  # Show first 10
        print(f"{i+1}. ID {candidate['id']}: {candidate['question'][:80]}...")
        print(f"   Reason: {candidate['reason']}")
        print(f"   Category: {candidate['category']}\n")
    
    if len(split_candidates) > 10:
        print(f"... and {len(split_candidates) - 10} more candidates")

if __name__ == "__main__":
    analyze_flashcards()

