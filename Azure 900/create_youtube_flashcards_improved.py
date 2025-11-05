import json
import os
import re
from pathlib import Path
from collections import defaultdict

def extract_clean_text_from_vtt(vtt_path):
    """Extract clean transcript text from VTT file."""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    transcript = []
    for i, line in enumerate(lines):
        line = line.strip()
        
        if not line:
            continue
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        if '-->' in line:
            continue
        if line.startswith('align:'):
            continue
        
        clean_line = re.sub(r'<[^>]+>', '', line)
        clean_line = re.sub(r'\s+', ' ', clean_line).strip()
        
        if len(clean_line) > 5 and not clean_line.isdigit():
            transcript.append(clean_line)
    
    full_text = ' '.join(transcript)
    full_text = re.sub(r'\s+', ' ', full_text)
    return full_text

def find_azure_service_definitions(text):
    """Find definitions of Azure services and concepts."""
    azure_services = {
        'Azure Resource Manager': ['ARM', 'Resource Manager'],
        'Resource Group': ['resource group', 'resource groups'],
        'Subscription': ['subscription', 'subscriptions'],
        'Management Group': ['management group', 'management groups'],
        'Availability Zone': ['availability zone', 'availability zones'],
        'Region': ['region', 'regions'],
        'Azure Advisor': ['Azure Advisor', 'advisor'],
        'Azure Monitor': ['Azure Monitor', 'monitor'],
        'Key Vault': ['Key Vault', 'key vault'],
        'Azure Firewall': ['Azure Firewall', 'firewall'],
        'Network Security Group': ['NSG', 'Network Security Group', 'network security groups'],
        'Azure Active Directory': ['Azure AD', 'Azure Active Directory', 'Entra ID'],
        'RBAC': ['RBAC', 'Role-Based Access Control'],
        'Azure Policy': ['Azure Policy', 'policy'],
        'Azure Blob Storage': ['Blob Storage', 'blob storage'],
        'Azure SQL Database': ['Azure SQL', 'SQL Database'],
        'Virtual Machine': ['Virtual Machine', 'VM', 'virtual machines'],
        'App Service': ['App Service', 'app service'],
        'Azure Functions': ['Azure Functions', 'Functions'],
        'Load Balancer': ['Load Balancer', 'load balancer'],
        'Application Gateway': ['Application Gateway', 'application gateway'],
        'Virtual Network': ['Virtual Network', 'VNet', 'virtual network'],
        'Azure Cost Management': ['Cost Management', 'cost management'],
        'Reserved Instances': ['Reserved Instances', 'reserved instances'],
        'Service Level Agreement': ['SLA', 'Service Level Agreement'],
    }
    
    definitions = []
    sentences = re.split(r'[.!?]\s+', text)
    
    for sentence in sentences:
        if len(sentence) < 50:
            continue
        
        sentence_lower = sentence.lower()
        
        for service, keywords in azure_services.items():
            for keyword in keywords:
                if keyword.lower() in sentence_lower:
                    if any(word in sentence.lower() for word in ['is ', 'are ', 'provides', 'allows', 'helps', 'enables']):
                        definitions.append({
                            'service': service,
                            'sentence': sentence[:300],
                            'keyword': keyword
                        })
                        break
    
    return definitions

