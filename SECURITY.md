# Security Policy

This document outlines the security procedures and policies for the Stock Research Agentic Chatbot project.

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it to us by emailing `security@example.com`. Please do not disclose the vulnerability publicly until we have had a chance to address it.

When reporting a vulnerability, please include:

- A detailed description of the vulnerability.
- Steps to reproduce the vulnerability.
- Any proof-of-concept code.
- Your contact information.

We will acknowledge your report within 48 hours and will work with you to resolve the issue.

## Security Best Practices

- **API Keys**: The application uses a `.env` file to manage API keys and other secrets. This file is included in `.gitignore` and should never be committed to the repository.
- **Dependencies**: We strive to keep our dependencies up-to-date. You can scan for vulnerabilities in the installed packages using tools like `pip-audit` for Python and `npm audit` for Node.js.
- **Container Security**: The Docker images are built using official base images and are run with a non-root user.
- **Web Scraping**: The web scraping tools are designed to be respectful of `robots.txt` and the terms of service of the websites they access.

## Data Privacy

The application does not store any personal user data. All analysis is performed on the provided stock tickers and queries, and the results are not persisted in-memory or stored in a local vector database for the duration of the session.

