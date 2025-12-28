title: "Bug Report: "
description: "Report a bug in the project"
labels:
  - bug
  - triage

body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to file a bug report!

  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear and concise description of what the bug is
      placeholder: Describe the bug...
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How to reproduce the issue
      placeholder: |
        1. Step one...
        2. Step two...
        3. See error...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What you expected to happen
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      placeholder: |
        - OS: 
        - Python Version: 
        - Package Version: 
        - Browser (if applicable): 

  - type: textarea
    id: logs
    attributes:
      label: Error Logs
      description: Include any error messages or logs

  - type: textarea
    id: additional
    attributes:
      label: Additional Information
      description: Any other context or information
