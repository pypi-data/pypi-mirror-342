# Django Admin 2FA

[![PyPI version](https://badge.fury.io/py/django-admin-2fa.svg)](https://pypi.org/project/django-admin-2fa/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![TRADEMARK](https://img.shields.io/badge/License-MIT-green.svg)](TRADEMARK.md)
[![Django Versions](https://img.shields.io/badge/Django-3.2%2B-blue)](https://www.djangoproject.com/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/your-username/django-admin-2fa)

**Django Admin 2FA Plus** is a secure, easy-to-use Two-Factor Authentication package for Django Admin. It provides TOTP-based verification (Google Authenticator, Authy, etc.), recovery codes, and optional trusted devices.

---

## 🚀 Key Features

### 🔐 Fortified Admin Security
- Two-Factor Authentication (2FA) for Django Admin  
- Adds an extra layer of protection for staff logins

### 📲 Flexible TOTP Support
- Time-based One-Time Passwords using apps like:
  - Google Authenticator  
  - Authy  
  - and more!

### 🛡️ Recovery & Backup
- One-time backup codes for account recovery  

### 🧩 Device & Access Control
- Built-in admin panel to view & manage TOTP devices  
- "Trusted Device" support — keeps your users happy with fewer prompts

### 🎨 Rate Limit
- Extra security with rate limit

### ⚙️ Compatibility
- Supports Django 3.2-5.* and above  
- Easy to integrate with existing Django projects


## 📦 Installation

```bash
pip install django-admin-2fa
```

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "djangoadmin2fa",
]
```

Include the URLs:

```python
# urls.py
path("admin2fa/", include("djangoadmin2fa.urls")),
```

Add SITE_NAME variable in your django setting (Recomended)
Otherwise default DJANGO ADMIN 2FA will be shown in your authenticator app and in backup code print page instead of your website name.

```python
#settings.py
SITE_NAME = "www.yoursite.com"

```

Add the middleware near the top of your middleware stack:

```python
MIDDLEWARE = [
    ...
    "djangoadmin2fa.middleware.Admin2FAMiddleware",
    "djangoadmin2fa.middleware.Admin2faRateLimitMiddleware",
]
```

Run migrations:

```bash
python manage.py migrate
```

---

## 🚀 Quick Start

1. Log in to Django Admin.
2. It will automatically return to 2FA Setup page.
3. Scan the QR code using your authenticator app.
4. Enter the generated code to confirm.
5. Copy/Print the backup codes displayed — each can be used once.
6. Done! (Logout and login again to see effect)

---


## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Update code, if needed, as per pre-commit logs
5. Push to the branch: `git push origin feature/my-feature`
6. Open a Pull Request

You must follow PEP8, isort and must have proper test cases.

---

## 📬 Support

For questions, bug reports, or feature requests, please open an [issue](https://github.com/swe-himelrana/django-admin-2fa) on GitHub.
Feel free to reach out via email: [python.package@himosoft.com.bd](mailto:python.package@himosoft.com.bd)
---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
🚫 Branding usage is restricted — see the [LICENSE](LICENSE) and [TRADEMARK](TRADEMARK.md) files for details.

---

Secure your Django Admin with TOTP based 2FA system ✨
