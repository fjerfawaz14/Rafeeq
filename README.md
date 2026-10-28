# Rafeeq — Agentic AI Capstone Project

## About the Project

Rafeeq is the final capstone project I developed as part of the [SDAIA Academy Agentic AI Program](https://github.com/SDAIAAcademy/agentic-ai).

The project demonstrates the practical application of agentic AI concepts, including tool use, MCP-style communication, human approval for simulated actions, and security testing.

Rafeeq is a prototype agent designed to assist with municipal-service inquiries. It can search policy examples, calculate illustrative fees, inspect synthetic permit statuses, list demonstration appointment slots, and request human approval before simulated write actions.

**Important:** This is an independent educational prototype developed for the program's final project. It uses synthetic demonstration data and is not connected to a real municipality or any live permit, email, or booking system.

## Program Reference

- **Program:** SDAIA Academy Agentic AI
- **Project:** Rafeeq — Agentic AI Capstone Project
- **Program repository:** https://github.com/SDAIAAcademy/agentic-ai

## Features

- Tool-using LLM agent
- MCP-style policy search server
- Multiple local tools for municipal-service scenarios
- Human approval prompts for simulated write actions
- Email destination allowlist
- Step limit and approximate context-size limit
- Security unit tests
- JSONL evaluation tasks and CSV reports
- Basic error analysis

## Project Files

- `AGENTS.md`: Agent instructions and operating limits
- `requirements.txt`: Python dependencies
- `mcp_server.py`: Policy search server
- `rafeeq.py`: Agent, tools, and security checks
- `security_test.py`: Security unit tests
- `tasks.jsonl`: Evaluation tasks
- `evaluate.py`: Evaluation runner
- `SECURITY_NOTE.md`: Threat analysis and security limitations
- `README.md`: Project documentation

## Requirements

- Python 3.10 or newer
- An OpenRouter API key
- Internet access for model API requests

## Installation

### 1. Install Dependencies

Open a terminal in the project directory and run:

```powershell
py -m pip install -r requirements.txt
```

### 2. Configure the API Key

Create or update the `rafeeq_standalone.env` file in the project directory:

```text
OPENROUTER_API_KEY=YOUR_API_KEY
```

Replace `YOUR_API_KEY` with your own OpenRouter API key.

**Security note:** Never publish your actual API key, commit the environment file to GitHub, or include the key in screenshots. Ensure that the environment file is excluded from version control.

### 3. Run Rafeeq

Run the following command in the project directory:

```powershell
py rafeeq.py "What is the illustrative building permit fee?"
```

The agent may use local tools to respond to questions and may request human approval before simulated write actions.

## Run Security Tests

To run the security test suite:

```powershell
py security_test.py
```

The test suite covers scenarios such as:

- Email recipient validation and domain allowlisting
- Human approval requirements for simulated actions
- Rejection of invalid booking slots
- Limiting exposed permit information
- Validation of MCP-style request structures
- Rejection of unknown tools and invalid query types

The current test suite has passed 16 tests in the local development environment. Results may vary if the code or environment changes.

## Run Evaluation

Run the evaluation script:

```powershell
py evaluate.py
```

The evaluation attempts to generate the following files:

- `eval_A.csv`
- `eval_B.csv`
- `eval.csv`
- `ERROR_ANALYSIS.md`

### Compare Model Configurations

To compare two model configurations, set the model identifiers supported by your API provider.

Windows PowerShell:

```powershell
$env:MODEL_A="provider/model-a"
$env:MODEL_B="provider/model-b"
py evaluate.py
```

Replace the example model identifiers with actual supported model IDs.

The evaluation results should be reviewed before drawing conclusions about model performance.

## Evaluation Methodology

The automatic grader checks whether expected tools were used and whether specified words appear in or are absent from the final answer.

These checks provide a basic way to assess agent behavior, but they do not fully measure answer quality, factual accuracy, security, privacy, or correct tool execution.

Review the generated CSV files and error analysis manually. Run the evaluation before reporting performance measurements or making claims about results.

## Security Design

Rafeeq includes several basic safeguards:

- Input validation for MCP-style requests
- Restrictions on available tools
- Email recipient domain allowlisting
- Human approval requirements for simulated write actions
- Validation of booking approval values
- Limits on the permit information returned by the prototype
- Security-focused unit tests

These safeguards are intended to demonstrate security concepts in an educational prototype. They do not establish that the system is secure against every attack.

## Security Limitations

- Policy records, permit statuses, fees, and appointment slots use synthetic demonstration data.
- Email and booking tools are simulated and do not send real emails or create real appointments.
- The example email allowlist uses `madar.example`.
- The prototype does not provide production-grade authentication or a real approval backend.
- It does not enforce a real monetary API cost budget.
- Security tests cover specific scenarios and cannot guarantee complete security.
- Model responses and tool-use decisions may still be incorrect.

Do not use this prototype to process real applicant data or perform real municipal actions.

## Project Status

Rafeeq is an independent educational prototype developed as the final project for the SDAIA Academy Agentic AI Program.

The project demonstrates agentic AI workflows, tool integration, human approval concepts, and basic security testing.

Its implementation, automated tests, and evaluation results should be reviewed before reporting measured performance or claiming complete compliance with any program capstone rubric.

## Acknowledgment

Developed as a learning project associated with the [SDAIA Academy Agentic AI Program](https://github.com/SDAIAAcademy/agentic-ai).
