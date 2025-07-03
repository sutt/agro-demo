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

** 1. Run pytest on both t1 and t2**

- Note: currently the main worksapce has 3 tests

```bash
uv run pytest -vv
======================================= test session starts =======================================
tests/test_main.py::test_read_root PASSED                                                   [ 33%]
tests/test_main.py::test_read_item PASSED                                                   [ 66%]
tests/test_main.py::test_read_item_no_query PASSED                                          [100%]

======================================== 3 passed in 0.28s ========================================
```

#### Pytests

```bash
agro muster 'uv run pytest' 1,2
```

**Output:**
    - notice one more test has been added to each worktree for the `/about` route.

```bash
--- Running command in t1 (trees/t1) ---
$ uv run pytest -v
tests/test_main.py::test_read_root PASSED                                                   [ 25%]
tests/test_main.py::test_read_item PASSED                                                   [ 50%]
tests/test_main.py::test_read_item_no_query PASSED                                          [ 75%]
tests/test_main.py::test_read_about PASSED                                                  [100%]

======================================== 4 passed in 0.29s ========================================

--- Running command in t2 (trees/t2) --
tests/test_main.py::test_read_root PASSED                                                   [ 25%]
tests/test_main.py::test_read_item PASSED                                                   [ 50%]
tests/test_main.py::test_read_item_no_query PASSED                                          [ 75%]
tests/test_main.py::test_read_about PASSED                                                  [100%]

======================================== 4 passed in 0.28s =======================================
```

#### Examine the actual about page performance

**Launch Server on each worktree**

```bash
agro muster 'python app/main.py' 1,2 --server
```
- The argument `--server` allows detach mode to run multiple servers out of one shell.

**Output**

```bash
--- Running command in t1 (trees/t1) ---
$ python app/main.py > server.log 2>&1 & echo $! > server.pid

--- Running command in t2 (trees/t2) ---
$ python app/main.py > server.log 2>&1 & echo $! > server.pid
```

**Check About Page Contents
- You could do this in browser as well

```bash
# check worktree app, here the /about route hasn't been created
curl http://127.0.0.1:8000/about
# {"detail":"Not Found"}

# check worktree t1
curl http://127.0.0.1:8001/about
# {"message":"Keep up the great work!"}

# check worktree t2
curl http://127.0.0.1:8002/about
{"message":"This is an about page. Keep up the great work!"}

```

**Teardown worktree servers**
- use empty message + flag `--kill-server` to kill the specified worktree servers running in the background.

```bash

$ agro muster '' 1,2 --kill-server 

--- Running command in t1 (trees/t1) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

--- Running command in t2 (trees/t2) ---
$ kill $(cat server.pid) && rm -f server.pid server.log

# verify it's down
$ curl http://127.0.0.1:8002/about
curl: (7) Failed to connect to 127.0.0.1 port 8002 after 0 ms: Connection refused
```

### Launch Second Task & Other Commands

Now let's look at some other commands, let's launch a new task:

`.agdocs/specs/add-db.md`:
```md
add an in-memory database of just a python dictionary for item model.

add some seed data that can be loaded for tests.

create 2 tests to confirm this is working.
```

**Run commands**

```bash
agro exec 3 .agdocs/specs/add-db.md 
agro exec 4 .agdocs/specs/add-db.md 
```
**Output**

<details>
    <summary>
    Expand commands output
    </summary>

