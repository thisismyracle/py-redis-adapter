""" Cache sub initial class """

import json

from querybuilder.querybuilder import QueryBuilder


class Sub:
    """
    Cache sub initial class, where all the cache query begin

    methods:
        get_complete_key(key) -> complete_key(str)
        get(key,is_key_complete) -> value(dict) | None
        get_many(keys,is_key_complete) -> values(list[dict | None])
        get_all() -> values(list[dict])
        get_complete_val(key,val) -> complete_val(dict)
        set(key,val,is_key_complete,is_val_complete) -> is_success(bool)
        set_many(key_vals,is_key_complete,is_val_complete) -> is_success(bool)
        unset(key,is_key_complete) -> is_success(bool)
        unset_many(keys,is_key_complete) -> is_success(bool)
        unset_all() -> is_success(bool)
    """

    def __init__(self, query_builder: QueryBuilder):
        """
        Query Builder initialization

        :param query_builder: QueryBuilder object contains redis connection and sub info
        """
        self.query_builder = query_builder

    def get_complete_key(self, key: str | int) -> str:
        """
        Generates a complete key "<cache_name>/<sub_name>/<key>"

        :param key: the key of a sub, the value of first element in the sub_attr
        :return: complete_key in "<cache_name>/<sub_name>/<key>" format
        """
        return f'{self.query_builder.cache_name}/{self.query_builder.sub_name}/{str(key)}'

    # noinspection PyTypeChecker
    def get(self, key: str | int, is_key_complete: bool = False) -> dict | None:
        """
        Get cache from a key

        :param key: the key of a cache, the value of first element in the sub_attr
        :param is_key_complete: is key already in complete form or not
        :return: value(dict)
        """
        complete_key = key if is_key_complete else self.get_complete_key(key)
        val = self.query_builder.redis.get(complete_key)

        if val is None:
            return None

        return json.loads(val)

    def get_many(self, keys: list[str] | list[int], is_key_complete: bool = False)\
            -> list[dict | None]:
        """
        Get cache from a key list

        :param keys: a key list
        :param is_key_complete: is key already in complete form or not
        :return: value list
        """
        complete_keys = keys if is_key_complete else [self.get_complete_key(key) for key in keys]
        vals = self.query_builder.redis.mget(complete_keys)

        result = []
        for val in vals:
            if val is None:
                result.append(None)
                continue
            result.append(json.loads(val))

        return result

    def get_all(self) -> list[dict]:
        """
        Get all cache in the current cache context

        :return: list of values
        """
        key_prefix = self.get_complete_key('')
        _, complete_keys = self.query_builder.redis.scan(match=f'{key_prefix}*')

        return self.get_many(complete_keys, is_key_complete=True)

    def get_complete_val(self, key: str | int, val: dict) -> dict:
        """
        Generates a complete cache value, including the key itself

        :param key: the key of a cache, the value of first element in the sub_attr
        :param val: the val of a cache, the value of the rest in the sub_attr
        :return:  complete_val(dict)
        """
        sub_attr_list = list(self.query_builder.sub_attr.items())
        key_name = sub_attr_list[0][0]
        key_type = sub_attr_list[0][1].lower()

        temp_val = {}
        if 'integer' in key_type:
            temp_val[key_name] = int(key)
        else:
            temp_val[key_name] = str(key)

        temp_val = {**temp_val, **val}

        return temp_val

    def set(self, key: str | int, val: dict, is_key_complete: bool = False,
            is_val_complete: bool = False) -> bool:
        """
        Set cache with a single key

        :param key: the key of a cache, the value of first element in the sub_attr
        :param val: the val of a cache, the value of the rest in the sub_attr
        :param is_key_complete: is key already in complete form or not
        :param is_val_complete: is val already in complete form or not
        :return: is_success(bool)
        """
        complete_key = key if is_key_complete else self.get_complete_key(key)
        complete_val = val if is_val_complete else self.get_complete_val(key, val)

        if not self.query_builder.validate(complete_val):
            return False

        complete_val_str = str(json.dumps(complete_val))

        return self.query_builder.redis.set(complete_key, complete_val_str)

    def set_many(self, key_vals: dict[str, dict] | dict[int, dict], is_key_complete: bool = False,
                 is_val_complete: bool = False) -> bool:
        """
        Set cache with multiple keys and values

        :param key_vals: a dict contains  key and value pairs
        :param is_key_complete: is key already in complete form or not
        :param is_val_complete: is val already in complete form or not
        :return: is_success(bool)
        """
        temp_key_vals = {}
        for key, val in key_vals.items():
            complete_key = key if is_key_complete else self.get_complete_key(key)
            complete_val = val if is_val_complete else self.get_complete_val(key, val)

            if not self.query_builder.validate(complete_val):
                return False

            complete_val_str = str(json.dumps(complete_val))
            temp_key_vals[complete_key] = complete_val_str

        return self.query_builder.redis.mset(temp_key_vals)

    def unset(self, key: str | int, is_key_complete: bool = False) -> bool:
        """
        Unset a cache with a single key

        :param key: the key of a cache, the value of first element in the sub_attr
        :param is_key_complete: is key already in complete form or not
        :return: is_success(bool)
        """
        complete_key = key if is_key_complete else self.get_complete_key(key)
        return bool(self.query_builder.redis.delete(complete_key))

    def unset_many(self, keys: list[str] | list[int], is_key_complete: bool = False) -> bool:
        """
        Unset multiple cache with multiple keys

        :param keys: the key of a cache, the value of first element in the sub_attr
        :param is_key_complete: is key already in complete form or not
        :return: is_success(bool)
        """
        complete_keys = keys if is_key_complete else [self.get_complete_key(key) for key in keys]
        complete_vals = self.get_many(complete_keys, is_key_complete=True)

        is_all_ok = True
        for i, complete_key in enumerate(complete_keys):
            if complete_vals[i] is not None:
                if not self.unset(complete_key, is_key_complete=True):
                    is_all_ok = False
                    break

        if is_all_ok:
            return True

        key_vals = {complete_keys[i]: complete_vals[i] for i in range(len(keys))
                    if complete_vals[i] is not None}
        self.set_many(key_vals, is_key_complete=True, is_val_complete=True)
        return False

    def unset_all(self) -> bool:
        """
        Unset all cache in the context

        :return: is_success(bool)
        """
        key_prefix = self.get_complete_key('')
        _, complete_keys = self.query_builder.redis.scan(match=f'{key_prefix}*')

        return self.unset_many(complete_keys, is_key_complete=True)
