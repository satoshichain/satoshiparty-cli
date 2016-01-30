**@ouziel-slama:**

- Quality Assurance
- Update `CHANGELOG.md`
- Update `APP_VERSION` in `shellpartycli/__init__.py`
- Update `shellpartylib` version in `setup.py` (if necessary)
- Merge develop into Master
- Build binaries:
    * In a new VM install Windows dependencies (http://shellparty.io/docs/windows/)
    * `git clone https://github.com/ShellpartySHP/shellparty-cli.git`
    * `cd shellparty-cli`
    * `python setup.py install`
    * `python setup.py py2exe`
- Send @adamkrellenstein the MD5 of the generated ZIP file

**@adamkrellenstein:**

- Tag and Sign Release (include MD5 hash in message)
- Write [Release Notes](https://github.com/ShellpartySHP/shellpartyd/releases)
- Upload (signed) package to PyPi
    * `sudo python3 setup.py sdist build`
    * `twine upload -s dist/$NEW_FILES`

**@ouziel-slama:**

- Upload ZIP file in [Github Release](https://github.com/ShellpartySHP/shellparty-cli/releases)

**@ivanazuber:**:

- Post to [Official Forums](https://forums.shellparty.io/discussion/445/new-version-announcements-shellparty-and-shellpartyd), Skype, [Gitter](https://gitter.im/ShellpartySHP)
- Post to social media
- SMS and mailing list notifications
