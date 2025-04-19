# 🔐 cred-switcher

A simple CLI tool to quickly switch between different **Git identities** and **AWS credentials**.

Perfect for developers juggling multiple projects, clients, or AWS environments.

---

## 🚀 Features

- ✅ Switch global Git user name and email  
- ✅ Update AWS credentials (`~/.aws/credentials` and `~/.aws/config`)  
- ✅ Manage multiple profiles in one config  
- ✅ Interactive prompts for adding profiles  
- ✅ Secure input for AWS secrets (nothing printed to screen)  

---

## 📦 Installation

### 🔁 Recommended: Use a Virtual Environment

```bash
git clone https://github.com/karizmattic876/cred-switcher.git
cd cred-switcher

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the CLI in editable mode
pip install --editable .
```

---

## 🧹 Uninstallation

If using a virtual environment:

```bash
deactivate
rm -rf venv/
```

Or uninstall globally:

```bash
pip uninstall cred-switcher
```

---

## 🛠️ Usage

```bash
cred-switcher add <profile>     # Add a new profile
cred-switcher set <profile>     # Switch to a saved profile
cred-switcher list              # List all saved profiles
cred-switcher show              # Show current Git and AWS identity
```

---

## 🖼️ Demo

Here's how `cred-switcher` looks in action:

![cred-switcher demo](screenshot.png)

---

## 📜 License

MIT © Karizmattic