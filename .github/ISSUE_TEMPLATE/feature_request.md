name: Feature Request
description: Suggest an idea for this project
title: "[FEATURE] "
labels: ["enhancement", "triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for your interest in improving our project!

  - type: textarea
    id: description
    attributes:
      label: Feature Description
      description: A clear and concise description of what the feature would do
      placeholder: Describe the feature...
    validations:
      required: true

  - type: textarea
    id: use-case
    attributes:
      label: Use Case / Problem Statement
      description: Describe the problem this feature would solve
      placeholder: What problem does this solve?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: Describe how you would like this feature to work
      placeholder: How should this work?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      description: Describe any alternative solutions or features you've considered

  - type: textarea
    id: additional
    attributes:
      label: Additional context
      description: Add any other context, mockups, or examples
