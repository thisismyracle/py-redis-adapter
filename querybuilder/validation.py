""" Data type validation class """

from typing import Any


class Validation:
    """
    A class for data type validation only

    methods:
        is_not_nulL(data) -> is_valid(bool)
        is_integer(data) -> is_valid(bool)
        is_real(data) -> is_valid(bool)
        is_text(data) -> is_valid(bool)
        is_boolean(data) -> is_valid(bool)
    """

    @classmethod
    def is_not_null(cls, data: Any) -> bool:
        """
        Check if data is not null (None)

        :param data: input data
        :return: is_valid(bool)
        """
        if data is not None:
            return True
        return False

    @classmethod
    def is_integer(cls, data: Any) -> bool:
        """
        Check if data is an integer

        :param data: input data
        :return: is_valid(bool)
        """
        if isinstance(data, int):
            return True
        return False

    @classmethod
    def is_real(cls, data: Any) -> bool:
        """
        Check if data is a real number

        :param data: input data
        :return: is_valid(bool)
        """
        if isinstance(data, float):
            return True
        return False

    @classmethod
    def is_text(cls, data: Any) -> bool:
        """
        Check if data is a text

        :param data: input data
        :return: is_valid(bool)
        """
        if isinstance(data, str):
            return True
        return False

    @classmethod
    def is_boolean(cls, data: Any) -> bool:
        """
        Check if data is a boolean

        :param data: input data
        :return: is_valid(bool)
        """
        if isinstance(data, bool):
            return True
        return False
