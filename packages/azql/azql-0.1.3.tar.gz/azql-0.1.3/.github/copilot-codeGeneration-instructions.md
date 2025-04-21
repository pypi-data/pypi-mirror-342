# GitHub Copilot Code Generation Instructions

## Python Code Style: `.py` Files
- Follow these guidelines for all Python files.

### General
- Minimum Python Version: `3.10`.

### Formatting
- Adhere to the `PEP8` standard.
- Use `snake_case` for variable and function names.
- Use `PascalCase` for class names.
- Enclose strings in `double quotes`.
- Indent code using `4 spaces`.
- Use `typing` annotations wherever possible. Prefer built-in types (e.g., `list`, `dict`, `tuple`) over imports from the `typing` module.
- Avoid unnecessary blank lines and trailing whitespace.
- Limit line length to `80 characters`. Use line breaks for longer lines, maintaining proper indentation.
- Ensure consistent formatting across the codebase for readability and maintainability.
- Regularly review and update formatting rules to align with evolving project requirements.

### Linting
- Use `ruff` as the primary linter.
- Check for `[tool.ruff.lint]` entries in `pyproject.toml` or rules in `ruff.toml`.
- Resolve all linting violations before committing code.
- If `ruff` is unavailable, use an alternative linter that supports `PEP8` compliance.
- Regularly update linting configurations to align with project standards.
- Document custom linting rules or exceptions in the repository.

---

## SQL Code Style: `.sql` Files
- Use these guidelines for all SQL files.
- Dialect: `TSQL` for Microsoft SQL Server.

### Formatting
- Use `snake_case` for variable names.
- Write `comma-first` lines.
- Use UPPERCASE for SQL keywords (e.g., SELECT, FROM, WHERE).
- Indent with `4 spaces`, not tabs.
- Add line breaks before each clause (e.g., WHERE, JOIN, GROUP BY).
- Use short but meaningful aliases for table names.
- Include the schema name when referencing tables (e.g., `dbo.table_name`).
- Add comments for complex logic or non-obvious operations.
- Align similar elements vertically for better readability.

#### Example: Comma-First Style
```sql
SELECT
  column_id
    , column_name
FROM dbo.mytable
```

---

## Markdown Style: `.md` Files
- Improve grammar and clarity when using `/fix` or `improve` commands.
- Ensure concise and professional language.
- Use proper headings and formatting for readability.
- Avoid redundant or overly complex phrasing.
- Regularly review and refine content for accuracy and consistency.