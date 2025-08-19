# src/smart_contract_audit_agent/tools/audit_tools.py

"""
Tool definitions for the smart contract audit crew.

Exports:
- code_search_tool: RAG over your local repo or added sources
- file_read_tool: read file contents
- search_tool: web search via Serper
- scrape_tool: scrape a web page
- directory_listing_tool: list files in a directory (recursive)
- github_search_tool: search and fetch contracts from GitHub repositories
"""

from crewai_tools import (
    RagTool,
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    ScrapeWebsiteTool,
)
from crewai.tools import BaseTool
import requests
import re
import os
from typing import Type
from pydantic import BaseModel, Field

# ---------------------------
# RAG: semantic QA over your data
# ---------------------------
# Empty knowledge base until you add content.
# If you want this ready out of the box, uncomment the .add(...) lines below.
code_search_tool = RagTool()

# Example ingests (optional). Uncomment if you want auto-ingest on import.
# code_search_tool.add(data_type="directory", path=".")
# code_search_tool.add(data_type="directory", path="./src")
# code_search_tool.add(data_type="directory", path="./knowledge")

# ---------------------------
# File read: direct file contents
# ---------------------------
file_read_tool = FileReadTool()

# ---------------------------
# Directory listing: enumerate files recursively
# ---------------------------
# Keep the exported variable name to match your YAML.
directory_listing_tool = DirectoryReadTool(directory=".")

# ---------------------------
# Web search: Serper (needs SERPER_API_KEY in env)
# ---------------------------
search_tool = SerperDevTool()

# ---------------------------
# Web scraping: pull page content for analysis
# ---------------------------
scrape_tool = ScrapeWebsiteTool()

# ---------------------------
# Custom GitHub Repository Tool
# ---------------------------
class GitHubRepoInput(BaseModel):
    """Input schema for GitHub Repository Tool."""
    repo_url: str = Field(..., description="The GitHub repository URL (e.g., https://github.com/owner/repo)")
    file_pattern: str = Field(default="*.sol", description="File pattern to search for (default: *.sol)")

