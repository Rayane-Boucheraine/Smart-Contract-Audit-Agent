#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the correct class name we defined in crew.py
from smart_contract_audit_agent.crew import SmartContractAuditAgentCrew

def run():
    """
    Run the crew with command line arguments.
    """
    if len(sys.argv) < 2:
        print("Error: Please provide a GitHub repository URL")
        print("Usage: python src/smart_contract_audit_agent/main.py <github_url>")
        print("Example: python src/smart_contract_audit_agent/main.py https://github.com/owner/repo")
        sys.exit(1)
    
    contract_source = sys.argv[1]
    
    if not contract_source.startswith('https://github.com'):
        print("Error: Please provide a valid GitHub repository URL")
        print("Expected format: https://github.com/owner/repo")
        sys.exit(1)
    
    inputs = {
        'contract_source': contract_source
    }
    
    try:
        SmartContractAuditAgentCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    print("## Welcome to Smart Contract Audit Agent! ##")
    print('----------------------------------------------')
    
    if len(sys.argv) < 2:
        print("Error: GitHub repository URL required")
        print("Usage: python src/smart_contract_audit_agent/main.py <github_url>")
        print("Example: python src/smart_contract_audit_agent/main.py https://github.com/OpenZeppelin/openzeppelin-contracts")
        sys.exit(1)
        
    contract_source = sys.argv[1]
    print(f"Auditing GitHub repository: {contract_source}")
    
    if not contract_source.startswith('https://github.com'):
        print("Error: Please provide a valid GitHub repository URL")
        sys.exit(1)

    run_inputs = {'contract_source': contract_source}
    SmartContractAuditAgentCrew().crew().kickoff(inputs=run_inputs)