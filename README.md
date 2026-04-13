# Agentic Loan Underwriter with Persistent Memory

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-grade Agentic AI system that automates the loan underwriting process while maintaining auditability, consistency, and human oversight.

## Overview

This system acts as an autonomous underwriting assistant that:

- Ingests and analyzes loan applications and supporting documents
- Verifies applicant identity and creditworthiness
- Applies complex credit policies with citation-level precision
- Learns from historical decisions via persistent memory
- Provides fully auditable recommendations with human-in-the-loop checkpoints

## Architecture

![Architecture Diagram](docs/architecture.png)

_(Diagram coming soon)_

### Key Components

- **LangGraph Orchestrator**: State-machine based agent workflow
- **Specialized AI Agents**: Document Processing, Verification, Credit Assessment, Policy Compliance, Report Generation
- **Persistent Memory**: pgvector-powered semantic storage of past underwriting cases
- **MCP Servers**: Standardized tool interfaces for external services
- **LiteLLM Gateway**: Provider-agnostic LLM routing with fallbacks

## Tech Stack

| Layer            | Technology                        |
| ---------------- | --------------------------------- |
| Frontend         | React + TypeScript + Tailwind CSS |
| Backend API      | FastAPI (Python)                  |
| AI Orchestration | LangGraph                         |
| LLM Gateway      | LiteLLM                           |
| Database         | PostgreSQL + pgvector             |
| Containerization | Docker                            |
| Observability    | LangSmith + Prometheus            |

## Project Status

🚧 **Under Active Development** 🚧

This project is being built as a portfolio piece demonstrating enterprise AI architecture patterns.

## Getting Started

_Detailed setup instructions coming soon._

## License

MIT
