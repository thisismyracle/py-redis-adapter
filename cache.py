""" The main file for using Cache """

import json
from redis import Redis

from querybuilder.querybuilder import QueryBuilder
from querybuilder.sub import Sub


class Cache:
    """
    Cache class

    methods:
        setup_passphrase(new_passphrase) -> None
        load_blueprint() -> is_success(bool)
        save_blueprint() -> is_success(bool)
        is_admin(passphrase) -> is_admin(bool)
        is_sub_exists(sub_name) -> is_exists(bool)
        create_sub(sub_name,sub_attr,passphrase) -> is_success(bool)
        delete_sub(sub_name,passphrase) -> is_success(bool)
        sub(sub_name) -> sub(Sub)
    """

    def __init__(self, cache_name: str, redis_host: str, redis_port: int):
        """
        Cache initialization

        :param cache_name: name of the cache
        :param redis_host: the IP address where the redis is hosted
        :param redis_port: the port where the redis is hosted
        """
        self.cache_name = cache_name
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.passphrase = None
        self.blueprint = {}
        self.blueprint_path = f'{self.cache_name}_blueprint.json'
        self.load_blueprint()

        try:
            self.redis = Redis(host=redis_host, port=redis_port)
            self.redis.ping()
        except ConnectionError as exc:
            raise exc

    def setup_passphrase(self, new_passphrase: str):
        """
        Set up a new passphrase to perform an administrative task

        :param new_passphrase: a new passphrase(str)
        :return: None
        """
        self.passphrase = new_passphrase
        print('New passphrase has been set.')

    def load_blueprint(self) -> bool:
        """
        Load saved blueprint

        :return: is_success(bool)
        """
        try:
            with open(self.blueprint_path, 'r', encoding='UTF-8') as file:
                self.blueprint = json.loads(file.read())
        except IOError:
            return False
        return True

    def save_blueprint(self) -> bool:
        """
        Save the current blueprint

        :return: is_success(bool)
        """
        try:
            with open(self.blueprint_path, 'w+', encoding='UTF-8') as file:
                file.write(json.dumps(self.blueprint, indent=4))
        except IOError:
            return False
        return True

    def is_admin(self, passphrase: str) -> bool:
        """
        Check if you can perform administrative task or not

        :param passphrase: passphrase for administrative level methods
        :return: is_admin(bool)
        """
        if self.passphrase is None:
            err_msg = 'Passphrase is not set. Please call "setup_passphrase(new_passphrase)".'
            raise ValueError(err_msg)

        if passphrase == self.passphrase:
            return True
        return False

    def is_sub_exists(self, sub_name: str) -> bool:
        """
        Check if the specified sub is already exists

        :param sub_name: sub name, similar to table in SQL
        :return: is_exists(bool)
        """
        if sub_name in self.blueprint:
            return True
        return False

    def create_sub(self, sub_name: str, sub_attr: dict, passphrase: str | None = None) -> bool:
        """
        Creates new sub in the cache

        :param sub_name: sub name, similar to table in SQL
        :param sub_attr: sub attributes, e.g. {"name": "TEXT"}
        :param passphrase: passphrase for administrative level methods
        :return: is_success(bool)
        """
        if passphrase is None:
            err_msg = 'Please provide "passphrase" in the args to perform administrative methods.'
            raise ValueError(err_msg)
        if not self.is_admin(passphrase):
            raise ValueError('The given passphrase is not match, sub creation failed.')
        if self.is_sub_exists(sub_name):
            raise KeyError(f'Sub named `{sub_name}` is already exists, sub creation failed.')

        sub_attr_list = list(sub_attr.items())
        key_type = sub_attr_list[0][1]
        if 'real' in key_type or 'boolean' in key_type:
            raise ValueError('The key should be in a TEXT or INTEGER data type.')

        self.blueprint[sub_name] = sub_attr
        if self.save_blueprint():
            print(f'Sub `{sub_name}` has been created.')
            return True

        print(f'Sub creation failed, cannot access `{self.blueprint_path}`.')
        del self.blueprint[sub_name]
        return False

    def delete_sub(self, sub_name: str, passphrase: str | None = None) -> bool:
        """
        Delete existing sub from the cache, and its cache

        :param sub_name: sub name, similar to table in SQL
        :param passphrase: passphrase for administrative level methods
        :return: is_success(bool)
        """
        if passphrase is None:
            err_msg = 'Please provide "passphrase" in the args to perform administrative methods.'
            raise ValueError(err_msg)
        if not self.is_admin(passphrase):
            raise ValueError('The given passphrase is not match, sub creation failed.')
        if not self.is_sub_exists(sub_name):
            raise KeyError(f'There is no Sub named `{sub_name}`. Sub deletion failed.')

        temp_sub = self.blueprint[sub_name]
        del self.blueprint[sub_name]

        is_del_rows_success = False
        temp_redis = {}
        try:
            prefix = f'{self.cache_name}/{sub_name}/'
            for key in self.redis.scan_iter(f'prefix:{prefix}*'):
                temp_redis[key] = self.redis.get(key)
                self.redis.delete(key)
            is_del_rows_success = True
        except NameError:
            pass

        if is_del_rows_success:
            if self.save_blueprint():
                print(f'Sub `{sub_name}` has been deleted.')
                return True

        print('Sub deletion failed. No sub has been deleted.')
        self.blueprint[sub_name] = temp_sub
        self.redis.mset(temp_redis)
        return False

    def sub(self, sub_name: str) -> Sub:
        """
        The cache query builder starts here, get the specified sub to starts query

        :param sub_name: sub name, similar to table in SQL
        :return: Sub object
        """
        if not self.is_sub_exists(sub_name):
            raise NameError(f'There is no sub named `{sub_name}.`')

        qb = QueryBuilder(self.redis, self.cache_name, sub_name, self.blueprint[sub_name])

        return Sub(qb)
