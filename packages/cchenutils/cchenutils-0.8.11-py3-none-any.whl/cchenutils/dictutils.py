import json


class Dict(dict):
    def __init__(self, iterable, **kwargs):
        if isinstance(iterable, list):
            iterable = {str(i): value for i, value in enumerate(iterable)}
        super().__init__(iterable, **kwargs)

    def path(self, key, default=None):
        # nested get
        if '/' in key:
            k1, k2 = key.split('/', 1)
            return self.__class__(self[k1]).path(k2, default) if k1 in self else None
        else:
            return self.__class__(self[key]) if isinstance(self.get(key), (dict, Dict)) else self.get(key, default)

    def get(self, key, *args, **kwargs):
        value = super().get(key, *args, **kwargs)
        return Dict(value) if isinstance(value, dict) else value

    def gets(self, keys, default=None):
        if default is None:
            default = {}
        return [json.dumps(val)
                if isinstance(val := self.path(k, default.get(k)), (dict, list, Dict))
                else val
                for k in keys]

    def filter(self, keys, default=None):
        if default is None:
            default = {}
        return Dict({key: self.path(key, default.get(key)) for key in keys})

    def prints(self):
        for k, v in self.items():
            print(f'{k}: {v}')

    def __getitem__(self, key):
        value = super().__getitem__(key)
        return Dict(value) if isinstance(value, dict) else value
