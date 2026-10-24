### Lab Code Contribution Guide

Welcome to the lab repository! To keep our code clean, reproducible, and ready for selective public release, all members must follow this contribution and review workflow. 

Before writing any code, ensure you have loaded the master .gitignore file so that raw data and configuration files are never tracked. 

### 1. Branch Naming Conventions

Never write or commit code directly to the main branch. Always create a descriptive feature branch from the latest version of main. 

Use the following prefixes when creating a branch in VS Code: 

* feature/ for new scripts, analysis workflows, or algorithms (e.g., feature/rna-seq-pipeline)
* fix/ for correcting bugs or broken code (e.g., fix/matlab-import-error)
* docs/ for writing documentation, README updates, or comments (e.g., docs/add-installation-steps)

### 2. Code Requirements

Before you submit your code for peer review, verify that your scripts meet these standards: 

* **No Raw Data:** Never stage or commit .csv, .xlsx, .mat, or other raw data formats. Double-check your VS Code changes panel to ensure these are hidden.
* **Relative Paths Only:** Do not use absolute computer paths (e.g., C:/Users/YourName/Documents/Data/). Use relative paths (e.g., ../data/) so your code runs flawlessly on other lab members' machines.
* **Documentation:** Include a brief comment block at the top of new scripts explaining what the code does, its inputs, and its expected outputs.

### 3. How to Submit Code for Review

When your feature is complete and working on your machine, follow these steps to merge it into the lab's private main branch: 

1. **Commit and Push:** Save your work, commit it with a descriptive message, and push your branch to the private remote (origin) using VS Code or GitHub Desktop.
2. **Open a Pull Request (PR):** Navigate to our private GitHub repository in your browser. Click the **Compare & pull request** button next to your recently pushed branch.
3. **Describe Your Changes:** In the PR description field, briefly explain: 

  * What problem this code solves or what analysis it performs.
  * Any specific package dependencies or environment setups required to run it.
4. **Assign a Reviewer:** Request a review from at least one peer or a lab admin.

### 4. The Review Process

* **For Reviewers:** Run the code locally if possible, check for edge cases, and ensure the code follows our lab formatting style. Leave constructive feedback directly on the GitHub PR lines.
* **For Authors:** Address any review comments or requested changes by pushing new commits to your feature branch. The PR will update automatically.
* **Merging:** Once the PR receives a green approval badge from a reviewer or lab admin, it can be safely merged into main.

### 5. Public Releases (Admin Only)

Only designated lab admins have the authority to push code to our external public repository. 

Admins will periodically pull approved code from the private main branch into the public-release branch, audit the code for privacy compliance, and use the VS Code "Push to... public" command to share our findings with the scientific community.
