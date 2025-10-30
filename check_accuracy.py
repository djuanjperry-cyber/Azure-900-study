#!/usr/bin/env python3
"""
Double-check all Azure flashcards for accuracy
"""

import json
import re

def check_flashcard_accuracy():
    """Check all flashcards for answer accuracy and consistency"""
    
    # Load the accuracy-fixed flashcard file
    with open('azure-900-accuracy-fixed.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"Checking {len(flashcards)} flashcards for accuracy...\n")
    
    issues_found = []
    
    for card in flashcards:
        card_id = card['id']
        question = card['question']
        options = card['options']
        answer = card['answer']
        explanation = card['explanation']
        
        # Get the correct answer text
        correct_option = next((opt for opt in options if opt.startswith(answer + ')')), None)
        if not correct_option:
            issues_found.append(f"Card {card_id}: No option found for answer '{answer}'")
            continue
            
        correct_text = correct_option[3:]  # Remove "A) " prefix
        
        # Check if the explanation mentions the correct answer
        explanation_lower = explanation.lower()
        correct_text_lower = correct_text.lower()
        
        # Look for key terms from the correct answer in the explanation
        key_terms = [word for word in correct_text_lower.split() if len(word) > 3]
        explanation_matches = sum(1 for term in key_terms if term in explanation_lower)
        
        # Check for potential issues
        issues = []
        
        # Check if explanation contradicts the answer
        if "however" in explanation_lower or "but" in explanation_lower:
            issues.append("Explanation contains contradiction words")
            
        # Check if the explanation is too generic
        if len(explanation.split()) < 10:
            issues.append("Explanation too short")
            
        # Check if answer seems wrong based on common Azure knowledge
        if "automatic scaling" in correct_text_lower and "authentication" in question.lower():
            issues.append("MFA question with scaling answer - likely incorrect")
            
        if "performance" in correct_text_lower and "security" in question.lower():
            issues.append("Security question with performance answer - likely incorrect")
            
        # Check for obvious mismatches
        if "all of the above" in correct_text_lower:
            issues.append("Still contains 'all of the above'")
            
        if issues:
            issues_found.append(f"Card {card_id}: {', '.join(issues)}")
            print(f"❌ Card {card_id}: {question[:60]}...")
            print(f"   Answer: {correct_text}")
            print(f"   Issues: {', '.join(issues)}")
            print()
    
    print(f"\nFound {len(issues_found)} potential issues:")
    for issue in issues_found:
        print(f"  - {issue}")
    
    # Check answer distribution
    answer_dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for card in flashcards:
        if card['answer'] in answer_dist:
            answer_dist[card['answer']] += 1
    
    print(f"\nAnswer distribution: {answer_dist}")
    
    # Check for duplicate questions
    questions = [card['question'] for card in flashcards]
    duplicates = [q for q in set(questions) if questions.count(q) > 1]
    if duplicates:
        print(f"\nDuplicate questions found: {len(duplicates)}")
        for dup in duplicates[:3]:  # Show first 3
            print(f"  - {dup[:60]}...")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    is_accurate = check_flashcard_accuracy()
    print(f"\nOverall accuracy check: {'✅ PASSED' if is_accurate else '❌ ISSUES FOUND'}")
