# Demo-App for Agro

A simple FastAPI application for demoing [Agro](https://github.com/sutt/agro)

## Getting Started

```bash
git clone git@github.com:sutt/agro-demo.git
cd agro-demo

uv sync
uv run app/main.py
```

### Prerequisites

- uv venv: `uv` / Python 3.12+ 

## Agro Walk through 

Here's a quick tutorial for how to use [`Agro`](https://github.com/sutt/agro) to exntend this demo app.

### Launch Two Agents

**1. Use a predefined task and launch an agent**

- This repo comes with `.agdocs` tracked which contains `/agdocs`

`add-about.md`
```md
add an about page and route
add a unique message of encouragment to the about page
add a test 
run the test to make sure it passes before exiting
```

**Run command:**
```bash
$ agro exec 1 .agdocs/specs/add-about.md 
```
**Output:**
- notice the git worktree / branch management + launch of aider

```bash
♻️  Cleanup for index 1 complete.

Creating new worktree for index 1...
Creating new worktree 't1' at 'trees/t1' on branch 'tree/t1'...
Preparing worktree (new branch 'tree/t1')
HEAD is now at f0b97b1 refactor: .agdocs structure
Copying .env to trees/t1/.env
Warning: Source env file '.env' not found. Creating an empty .env file.
Adding worktree overrides to trees/t1/.env
Setting up Python environment in trees/t1...

🌴 New worktree created successfully.
   Worktree: trees/t1
   Branch: tree/t1
   API Port: 8001
   DB Port:  5433

🌱 Working on new branch: output/add-about.1

Launching agent in detached mode from within trees/t1...

🏃 Agent for index 1 started successfully.
   Worktree: /home/user/tools_dev/demo_fastapi/trees/t1
   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md
   Branch: output/add-about.1
   Start time: 2025-07-03 17:13:58
   PID: 579494 (saved to /home/user/tools_dev/demo_fastapi/.agdocs/swap/t1.pid)
   Log file: /home/user/tools_dev/demo_fastapi/trees/t1/maider.log
```
**2. Launch a second agent on same task**

**Run command:**
```bash
$ agro exec 2 .agdocs/specs/add-about.md 
```
**Output (shortened):**
- notice how work tree is incremented
- notice how API_PORT is incremented

```bash
♻️  Cleanup for index 2 complete.

🌴 New worktree created successfully.
   Worktree: trees/t2
   Branch: tree/t2
   API Port: 8002

🌱 Working on new branch: output/add-about.2

Launching agent in detached mode from within trees/t2...

🏃 Agent for index 2 started successfully.
   Worktree: /home/user/tools_dev/demo_fastapi/trees/t2
   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-about.md
   Branch: output/add-about.2

```

### View Two Agents Results


