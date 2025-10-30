#!/usr/bin/env python3
"""
Fix the remaining 6 cards with better explanation cleaning
"""

import json
import re

def fix_remaining_cards():
    """Fix the 6 cards with contradiction words in explanations"""
    
    # Load the accuracy-fixed flashcard file
    with open('azure-900-accuracy-fixed.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"Fixing remaining cards with contradiction words...\n")
    
    # Cards that need fixing (based on manual review)
    cards_to_fix = [8, 17, 35, 76, 95, 96]
    
    fixed_count = 0
    
    for card in flashcards:
        if card['id'] in cards_to_fix:
            explanation = card['explanation']
            
            # Clean up explanations more precisely
            # Remove trailing incomplete sentences and notes
            cleaned_explanation = re.sub(r'\. \(Note:.*$', '.', explanation)
            cleaned_explanation = re.sub(r'\. \(.*$', '.', cleaned_explanation)
            
            # Fix specific issues
            if card['id'] == 8:
                cleaned_explanation = "Azure Availability Zones provide protection against data center failures by distributing resources across physically separate data centers within the same region, each with independent power, cooling, and networking infrastructure."
            elif card['id'] == 17:
                cleaned_explanation = "Azure Cosmos DB is a globally distributed, multi-model database service that provides automatic scaling, global distribution, and multiple consistency models for modern applications."
            elif card['id'] == 35:
                cleaned_explanation = "Azure DDoS Protection provides always-on monitoring and automatic attack mitigation to protect Azure resources from distributed denial-of-service attacks."
            elif card['id'] == 76:
                cleaned_explanation = "Azure Availability Sets protect against hardware failures within a data center by distributing virtual machines across multiple physical servers and update domains."
            elif card['id'] == 95:
                cleaned_explanation = "Azure Availability Zones provide fault tolerance by distributing resources across physically separate data centers within the same region, ensuring high availability even if one zone fails."
            elif card['id'] == 96:
                cleaned_explanation = "Azure Availability Zones provide high availability by ensuring 99.99% uptime SLA through redundant infrastructure and automatic failover capabilities."
            
            if cleaned_explanation != explanation:
                card['explanation'] = cleaned_explanation
                print(f"Card {card['id']}: Cleaned explanation")
                fixed_count += 1
    
    print(f"\nFixed {fixed_count} explanations")
    
    # Save the final cleaned flashcards
    with open('azure-900-final-clean.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"Saved {len(flashcards)} flashcards to azure-900-final-clean.json")
    
    # Verify no contradiction words remain
    contradiction_count = 0
    for card in flashcards:
        explanation = card['explanation'].lower()
        if 'however' in explanation or (' but ' in explanation and 'networking' not in explanation):
            contradiction_count += 1
            print(f"Still has contradiction: Card {card['id']}")
    
    print(f"Remaining contradiction words: {contradiction_count}")

if __name__ == "__main__":
    fix_remaining_cards()

