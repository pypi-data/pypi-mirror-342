# 🔐 cred-switcher
[![PyPI version](https://badge.fury.io/py/cred-switcher.svg)](https://pypi.org/project/cred-switcher/)

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

Install globally via [PyPI](https://pypi.org/project/cred-switcher/):

```bash
pip install cred-switcher
```

> 🔁 Recommended for devs: use a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install cred-switcher
```

Then run it:

```bash
cred-switcher
```

---

## 🧹 Uninstallation

To remove it:

```bash
pip uninstall cred-switcher
```

If you used a virtual environment:

```bash
deactivate
rm -rf venv/
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