def create_question_from_definition(def_data, video_title, flashcard_id):
    """Create a well-formed flashcard from definition."""
    service = def_data['service']
    sentence = def_data['sentence']
    
    # Extract the definition part
    definition = sentence
    if 'is ' in sentence.lower():
        parts = re.split(r'is\s+', sentence, 1, flags=re.IGNORECASE)
        if len(parts) > 1:
            definition = parts[1].strip()
    elif 'are ' in sentence.lower():
        parts = re.split(r'are\s+', sentence, 1, flags=re.IGNORECASE)
        if len(parts) > 1:
            definition = parts[1].strip()
    elif 'provides' in sentence.lower():
        parts = re.split(r'provides?\s+', sentence, 1, flags=re.IGNORECASE)
        if len(parts) > 1:
            definition = parts[1].strip()
    
    if len(definition) < 30:
        definition = sentence[:200]
    
    definition = definition[:150].strip()
    if definition.endswith(','):
        definition = definition[:-1]
    
    question = f"What is {service}?"
    if 'are' in sentence.lower() or service.endswith('s'):
        question = f"What are {service}?"
    
    explanation = f"{service} {definition}. This information comes directly from John Savill's AZ-900 YouTube course video: {video_title}."
    
    # Create realistic distractors based on service type
    distractors = get_distractors_for_service(service)
    
    flashcard = {
        'id': flashcard_id,
        'question': question,
        'options': [
            f"A) {definition}",
            f"B) {distractors[0]}",
            f"C) {distractors[1]}",
            f"D) {distractors[2]}"
        ],
        'answer': 'A',
        'explanation': explanation,
        'category': video_title[:60],
        'source': f'John Savill AZ-900 YouTube Course - {video_title}'
    }
    
    return flashcard

def get_distractors_for_service(service):
    """Get realistic distractors based on service category."""
    service_lower = service.lower()
    
    if 'storage' in service_lower or 'blob' in service_lower:
        return [
            "A compute service for running virtual machines",
            "A networking service for load balancing",
            "A security service for identity management"
        ]
    elif 'network' in service_lower or 'firewall' in service_lower or 'nsg' in service_lower:
        return [
            "A storage service for unstructured data",
            "A compute service for containers",
            "A database service for relational data"
        ]
    elif 'security' in service_lower or 'key vault' in service_lower or 'rbac' in service_lower or 'entra' in service_lower or 'active directory' in service_lower:
        return [
            "A compute service for running applications",
            "A storage service for file shares",
            "A networking service for VPN connections"
        ]
    elif 'monitor' in service_lower or 'advisor' in service_lower:
        return [
            "A storage service for backup and recovery",
            "A networking service for traffic routing",
            "A compute service for serverless functions"
        ]
    elif 'compute' in service_lower or 'virtual machine' in service_lower or 'app service' in service_lower or 'function' in service_lower:
        return [
            "A storage service for object data",
            "A networking service for private connections",
            "A security service for access control"
        ]
    elif 'cost' in service_lower or 'pricing' in service_lower:
        return [
            "A monitoring service for application performance",
            "A security service for threat detection",
            "A compute service for batch processing"
        ]
    else:
        return [
            "A service for managing network traffic",
            "A storage solution for structured data",
            "A security service for identity management"
        ]

def main():
    azure_dir = Path('/Users/djuanperry/study-buddy/Azure 900')
    vtt_files = sorted([f for f in azure_dir.glob('*.vtt') if 'en.vtt' in f.name])
    
    all_flashcards = []
    flashcard_id = 1
    
    print(f"Processing {len(vtt_files)} VTT files from John Savill's AZ-900 YouTube course...")
    
    for vtt_file in vtt_files:
        print(f"\nProcessing: {vtt_file.name[:60]}...")
        try:
            transcript = extract_clean_text_from_vtt(vtt_file)
            
            if len(transcript) < 200:
                print(f"  Skipping - transcript too short")
                continue
            
            video_title = vtt_file.stem.replace('.en', '')
            
            definitions = find_azure_service_definitions(transcript)
            
            print(f"  Found {len(definitions)} Azure service definitions")
            
            seen_services = set()
            for def_data in definitions:
                service = def_data['service']
                if service not in seen_services:
                    flashcard = create_question_from_definition(def_data, video_title, flashcard_id)
                    if flashcard and len(flashcard['options'][0]) < 200:
                        all_flashcards.append(flashcard)
                        flashcard_id += 1
                        seen_services.add(service)
            
        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    output_file = azure_dir / 'azure-900-youtube-only.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_flashcards, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Created {len(all_flashcards)} flashcards exclusively from John Savill's YouTube videos")
    print(f"📁 Saved to: {output_file}")
    
    return output_file

if __name__ == '__main__':
    main()

