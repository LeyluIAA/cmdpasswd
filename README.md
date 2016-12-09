# cmdpasswd

cmdpasswd is a command line tool to manage password.

It let you store and display passwords.

## requirements

- python 2.7+

## Usage

```bash
$ git clone https://github.com/LeyluIAA/cmdpasswd.git
$ cd cmdpasswd
$ python pass.pyc -h
```

## Advice

- Passwords are quite important, you **should** cron the 'cp/scp/rsync' of pass.db on several directories and even servers.
- For security again, prefer the pass.pyc to pass.py. You should only keep pass.pyc in your computer after cloning the repo.
