from pyamlconf.config import PyamlConfig

config = PyamlConfig('tests/config.yaml')

print(config.get('db.url'))
print(config.get('db.desc'))