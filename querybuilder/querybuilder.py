""" QueryBuilder: the data class """

from dataclasses import dataclass
from redis import Redis

from querybuilder.validation import Validation


@dataclass
class QueryBuilder:
    """
    Query Builder main class, containing essential information to run the cache query

    methods:
        validate(input_) -> is_valid(bool)
    """

    def __init__(self, redis: Redis, cache_name: str, sub_name: str, sub_attr: dict):
        """
        Query Builder initialization

        :param redis: Redis connection
        :param cache_name: cache name, a context name for dividing cache from another app
        :param sub_name: sub name, similar to table in SQL
        :param sub_attr: sub attributes, e.g. {"name": "TEXT"}
        """
        self.redis = redis
        self.cache_name = cache_name
        self.sub_name = sub_name
        self.sub_attr = sub_attr

    def validate(self, input_: dict) -> bool:
        """
        Validation for user input

        :param input_: user input, e.g. {"name": "Johnson", ...}
        :return: is_valid(bool)
        """
        # pylint: disable=R0911

        for col_name in self.sub_attr:
            if col_name not in input_:
                return False

            data = input_[col_name]
            data_type = self.sub_attr[col_name].lower()
            if 'not null' in data_type:
                if not Validation.is_not_null(data):
                    return False

            if 'text' in data_type:
                if not Validation.is_text(data):
                    return False
            elif 'integer' in data_type:
                if not Validation.is_integer(data):
                    return False
            elif 'real' in data_type:
                if not Validation.is_real(data):
                    return False
            elif 'boolean' in data_type:
                if not Validation.is_boolean(data):
                    return False

        return True