class GitHubRepositoryTool(BaseTool):
    name: str = "GitHub Repository Smart Contract Fetcher"
    description: str = "Fetches Solidity smart contracts from a GitHub repository URL. Provides complete contract code for analysis."
    args_schema: Type[BaseModel] = GitHubRepoInput

    def _run(self, repo_url: str, file_pattern: str = "*.sol") -> str:
        """
        Fetch Solidity files from a GitHub repository.
        """
        try:
            # Extract owner and repo from URL
            match = re.match(r'https://github\.com/([^/]+)/([^/]+)', repo_url.rstrip('/'))
            if not match:
                return f"Error: Invalid GitHub URL format. Expected: https://github.com/owner/repo"
            
            owner, repo = match.groups()
            
            # Get GitHub token from environment if available
            headers = {'Accept': 'application/vnd.github.v3.raw'}
            github_token = os.getenv('GITHUB_TOKEN')
            if github_token:
                headers['Authorization'] = f'token {github_token}'
            
            # Recursively search for Solidity files
            solidity_files = self._find_solidity_files(owner, repo, "", headers)
            
            if not solidity_files:
                return "No Solidity (.sol) files found in the repository."
            
            # Focus on main contract files first, prioritize src directory
            main_contracts = []
            other_files = []
            
            for file_path, download_url in solidity_files:
                # Check if it's a main contract (in src directory and not a test file)
                is_main_contract = (
                    ('src/' in file_path or file_path.startswith('src/')) and 
                    not file_path.endswith('.t.sol') and 
                    not file_path.endswith('.s.sol')  # exclude script files
                )
                
                if is_main_contract:
                    main_contracts.append((file_path, download_url))
                else:
                    other_files.append((file_path, download_url))
            
            # Process main contracts first with complete content
            results = []
            total_chars = 0
            
            # Add summary
            summary = f"=== REPOSITORY ANALYSIS SUMMARY ===\n"
            summary += f"Repository: {repo_url}\n"
            summary += f"Total files found: {len(solidity_files)}\n"
            summary += f"Main contracts: {len(main_contracts)}\n"
            summary += f"Supporting files: {len(other_files)}\n\n"
            results.append(summary)
            
            # Process main contracts first (give them full content)
            for file_path, download_url in main_contracts:
                try:
                    # Use raw GitHub API to get complete file content
                    raw_url = download_url.replace('https://api.github.com/repos/', 'https://raw.githubusercontent.com/').replace('/contents/', '/')
                    
                    file_response = requests.get(raw_url, headers={'Authorization': headers.get('Authorization', '')})
                    
                    if file_response.status_code == 200:
                        content = file_response.text
                        
                        file_output = f"\n=== MAIN CONTRACT: {file_path} ===\n"
                        file_output += f"Contract size: {len(content)} characters\n"
                        file_output += f"Complete source code:\n{content}\n"
                        
                        results.append(file_output)
                        total_chars += len(file_output)
                        
                        # Log for debugging
                        print(f"Processed MAIN CONTRACT {file_path}: {len(content)} characters")
                        
                    else:
                        error_msg = f"\n=== ERROR: {file_path} ===\nCould not fetch file (Status: {file_response.status_code})\n"
                        results.append(error_msg)
                        
                except Exception as file_error:
                    error_msg = f"\n=== ERROR: {file_path} ===\nException: {str(file_error)}\n"
                    results.append(error_msg)
            
            # Process supporting files (scripts, tests) with limited content
            for file_path, download_url in other_files:
                # Break if we're getting too much output
                if total_chars > 100000:
                    results.append("\n=== OUTPUT SIZE LIMIT REACHED ===\nAdditional supporting files truncated.\n")
                    break
                
                try:
                    raw_url = download_url.replace('https://api.github.com/repos/', 'https://raw.githubusercontent.com/').replace('/contents/', '/')
                    
                    file_response = requests.get(raw_url, headers={'Authorization': headers.get('Authorization', '')})
                    
                    if file_response.status_code == 200:
                        content = file_response.text
                        
                        file_output = f"\n=== SUPPORTING FILE: {file_path} ===\n"
                        file_output += f"File size: {len(content)} characters\n"
                        
                        # Limit supporting files to 2000 characters for brevity
                        if len(content) > 2000:
                            file_output += f"First 2000 characters:\n{content[:2000]}...\n[File truncated for brevity]\n"
                        else:
                            file_output += f"Complete content:\n{content}\n"
                        
                        results.append(file_output)
                        total_chars += len(file_output)
                        
                        print(f"Processed SUPPORTING FILE {file_path}: {len(content)} characters")
                        
                    else:
                        error_msg = f"\n=== ERROR: {file_path} ===\nCould not fetch file (Status: {file_response.status_code})\n"
                        results.append(error_msg)
                        
                except Exception as file_error:
                    error_msg = f"\n=== ERROR: {file_path} ===\nException: {str(file_error)}\n"
                    results.append(error_msg)
            
            full_output = "".join(results)
            
            # Update summary with final size
            final_summary = summary.replace("Supporting files:", f"Supporting files: {len(other_files)}\nTotal output size: {len(full_output)} characters\n")
            
            return full_output.replace(summary, final_summary)
            
        except Exception as e:
            return f"Error: {str(e)}"

    def _find_solidity_files(self, owner: str, repo: str, path: str, headers: dict) -> list:
        """
        Recursively find all .sol files in the repository.
        """
        solidity_files = []
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        
        try:
            # Remove Accept header for directory listing
            list_headers = {k: v for k, v in headers.items() if k != 'Accept'}
            response = requests.get(api_url, headers=list_headers)
            
            if response.status_code != 200:
                return solidity_files
            
            contents = response.json()
            
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith('.sol'):
                    solidity_files.append((item['path'], item['download_url']))
                elif item['type'] == 'dir':
                    # Recursively search subdirectories
                    solidity_files.extend(self._find_solidity_files(owner, repo, item['path'], headers))
            
        except Exception:
            pass  # Ignore errors in subdirectories
        
        return solidity_files

# Create instance of the GitHub tool
github_repo_tool = GitHubRepositoryTool()

__all__ = [
    "code_search_tool",
    "file_read_tool",
    "search_tool",
    "scrape_tool",
    "directory_listing_tool",
    "github_repo_tool",
]
