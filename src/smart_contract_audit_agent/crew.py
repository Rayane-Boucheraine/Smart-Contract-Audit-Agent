from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from textwrap import dedent

# Import your tools and instantiate them here
from smart_contract_audit_agent.tools.audit_tools import (
    file_read_tool, 
    code_search_tool, 
    search_tool, 
    scrape_tool, 
    directory_listing_tool,
    github_repo_tool
)

@CrewBase
class SmartContractAuditAgentCrew():
    """SmartContractAuditAgent crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def senior_smart_contract_security_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_smart_contract_security_auditor'],
            verbose=True,
            tools=[github_repo_tool, code_search_tool, search_tool, scrape_tool]
        )

    @agent
    def smart_contract_code_review_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['smart_contract_code_review_specialist'],
            verbose=True,
            tools=[github_repo_tool, code_search_tool]
        )

    @task
    def security_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_audit_task'],
            agent=self.senior_smart_contract_security_auditor()
        )

    @task
    def code_quality_and_gas_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_quality_and_gas_optimization_task'],
            agent=self.smart_contract_code_review_specialist()
        )

    @task
    def final_report_task(self) -> Task:
        return Task(
            description=dedent(
                """\
                Create a comprehensive final audit report combining the security and code quality findings 
                from the previous tasks.
                
                Based on the previous task outputs, create a structured report with:
                1. Executive Summary (2-3 sentences about the contracts analyzed)
                2. Critical Vulnerabilities (top 3 most severe issues found)
                3. Medium/Low Priority Issues  
                4. Code Quality Recommendations
                5. Remediation Priority List
                
                Focus on the actual findings from the contract analysis.
                Keep the report concise and actionable (under 1000 words).
                
                Generate the report content directly - do not try to read any files or websites.
                """
            ),
            expected_output="A comprehensive final audit report with executive summary, prioritized vulnerabilities, and remediation steps",
            tools=[],
            agent=self.senior_smart_contract_security_auditor(),
            output_file="final_audit_report.md",
            context=[self.security_audit_task(), self.code_quality_and_gas_optimization_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SmartContractAuditAgent crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )