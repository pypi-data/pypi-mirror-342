import sqlalchemy as sa
from sqlalchemy_mixins import serialize


class SqlalchemyAdapterMixin(serialize.SerializeMixin):
    @classmethod
    def get_identity_qualifier(cls):
        result = []
        for pk in sa.inspection.inspect(cls).primary_key:
            result.append(pk.name)

        if len(result) > 1:
            return result[0]
        elif result:
            return tuple(result)
        else:
            return None

    def get_identity(self):
        return getattr(self, self.get_identity_qualifier())

    def as_dict(self):
        return self.to_dict()
