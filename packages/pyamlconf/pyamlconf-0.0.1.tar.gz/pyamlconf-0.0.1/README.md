# PyamlConf

A simple YAML-based configuration loader for Python

## Mustache 
bala bala..... see demo

## Install

```commandline
pip install pyamlconf
```

## Demo

create yaml file on local path: tests/config.yaml

```yaml
db:
  url: mysql://{{.host}}:3306
  host: 127.0.0.1
  name: dbtest
  pwd: 123456
  pool:
    size: 100
    maxidle: 10
  desc: "db.url = {{ db.url }}; db.name = {{ .name }}; db.pool = {{.pool}} "
```

create tests/test.py, like:

```python
from pyamlconf.config import PyamlConfig

config = PyamlConfig('tests/config.yaml')

print(config.get('db.url'))
print(config.get('db.desc'))
```

```commandline
python tests/test.py
```

output:

```commandline
mysql://127.0.0.1:3306
db.url = mysql://127.0.0.1:3306; db.name = dbtest; db.pool = {'size': 100, 'maxidle': 10}
```
