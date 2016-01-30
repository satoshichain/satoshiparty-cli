[![Latest Version](https://pypip.in/version/shellparty-cli/badge.svg)](https://pypi.python.org/pypi/shellparty-cli/)
[![Supported Python versions](https://pypip.in/py_versions/shellparty-cli/badge.svg)](https://pypi.python.org/pypi/shellparty-cli/)
[![License](https://pypip.in/license/shellparty-cli/badge.svg)](https://pypi.python.org/pypi/shellparty-cli/)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/ShellpartySHP/General)


# Description

`shellparty-cli` is a command line interface for [`shellparty-lib`](https://github.com/ShellpartySHP/shellpartyd).


# Requirements

* [Patched Shellcoin Core](https://github.com/shelldrak/SatoshiChain/releases) with the following options set:

	```
	rpcuser=SatoshiChainrpc
	rpcpassword=<password>
	txindex=1
	server=1
	addrindex=1
	rpcthreads=1000
	rpctimeout=300
	```

# Installation

**Linux and Mac OS X

```
$ git clone https://github.com/ShellpartySHP/shellparty-cli.git
$ cd shellparty-cli
$ pip3 install -r requirements.txt
$ python3 setup.py install
```

**Windows**

Download and decompress standalone [binaries](https://github.com/ShellpartySHP/shellparty-cli/releases).

# Usage

* `$ shellparty-server --help`

* `$ shellparty-client --help`


# Further Reading

* [Official Project Documentation](http://shellparty.io/docs/)
