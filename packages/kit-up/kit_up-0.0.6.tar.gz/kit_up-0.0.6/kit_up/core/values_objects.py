import abc
import uuid


class AbstractValueObject(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def auto(cls):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def value(self):
        raise NotImplementedError


class Id(AbstractValueObject, uuid.UUID):
    def __init__(self, uuid):
        super().__init__(int=uuid.int, is_safe=uuid.is_safe)

    @classmethod
    def auto(cls):
        return cls(uuid.uuid4())

    def __str__(self):
        return self.hex

    def as_uuid(self):
        return uuid.UUID(int=self.int, is_safe=self.is_safe)

    @classmethod
    def parse(cls, input):
        if isinstance(input, uuid.UUID):
            cls(input)
        return cls(uuid.UUID(input))

    @property
    def value(self):
        return self.hex


# # bits1 = ...
# # u = UUID(bits1)
# # i = ID(bits1)
# #
# # assert u == i
#
# # ValueObject - immutable
#
# user = User()
# print(user)
#
# group = Group()
# group.user
# group.member_count  # GroupLength(2)
#
# class GroupLength(int): ...
