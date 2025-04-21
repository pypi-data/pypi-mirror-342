## 🛠️ Project Scaffold for `SetMail`

---

### 📁 Folder structure:

```
setmail/
├── __init__.py
setup.py
README.md
```

---

### 📄 `setup.py`

```python
from setuptools import setup

setup(
    name='SetMail',
    version='0.1',
    author='Your Name',
    author_email='your@email.com',
    description='Minimalist email sending for Python — just import and send',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/SetMail/',
    packages=['setmail'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
```

---

### 📄 `setmail/__init__.py` (placeholder logic)

```python
import smtplib
from email.mime.text import MIMEText
import os

def send(to, subject, body, sender=None, smtp_server=None, password=None):
    sender = sender or os.getenv("SETMAIL_FROM")
    smtp_server = smtp_server or os.getenv("SETMAIL_SMTP")
    password = password or os.getenv("SETMAIL_PASS")

    if not all([sender, smtp_server, password]):
        raise ValueError("Missing SMTP configuration.")

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    host, port = smtp_server.split(":")
    with smtplib.SMTP_SSL(host, int(port)) as server:
        server.login(sender, password)
        server.sendmail(sender, [to], msg.as_string())
```

---

### 📄 `README.md`

```markdown
# SetMail

> The simplest way to send email in Python — no setup, just import and go.

[![PyPI version](https://img.shields.io/pypi/v/setmail.svg)](https://pypi.org/project/SetMail/)
[![License](https://img.shields.io/pypi/l/setmail.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/pypi/pyversions/setmail.svg)](https://python.org)

---

### 💡 What is SetMail?

SetMail is a zero-config SMTP mail sender designed for small Python projects.  
Use environment variables or pass values manually — and you're sending in seconds.

---

### 📦 Install

```bash
pip install setmail
```

---

### 🚀 Example

```python
import setmail

setmail.send(
    to="hello@example.com",
    subject="Test Email",
    body="This was sent using SetMail!"
)
```

---

### ⚙️ Environment Variables

You can configure SetMail globally with these:

```bash
export SETMAIL_FROM="you@example.com"
export SETMAIL_SMTP="smtp.example.com:465"
export SETMAIL_PASS="yourpassword"
```

Then just call `send()` with `to`, `subject`, and `body`.

---

### 🔐 Security Tip

Don't hardcode passwords in code — use `.env`, CI secrets, or vault systems.

---

### 📄 License

MIT. Lightweight and open to contributions.