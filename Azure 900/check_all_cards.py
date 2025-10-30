#!/usr/bin/env python3
"""
Check all randomized cards for answer-explanation mismatches
"""

import json
import re

def check_all_randomized_cards():
    """Check all cards for answer-explanation consistency"""
    
    # Load the corrected flashcard file
    with open('azure-900-corrected.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"Checking {len(flashcards)} flashcards for answer-explanation consistency...\n")
    
    mismatches = []
    
    for card in flashcards:
        card_id = card['id']
        question = card['question']
        options = card['options']
        answer = card['answer']
        explanation = card['explanation']
        
        # Get the correct answer text
        correct_option = next((opt for opt in options if opt.startswith(answer + ')')), None)
        if not correct_option:
            mismatches.append(f"Card {card_id}: No option found for answer '{answer}'")
            continue
            
        correct_text = correct_option[3:]  # Remove "A) " prefix
        
        # Check if explanation supports the answer
        explanation_lower = explanation.lower()
        correct_text_lower = correct_text.lower()
        
        # Look for key terms from the correct answer in the explanation
        key_terms = [word for word in correct_text_lower.split() if len(word) > 3]
        explanation_matches = sum(1 for term in key_terms if term in explanation_lower)
        
        # Check for obvious mismatches
        issues = []
        
        # Check if explanation contradicts the answer
        if "however" in explanation_lower or "but" in explanation_lower:
            issues.append("Explanation contains contradiction words")
            
        # Check for specific mismatches based on common patterns
        if "infrastructure as code" in correct_text_lower and "performance" in explanation_lower:
            issues.append("IaC answer but performance explanation")
            
        if "performance" in correct_text_lower and "infrastructure as code" in explanation_lower:
            issues.append("Performance answer but IaC explanation")
            
        if "security" in correct_text_lower and "performance" in explanation_lower:
            issues.append("Security answer but performance explanation")
            
        if "scaling" in correct_text_lower and "security" in explanation_lower:
            issues.append("Scaling answer but security explanation")
            
        # Check if explanation is too generic
        if len(explanation.split()) < 8:
            issues.append("Explanation too short")
            
        # Check for obvious wrong answers
        if "all of the above" in correct_text_lower:
            issues.append("Still contains 'all of the above'")
            
        if issues:
            mismatches.append(f"Card {card_id}: {', '.join(issues)}")
            print(f"❌ Card {card_id}: {question[:60]}...")
            print(f"   Answer: {correct_text}")
            print(f"   Issues: {', '.join(issues)}")
            print(f"   Explanation: {explanation[:100]}...")
            print()
    
    print(f"\nFound {len(mismatches)} potential mismatches:")
    for mismatch in mismatches:
        print(f"  - {mismatch}")
    
    # Check answer distribution
    answer_dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for card in flashcards:
        if card['answer'] in answer_dist:
            answer_dist[card['answer']] += 1
    
    print(f"\nAnswer distribution: {answer_dist}")
    
    return len(mismatches) == 0

if __name__ == "__main__":
    is_consistent = check_all_randomized_cards()
    print(f"\nOverall consistency check: {'✅ PASSED' if is_consistent else '❌ ISSUES FOUND'}")

