---
name: Custom Issue
about: Use this template for issues that don’t fit the bug report or feature request categories
title: "[CUSTOM] "
labels: ''
assignees: ''
---

## Custom Issue

### Purpose
Describe the purpose of this issue. What do you want to address or propose? (e.g., documentation update, question, new idea, etc.)

### Details
Provide a detailed explanation of your issue or request. Include as much context as possible to help maintainers understand your intent.

### Relevant Context
Add any relevant information, such as:
- **Audio Files**: Format, sample rate, or a link/sample if applicable.
- **Code Snippets**: If this involves code, include examples (use ``` for code blocks):
  ```python
  # Example code
  from bhargava_swara import some_function
  result = some_function("audio.wav")
  print(result)
  ```
- **Environment**: OS, Python version, Bhargava Swara version, etc.
- **References**: Links to papers, tools, or other resources.

### Desired Outcome
What do you hope to achieve by raising this issue? (e.g., clarification, discussion, implementation, etc.)

### Additional Notes
Add any extra thoughts, questions, or suggestions here.

---

### Purpose of This Custom Issue Template

This template is designed to:
- Provide flexibility for contributors to report issues or ideas that don’t strictly qualify as bugs or feature requests.
- Encourage detailed submissions with context (e.g., audio files, code, or references) relevant to `bhargava_swara`.
- Allow contributors to specify their desired outcome, making it easier for maintainers to respond effectively.

Examples of when to use this template:
- Requesting clarification on how to use a specific function (e.g., `generate_mel_spectrogram`).
- Proposing a new analysis method not listed in `contribute.md`.
- Reporting a documentation inconsistency or suggesting improvements.
- Asking for guidance on integrating a new synthesis tool.

---

### How to Add It

1. **Add to Your Repository**:
   - Place this file in `.github/ISSUE_TEMPLATE/custom_issue.md` alongside your other templates (`bug_report.md` and `feature_request.md`).

2. **Update `config.yml`** (optional):
   - If you’ve already added the `.github/ISSUE_TEMPLATE/config.yml` from my previous response, no changes are needed—it will automatically recognize this new template.

3. **Commit and Push**:
   ```bash
   git add .github/ISSUE_TEMPLATE/custom_issue.md
   git commit -m "Add custom issue template"
   git push origin main
   ```

4. **Test It**:
   - Go to your repository’s "Issues" tab, click "New Issue," and verify that "Custom Issue" appears as an option alongside "Bug Report" and "Feature Request."

---

If you had a more specific purpose in mind for this custom template (e.g., something tailored to a particular aspect of `bhargava_swara` like synthesis tools or raga analysis), please let me know, and I can refine it further!