```bash
$ agro exec 3 .agdocs/specs/add-db.md 
Attempting to remove existing worktree for index 3 (if any)...
Info: Worktree 'trees/t3' not found or not a valid worktree. Skipping removal.
Info: Branch 'tree/t3' not found. Skipping deletion.
♻️  Cleanup for index 3 complete.

Creating new worktree for index 3...
Creating new worktree 't3' at 'trees/t3' on branch 'tree/t3'...
Preparing worktree (new branch 'tree/t3')
HEAD is now at 7066f7f tutorial pt.2 (spec)
Copying .env to trees/t3/.env
Adding worktree overrides to trees/t3/.env
Setting up Python environment in trees/t3...

🌴 New worktree created successfully.
   Worktree: trees/t3
   Branch: tree/t3
   API Port: 8003
   DB Port:  5435
To start working, run: cd trees/t3 && source .venv/bin/activate

Switched to a new branch 'output/add-db.1'
🌱 Working on new branch: output/add-db.1

Launching agent in detached mode from within trees/t3...

🏃 Agent for index 3 started successfully.
   Worktree: /home/user/tools_dev/demo_fastapi/trees/t3
   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-db.md
   Branch: output/add-db.1
   Start time: 2025-07-03 18:17:49
   PID: 605984 (saved to /home/user/tools_dev/demo_fastapi/.agdocs/swap/t3.pid)
   Log file: /home/user/tools_dev/demo_fastapi/trees/t3/maider.log


$ agro exec 4 .agdocs/specs/add-db.md 
Attempting to remove existing worktree for index 4 (if any)...
Info: Worktree 'trees/t4' not found or not a valid worktree. Skipping removal.
Info: Branch 'tree/t4' not found. Skipping deletion.
♻️  Cleanup for index 4 complete.

Creating new worktree for index 4...
Creating new worktree 't4' at 'trees/t4' on branch 'tree/t4'...
Preparing worktree (new branch 'tree/t4')
HEAD is now at 7066f7f tutorial pt.2 (spec)
Copying .env to trees/t4/.env
Adding worktree overrides to trees/t4/.env
Setting up Python environment in trees/t4...

🌴 New worktree created successfully.
   Worktree: trees/t4
   Branch: tree/t4
   API Port: 8004
   DB Port:  5436
To start working, run: cd trees/t4 && source .venv/bin/activate
7066f7f38096bf71921e161a7b1e7d01f7347b26

Switched to a new branch 'output/add-db.2'
🌱 Working on new branch: output/add-db.2

Launching agent in detached mode from within trees/t4...

🏃 Agent for index 4 started successfully.
   Worktree: /home/user/tools_dev/demo_fastapi/trees/t4
   Task file: /home/user/tools_dev/demo_fastapi/.agdocs/specs/add-db.md
   Branch: output/add-db.2
   Start time: 2025-07-03 18:17:55
   PID: 606086 (saved to /home/user/tools_dev/demo_fastapi/.agdocs/swap/t4.pid)
   Log file: /home/user/tools_dev/demo_fastapi/trees/t4/maider.log
```

    


</details>




#### Killing a running agent
- Use surrender to terminate an ongoing agent with it's indices

```bash
$ agro surrender 3
--- Dry Run ---
Checking for running agent processes...
  - Found running process for t3: PID 605984
--- End Dry Run ---

Surrender and kill these 1 processes? (Y/n): Y

Proceeding with termination...
Killing process for t3 (PID 605984)...
  - Process 605984 terminated.
  - Removed PID file .agdocs/swap/t3.pid.

Surrender complete. Terminated 1 processes, 0 failed.

```
#### Viewing the result

**We should have 1 branch per agent run**
- one branch per start and one branch per stop.

```bash

  master
+ output/add-about.1
+ output/add-about.2
+ output/add-db.1
+ output/add-db.2
* output/add-db.2.copy
  tree/t1
  tree/t2
  tree/t3
  tree/t4

```

***Run command: `grab`***
```bash
agro grab output/add-db.2
```

**Output**
- This command helps you deal with worktrees have exclusive check-out on the branch where the work is.

```bash
Attempting to checkout branch 'output/add-db.2'...
Error executing command: git checkout output/add-db.2
fatal: 'output/add-db.2' is already checked out at '/home/user/tools_dev/demo_fastapi/trees/t4'

Branch 'output/add-db.2' is in use by another worktree.
Creating/updating copy 'output/add-db.2.copy' and checking it out.
Switched to branch 'output/add-db.2.copy'
Successfully checked out branch 'output/add-db.2.copy'.
```

**You can view diff on the HEAD**



```diff
-        "q": "testquery",
+@pytest.fixture
+def seed_db():
+    """Seed the database with some data for testing."""
+    db_data = {
+        1: {"name": "Foo", "description": "A foo item"},
+        2: {"name": "Bar", "description": "A bar item"},
     }
+    db.update(db_data)
+    yield
+    db.clear()
+
```

### Other commands

TODO
- grab
- fade
- delete


