# cmdpasswd

cmdpasswd is a command line tool to manage password.

It let you securely store and display passwords.

# requirements

- python 2.7+

# Usage

```bash
$ git clone https://github.com/LeyluIAA/cmdpasswd.git
$ python pass.py -h
```

# Advice

- Passwords are quite important, you **should** cron the 'cp/scp/rsync' of pass.db on several directories and even servers.
- With version 1.0, you have to type clear passwords on the command line, so you **should** cron the 'rm' of bash_history in order to clean passwords typing.
