# GitHub Copilot Commit Message Guidelines

Generate commit messages following these strict guidelines:

## Format

Always use the Conventional Commits format:
```
<type>(<scope>): <short summary>

<body>

<footer>
```

## Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc; no code change)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or fixing tests
- `build`: Changes to build process or tools
- `ci`: Changes to CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files

## Scope
Add a scope indicating what part of the codebase is affected:
- `model`
- `api`
- `ui`
- `data`
- `config`
- `deps`
- etc.

## Guidelines
1. Start with a capital letter and use imperative mood ("Add" not "Added")
2. Keep the summary under 72 characters
3. Be specific about what changed and why
4. Reference any relevant issue numbers in the footer
5. For breaking changes, add "BREAKING CHANGE:" in the footer
6. Include technical details that help reviewers understand the change

## Examples

Good:
```
feat(model): Add new strategic pricing calculation algorithm

Implement the Maxwell-Thompson formula for more accurate pricing predictions.
Algorithm improves accuracy by 15% on test dataset.

Closes #123
```

Bad:
```
changes
```
