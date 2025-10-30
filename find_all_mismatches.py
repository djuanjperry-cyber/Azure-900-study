#!/usr/bin/env python3
"""
COMPREHENSIVE MISMATCH DETECTION: Find ALL remaining issues
"""

import json

def find_all_mismatches():
    """Find every single mismatch in all cards"""
    
    # Load the emergency fix file
    with open('azure-900-emergency-fix.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"🔍 COMPREHENSIVE MISMATCH SCAN: Checking ALL {len(flashcards)} cards...\n")
    
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
        
        # Check for obvious mismatches
        explanation_lower = explanation.lower()
        correct_text_lower = correct_text.lower()
        
        # Check for specific mismatches
        issues = []
        
        # Infrastructure as Code mismatches
        if "infrastructure as code" in explanation_lower and "performance" in correct_text_lower:
            issues.append("IaC explanation but performance answer")
        elif "performance" in explanation_lower and "infrastructure as code" in correct_text_lower:
            issues.append("Performance explanation but IaC answer")
        
        # Security mismatches
        if "security" in explanation_lower and "performance" in correct_text_lower:
            issues.append("Security explanation but performance answer")
        elif "performance" in explanation_lower and "security" in correct_text_lower:
            issues.append("Performance explanation but security answer")
        
        # Scaling mismatches
        if "scaling" in explanation_lower and "security" in correct_text_lower:
            issues.append("Scaling explanation but security answer")
        elif "security" in explanation_lower and "scaling" in correct_text_lower:
            issues.append("Security explanation but scaling answer")
        
        # Data governance mismatches
        if "data governance" in explanation_lower and "synapse" in correct_text_lower:
            issues.append("Data governance explanation but Synapse answer")
        elif "purview" in explanation_lower and "synapse" in correct_text_lower:
            issues.append("Purview explanation but Synapse answer")
        
        # Resource Groups mismatches
        if "apply governance policies" in explanation_lower and "eliminate governance" in correct_text_lower:
            issues.append("Apply governance explanation but eliminate governance answer")
        elif "eliminate governance" in explanation_lower and "apply governance policies" in correct_text_lower:
            issues.append("Eliminate governance explanation but apply governance answer")
        
        # Resource Manager mismatches
        if "unified management and deployment" in explanation_lower and "automatic scaling" in correct_text_lower:
            issues.append("Unified management explanation but automatic scaling answer")
        elif "automatic scaling" in explanation_lower and "unified management and deployment" in correct_text_lower:
            issues.append("Automatic scaling explanation but unified management answer")
        
        # Availability mismatches
        if "distributing resources across physically separate data centers" in explanation_lower and "using virtual machines only" in correct_text_lower:
            issues.append("Distribute resources explanation but VMs only answer")
        elif "using virtual machines only" in explanation_lower and "distributing resources across physically separate data centers" in correct_text_lower:
            issues.append("VMs only explanation but distribute resources answer")
        
        # Check for "all of the above" remnants
        if "all of the above" in correct_text_lower:
            issues.append("Still contains 'all of the above'")
        
        if issues:
            mismatches.append(f"Card {card_id}: {', '.join(issues)}")
            print(f"❌ Card {card_id}: {question[:60]}...")
            print(f"   Answer: {correct_text}")
            print(f"   Issues: {', '.join(issues)}")
            print(f"   Explanation: {explanation[:100]}...")
            print()
    
    print(f"\nFound {len(mismatches)} mismatches:")
    for mismatch in mismatches:
        print(f"  - {mismatch}")
    
    return mismatches

if __name__ == "__main__":
    mismatches = find_all_mismatches()
    print(f"\nTotal mismatches found: {len(mismatches)}")
    if len(mismatches) > 0:
        print("❌ STILL HAVE ISSUES - Need to fix these!")
    else:
        print("✅ ALL CARDS ARE PERFECT!")

