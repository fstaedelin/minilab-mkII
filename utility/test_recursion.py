def find_parent_keys(d, target_key, parent_key=None):
  for k, v in d.items():
    if k == target_key:
      yield parent_key
    if isinstance(v, dict):
      for res in find_parent_keys(v, target_key, k):
        yield res

d = {
  'dev': {
    'dev1': {
      'mod': {
        'mod1': {'port': [1, 2, 3]},
      },
    },
    'dev2': {
      'mod': {
        'mod3': {'port': []},
      },
    },
  },
}

print(list(find_parent_keys(d, 'mod')))
print(list(find_parent_keys(d, 'dev')))

['dev2', 'dev1']
[None]
