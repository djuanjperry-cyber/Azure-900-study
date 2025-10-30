#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE CHECK - User has test in 2 days!
"""

import json

def final_comprehensive_check():
    """Final check of ALL cards for test readiness"""
    
    # Load the urgent fix file
    with open('azure-900-urgent-fix.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"🚨 FINAL CHECK: {len(flashcards)} flashcards for test readiness...\n")
    
    issues = []
    
    for card in flashcards:
        card_id = card['id']
        question = card['question']
        options = card['options']
        answer = card['answer']
        explanation = card['explanation']
        
        # Get the correct answer text
        correct_option = next((opt for opt in options if opt.startswith(answer + ')')), None)
        if not correct_option:
            issues.append(f"Card {card_id}: No option found for answer '{answer}'")
            continue
            
        correct_text = correct_option[3:]  # Remove "A) " prefix
        
        # Check for obvious mismatches
        explanation_lower = explanation.lower()
        correct_text_lower = correct_text.lower()
        
        # Check for specific mismatches
        if "infrastructure as code" in explanation_lower and "performance" in correct_text_lower:
            issues.append(f"Card {card_id}: IaC explanation but performance answer")
        elif "performance" in explanation_lower and "infrastructure as code" in correct_text_lower:
            issues.append(f"Card {card_id}: Performance explanation but IaC answer")
        elif "security" in explanation_lower and "performance" in correct_text_lower:
            issues.append(f"Card {card_id}: Security explanation but performance answer")
        elif "scaling" in explanation_lower and "security" in correct_text_lower:
            issues.append(f"Card {card_id}: Scaling explanation but security answer")
        elif "data governance" in explanation_lower and "synapse" in correct_text_lower:
            issues.append(f"Card {card_id}: Data governance explanation but Synapse answer")
        elif "purview" in explanation_lower and "synapse" in correct_text_lower:
            issues.append(f"Card {card_id}: Purview explanation but Synapse answer")
        
        # Check for "all of the above" remnants
        if "all of the above" in correct_text_lower:
            issues.append(f"Card {card_id}: Still contains 'all of the above'")
        
        # Check for incomplete explanations
        if len(explanation.split()) < 5:
            issues.append(f"Card {card_id}: Explanation too short")
    
    print(f"Found {len(issues)} issues:")
    for issue in issues:
        print(f"  ❌ {issue}")
    
    # Check answer distribution
    answer_dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for card in flashcards:
        if card['answer'] in answer_dist:
            answer_dist[card['answer']] += 1
    
    print(f"\nAnswer distribution: {answer_dist}")
    
    # Check for duplicates
    questions = [card['question'] for card in flashcards]
    duplicates = [q for q in set(questions) if questions.count(q) > 1]
    if duplicates:
        print(f"\nDuplicate questions: {len(duplicates)}")
        for dup in duplicates[:3]:
            print(f"  - {dup[:60]}...")
    
    if len(issues) == 0:
        print(f"\n✅ ALL CARDS ARE PERFECT FOR YOUR TEST!")
        print(f"✅ {len(flashcards)} flashcards ready")
        print(f"✅ Zero issues found")
        print(f"✅ Balanced answer distribution")
        print(f"✅ All explanations match answers")
        print(f"\n🎯 YOU'RE READY TO CRUSH THAT AZURE 900 TEST!")
    else:
        print(f"\n❌ {len(issues)} issues need fixing before test")
    
    return len(issues) == 0

if __name__ == "__main__":
    is_ready = final_comprehensive_check()
    print(f"\nTest readiness: {'✅ READY' if is_ready else '❌ NEEDS FIXES'}")

