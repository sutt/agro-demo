# Demo-App for Agro

A simple FastAPI application for demoing [Agro](https://github.com/sutt/agro)

## Getting Started

### Install Agro

```bash
pip install agro
# or
uv tool install agro
```

Or setup a dev install, instructions [here](https://github.com/sutt/agro?tab=readme-ov-file#local-development-install).

### Setup 

Clone the repo, setup the uv environment, start the server.

- **Prerequisites:** `uv` / Python 3.11+ 

```bash
git clone https://github.com/sutt/agro-demo
cd agro-demo

# setup environment and run server
uv sync
cp .env.example .env
uv run app/main.py
# hit ctrl+c to shutdown server, and let's start...
```

## Agro Walk through 

**Also see the [case studies](./docs/case-studies/index.md) for more advanced guidance on using this tool**

**0. Clone & Setup the Demo Repo** Follow the Setup steps.

**1. Launch four agents in parallel**

_Agro is configured to use aider by default. Add the name of the coding agent you have installed as the argument to use the one you have installed._

```bash
$ agro exec add-about 2       # launch two agents of aider 
$ agro exec add-about claude  # if you have claude-code installed
$ agro exec add-about gemini  # if you have gemini installed
```
This repo comes with tasks in `.agdocs/specs` including the spec

**[add-about.md](.)**
>add an about page and route
>add a unique message of encouragment to the about page
>add a test 
>run the test to make sure it passes before exiting

**Basic Output**
- notice the git worktree / branch management + launch of aider, claude and gemini

```bash
♻️  Cleanup for index 1 complete.
🏃 Agent for index 1 started successfully.
   Worktree: /home/user/dev/agro/agro-demo/trees/t1
   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
   Branch: output/add-about.1
   Agent type: aider
   Initial commit SHA: 31ad99
   Start time: 2025-07-18 09:12:20
♻️  Cleanup for index 2 complete.
🏃 Agent for index 2 started successfully.
   Worktree: /home/user/dev/agro/agro-demo/trees/t2
   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
   Branch: output/add-about.2
   Agent type: aider
   Initial commit SHA: 31ad99
   Start time: 2025-07-18 09:12:20

♻️  Cleanup for index 3 complete.
🏃 Agent for index 3 started successfully.
   Worktree: /home/user/dev/agro/agro-demo/trees/t3
   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
   Branch: output/add-about.3
   Agent type: claude
   Initial commit SHA: 31ad99
   Start time: 2025-07-18 09:13:13

♻️  Cleanup for index 4 complete.
🏃 Agent for index 4 started successfully.
   Worktree: /home/user/dev/agro/agro-demo/trees/t4
   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/add-about.md
   Branch: output/add-about.4
   Agent type: gemini
   Initial commit SHA: 31ad99
   Start time: 2025-07-18 09:13:27
```

Now you should see multiple branches created, one for each agent:

```bash
$ git branch
* master
+ output/add-about.1
+ output/add-about.2
+ output/add-about.3
+ output/add-about.4
```

**2. Launch Server on each worktree**

```bash
agro muster --server 'uv run python app/main.py' output
```
- The argument `--server` allows detach mode to run multiple servers out of one shell.

**Output**

```bash
agro muster --server 'uv run python app/main.py' output

--- Running command in t1 (output/add-about.1) ---
$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid

--- Running command in t2 (output/add-about.2) ---
$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid

--- Running command in t3 (output/add-about.3) ---
$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid

--- Running command in t4 (output/add-about.4) ---
$ uv run python app/main.py > server.log 2>&1 & echo $! > server.pid
```

**Check About Page Contents**
_You could do this in browser as well_

```bash
# check worktree t1 - aider agent (#1)
curl http://127.0.0.1:8001/about
# {"message":"Keep up the great work!"}

# check worktree t2 - aider agent (#2)
curl http://127.0.0.1:8002/about
# {"message":"You are doing great!"}

# check worktree t3 - claude agent
curl http://localhost:8003/about
# {"message":"🌱 Every great journey begins with a single step. You're already on your way to something amazing!","title":"About AgSwap","description":"Welcome to AgSwap - where agricultural innovation meets community collaboration."}

# check worktree t4 - gemini agent
curl http://localhost:8004/about
# {"message":"Keep up the great work, you're awesome!"}

```

Now clean up the server:

```bash
# run muster with --kill-server to take it down each worktree
$ agro muster --kill-server '' output

--- Running command in t1 (output/add-about.1) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

--- Running command in t2 (output/add-about.2) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

--- Running command in t3 (output/add-about.3) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

--- Running command in t4 (output/add-about.4) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

# checking agent1's worktree env, we see the server is no longer responding
$ curl http://localhost:8001
curl: (7) Failed to connect to localhost port 8001 after 0 ms: Connection refused
```

**3. Checking tests**

We run our existing tests with:

```bash
$ uv run pytest -q
3 passed in 0.28s
```

So we see have 3 existing tests, now let's check the output of our agents:

```bash
$ agro muster 'uv run pytest -q' output

--- Running command in t1 (output/add-about.1) ---
$ uv run pytest -q
4 passed in 0.25s

--- Running command in t2 (output/add-about.2) ---
$ uv run pytest -q
4 passed in 0.28s

--- Running command in t3 (output/add-about.3) ---
$ uv run pytest -q
4 passed in 0.25s

--- Running command in t4 (output/add-about.4) ---
$ uv run pytest -q
3 passed in 0.24s
```
### Or add your own spec to a project

For example:

**Create and commit a spec file and pass to an agent**
```bash
agro init # add .agdocs/ to repo

# create a spec
agro task hello-world  
# then add the text to the spec: "add hello world to the readme of this project"
# equivalent to:
echo "add hello world to the readme of this project" > .agdocs/specs/hello-world.md

agro exec
# equivalent to:
agro exec add-about 1 aider
```


