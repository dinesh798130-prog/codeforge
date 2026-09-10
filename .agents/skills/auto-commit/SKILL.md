---
name: auto-commit
description: Reviews the diff of all code changes, generates a concise Conventional Commits message, and executes git add and git commit commands in the terminal.
---

# Auto Commit Skill

This skill guides the agent in reviewing working directory changes, generating a clear commit message conforming to the Conventional Commits specification, and committing the changes via git.

## Workflow Instructions

### Step 1: Inspect Git Status and Code Diffs
1. Check repository state and inspect all modified, added, or deleted files:
   - Run `git status` to inspect tracked and untracked changes.
   - Run `git diff` to analyze unstaged modifications.
   - Run `git diff --cached` (or `git diff --staged`) to analyze any already-staged changes.
2. If there are untracked files intended for inclusion, inspect their purpose and contents.
3. If there are no changes to commit, inform the user and terminate the workflow early.

### Step 2: Generate a Conventional Commit Message
1. Analyze the intent and scope of the modifications:
   - Identify the primary nature of the changes (e.g., new feature, bug fix, refactor, tests, documentation).
2. Select the appropriate Conventional Commit type:
   - **`feat`**: A new feature or capability for the user.
   - **`fix`**: A bug fix.
   - **`refactor`**: Code changes that neither fix a bug nor add a feature (e.g., code cleanup, reorganization).
   - **`test`**: Adding missing tests or correcting existing tests.
   - **`docs`**: Documentation-only changes.
   - **`style`**: Changes that do not affect code logic (whitespace, formatting, missing semicolons, etc.).
   - **`perf`**: A code change that improves performance.
   - **`chore`**: Build process updates, dependency upgrades, or auxiliary tool changes.
3. Construct the commit message:
   - Format: `<type>[optional scope]: <imperative description>`
   - Example: `refactor: clean up logic and add unit tests`
   - Use lowercase for the type and description.
   - Use the imperative mood (e.g., "add", "clean", "fix" instead of "added", "cleaning", "fixes").
   - Keep the subject line concise (under 72 characters).
   - If changes span multiple areas, add bullet points or an explanatory body separated by an empty line.

### Step 3: Stage and Commit Changes
1. Stage the appropriate files:
   ```bash
   git add .
   ```
   *(or stage specific files if selectively committing changes)*
2. Execute the commit command with the generated message:
   ```bash
   git commit -m "<type>: <concise description>"
   ```
   *For commits requiring a detailed body, provide multiple `-m` flags:*
   ```bash
   git commit -m "<type>: <concise description>" -m "<detailed explanation or bullet points>"
   ```

### Step 4: Verify and Report
1. Verify the commit was recorded successfully:
   - Run `git log -1 --stat` or `git status`.
2. Output a summary to the user:
   - The commit hash and message used.
   - A list of committed files and modification counts.
