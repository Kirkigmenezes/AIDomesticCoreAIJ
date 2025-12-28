name: Pull Request
description: Create a pull request
labels: []
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for contributing! Please fill in the details below.

  - type: textarea
    attributes:
      label: Description
      description: Please provide a description of the changes
      placeholder: "Describe what this PR does and why"
    validations:
      required: true

  - type: textarea
    attributes:
      label: Related Issues
      description: Link to related issues (e.g., "Fixes #123")
      placeholder: "Fixes #123\nRelated to #456"

  - type: textarea
    attributes:
      label: Changes
      description: List the specific changes made
      placeholder: |
        - Changed X to Y
        - Added feature Z
        - Fixed bug W

  - type: textarea
    attributes:
      label: Testing
      description: How was this tested?
      placeholder: |
        - [ ] Unit tests added
        - [ ] Integration tests passed
        - [ ] Manual testing completed

  - type: checkboxes
    attributes:
      label: Checklist
      options:
        - label: Code follows style guidelines
          required: true
        - label: Tests pass locally
          required: true
        - label: Documentation updated
          required: true
        - label: No breaking changes
          required: true
        - label: Commit messages follow conventional commits
          required: true

  - type: textarea
    attributes:
      label: Screenshots/Output
      description: If applicable, add screenshots or output
