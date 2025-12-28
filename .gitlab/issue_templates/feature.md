title: "Feature Request: "
description: "Suggest an idea for this project"
labels:
  - enhancement
  - triage

body:
  - type: markdown
    attributes:
      value: |
        Thanks for the feature suggestion!

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear description of the feature
      placeholder: Describe the feature...
    validations:
      required: true

  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this solve?
      placeholder: What problem does this solve?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How this feature would work
      placeholder: How should this work?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      description: Any alternative approaches you've considered

  - type: textarea
    id: additional
    attributes:
      label: Additional Context
      description: Any other information, mockups, or examples
