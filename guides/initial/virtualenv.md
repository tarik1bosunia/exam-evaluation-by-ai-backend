# 🐍 Creating a Python Virtual Environment

---

##  For Linux

###  Step 1: Ensure Python and pip are installed

On most Linux distributions, Python 3 and pip can be installed via package manager:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

### Step 2: Create a virtual environment
This creates a folder myenv (you can use any name) containing the isolated Python environment.
```bash
python3 -m venv myenv
```

### Step 3: Activate the virtual environment
```bash
source myenv/bin/activate
```
### Step 4: Deactivate the virtual environment
```sh
deactivate
```

---

## For Windows
If Python is installed, pip should already be available.

### Step 1: Create a virtual environment
Open Command Prompt or PowerShell, navigate to your project folder, and run:
```sh
python -m venv myenv
```
### Step 2: Activate the virtual environment
```sh
venv/scripts/activate
```
### 3: Deactivate the virtual environment
```sh
deactivate
```
---
