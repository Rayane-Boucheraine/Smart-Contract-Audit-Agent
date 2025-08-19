# Smart Contract Audit Agent

An AI-powered smart contract security auditing system built with [CrewAI](https://crewai.com). This tool performs comprehensive security audits of Solidity smart contracts by fetching them directly from GitHub repositories and analyzing them for vulnerabilities, code quality issues, and gas optimization opportunities.

## 🚀 Features

- **GitHub Integration**: Automatically fetch and analyze smart contracts from any public GitHub repository
- **Comprehensive Security Analysis**: Detects reentrancy, access control issues, integer overflow, and other SWC vulnerabilities
- **Code Quality Review**: Identifies gas optimization opportunities, style violations, and maintainability issues
- **AI-Powered Analysis**: Uses advanced AI agents specialized in smart contract security and code review
- **Automated Report Generation**: Creates detailed audit reports in Markdown format

## 📋 Prerequisites

- Python >=3.10 <3.14
- OpenAI API key
- Optional: GitHub token for higher API rate limits

## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone <your-repo-url>
cd smart_contract_audit_agent
```

2. **Install dependencies:**

```bash
pip install uv
crewai install
```

3. **Configure environment variables:**
   Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here  # Optional but recommended
SERPER_API_KEY=your_serper_api_key   # Optional for web search
```

## 🚀 Usage

### Audit a GitHub Repository

```bash
python src/smart_contract_audit_agent/main.py https://github.com/owner/repository-name
```

**Examples:**

```bash
# Audit a DeFi protocol
python src/smart_contract_audit_agent/main.py https://github.com/Uniswap/v3-core

# Audit a contest repository
python src/smart_contract_audit_agent/main.py https://github.com/CodeHawks-Contests/2025-07-last-man-standing

# Audit OpenZeppelin contracts
python src/smart_contract_audit_agent/main.py https://github.com/OpenZeppelin/openzeppelin-contracts
```

## 📊 Output

The system generates a comprehensive audit report saved as `final_audit_report.md` containing:

1. **Executive Summary** - Overview of the contracts analyzed
2. **Critical Vulnerabilities** - High-severity security issues requiring immediate attention
3. **Medium/Low Priority Issues** - Important but less critical findings
4. **Code Quality Recommendations** - Style improvements and best practices
5. **Remediation Priority List** - Ordered action items for developers

## 🤖 AI Agents

The system uses two specialized AI agents:

- **Senior Smart Contract Security Auditor**: Focuses on identifying security vulnerabilities, reentrancy issues, access control problems, and other critical security concerns
- **Smart Contract Code Review Specialist**: Analyzes code quality, gas optimization opportunities, style guide compliance, and maintainability

## 🔍 Supported Vulnerability Classes

- **SWC-107**: Reentrancy
- **SWC-101**: Integer Overflow/Underflow
- **SWC-132**: Access Control Issues
- **SWC-136**: Unchecked Return Values
- **Gas Optimization Issues**
- **Style Guide Violations**
- **Documentation Issues**

## 🛠️ Technical Architecture

```
src/smart_contract_audit_agent/
├── main.py                 # Entry point
├── crew.py                 # CrewAI configuration
├── config/
│   ├── agents.yaml         # AI agent configurations
│   └── tasks.yaml          # Task definitions
└── tools/
    └── audit_tools.py      # GitHub fetching and analysis tools
```

## 🧪 Example Output

When you run an audit, you'll see:

```
## Welcome to Smart Contract Audit Agent! ##
----------------------------------------------
Auditing GitHub repository: https://github.com/example/repo
Processed MAIN CONTRACT src/Token.sol: 2847 characters
Processed SUPPORTING FILE test/Token.t.sol: 1234 characters
```

The final report will include specific findings like:

- **Critical**: Reentrancy vulnerability in `withdraw()` function
- **Medium**: Missing access control on `mint()` function
- **Low**: Incomplete NatSpec documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [CrewAI](https://crewai.com)
- Powered by OpenAI GPT models
- Inspired by the need for automated smart contract security analysis

## 📞 Support

For questions, issues, or feature requests:

- Open an issue on GitHub
- Check the [CrewAI documentation](https://docs.crewai.com)
- Join the [CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)

---

**⚠️ Disclaimer**: This tool is for educational and development purposes. Always conduct professional security audits before deploying smart contracts to production.
