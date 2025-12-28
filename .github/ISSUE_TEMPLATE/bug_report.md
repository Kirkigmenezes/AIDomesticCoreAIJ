name: Bug Report
description: File a bug report
title: "[BUG] "
labels: ["bug", "triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear and concise description of what the bug is.
      placeholder: Describe the issue...
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
      placeholder: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: A clear and concise description of what you expected to happen.
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual behavior
      description: What actually happened instead.
    validations:
      required: true

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots
      description: If applicable, add screenshots or error messages

  - type: textarea
    id: environment
    attributes:
      label: Environment Information
      description: Please provide your environment details
      value: |
        - OS: 
        - Python Version: 
        - Package Version: 
        - Browser (if applicable): 
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Error Logs
      description: Add any error logs or stack traces
      render: shell

  - type: textarea
    id: additional
    attributes:
      label: Additional context
      description: Add any other context about the problem here
