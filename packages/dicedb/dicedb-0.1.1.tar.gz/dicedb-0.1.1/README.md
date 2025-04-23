# DiceDB for Python

⚠️ This is not an official sdk for python and still in development.

## Installation and Usage

### From PyPI

```bash
pip install dicedb
```

### From Source

Clone the repository and install the package:

```bash
$ git clone https://github.com/un4gt/dicedb.git --depth 1 --branch main
$ uv sync
$ uv buid
```

## Supported Commands

|    command    | description  |
|:-------------:|:------------:|
|    `decr`     |   `DECRBY`   |
|   `decrby`    |   `DECRBY`   |
|   `delete`    |    `DEL`     |
|    `echo`     |    `ECHO`    |
|   `exists`    |   `EXISTS`   |
|   `expire`    |   `EXPIRE`   |
|  `expire_at`  |  `EXPIREAT`  |
| `expire_time` | `EXPIRETIME` |
|   `flushdb`   |  `FLUSHDB`   |
|     `get`     |    `GET`     |
|   `get_del`   |  `GET_DEL`   |
|   `get_ex`    |   `GET_EX`   |
|    `hget`     |    `HGET`    |
|  `hget_all`   |  `HGETALL`   |
|    `hset`     |    `HSET`    |
|   `incr_by`   |   `INCRBY`   |
|    `incr`     |   `INCRBY`   |
|    `ping`     |    `PING`    |
|     `ttl`     |    `TTL`     |
|   `typeof`    |    `TYPE`    |
|     `set`     |    `SET`     |


## Roadmap

- [ ] More documentation/tests/examples
- [ ] Support for all commands
- [ ] Connection pool
- [ ] Support for async


## Contributing

PRs and issues are welcome! 

## About Developing

### Generate Python Proto Files

*cmd.proto and res.proto comes from https://github.com/DiceDB/dicedb-protos*

On Windows: 

```bash
protoc -I=protos\ --python_out=src\dicedb\proto\ --pyi_out=src\dicedb\proto cmd.proto res.proto
```