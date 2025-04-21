from kit_up.core.domains import base
from kit_up.core.mixins import require


# - API / Presentation
# adapters?
#   - falcon

# class DataAccessGate(AbstractConstructor):
#     def deconstruct(self, model, **kwargs) -> "OrmModel": ...
#
#     def construct(self, orm_model, **kwargs) -> "Model": ...
#
#     # for entity creation
#     def initialize(self, data) -> "OrmModel": ...


class Gate:
    def __init__(self):
        self._mm = "kls"
        self._schema = self._mm()

    def construct(self, data, *other: dict, partial: bool = False):
        return self._schema.load(
            data,
            *other,
            many=bool(other),
            partial=partial,
        )

    def deconstruct(self, model, *models):
        return self._schema.dump(model, *models, many=bool(models))


class RequiresGateMixin(require.RequiresMixin, requires="gate"):
    _gate: Gate


# 1. read           | req.body
# 2. deserialize    | req.media
# 3.a. construct    | construct(media)          | <-- !!!
# 3.b. construct    | construct(path params)    | <-- !!!
# 3.c. construct    | construct(query params)   | <-- !!!
# 3.d. construct    | construct(headers)        | <-- !!!
# -. validate       | <optional> presentation validation  | <-- !!!
# 4. validate       | #domain#
# 5. process        | #domain#
# 6. deconstruct    | deconstruct(obj)  | <-- !!!
# 7. serialize      | resp.media = deconstructed
# 8. write          | resp.body


class Resource(base.RequiresDomainMixin, RequiresGateMixin):
    def get(self, identity):  # construct identity: /objects/{id:uuid}
        model = self._domain.get(identity)
        result = self._gate.deconstruct(model)
        return result

    def update(self, identity, inputs):
        updates = self._gate.construct(inputs, partial=True)
        model = self._domain.update(identity, updates)
        result = self._gate.deconstruct(model)
        return result

    def delete(self, identity):
        self._domain.delete(identity)


class Collection(base.RequiresDomainMixin, RequiresGateMixin):
    def create(self, inputs):
        data = self._gate.construct(inputs)
        model = self._domain.create(data)
        result = self._gate.deconstruct(model)
        return result
        # TODO(dburmistrov): resp.location = image.uri
        #   resp.status = falcon.HTTP_201

    def filter(self, **clauses):
        models = self._domain.filter(*clauses)
        return self._gate.deconstruct(*models)
