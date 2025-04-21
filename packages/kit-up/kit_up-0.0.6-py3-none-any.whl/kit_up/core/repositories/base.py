from kit_up.core import models
from kit_up.core.mixins import require


class AbstractRepository:
    def get_model_type(self) -> type[models.BaseModel]:
        raise NotImplementedError


class AbstractAsyncRepository:
    def get_model_type(self) -> type[models.BaseModel]:
        raise NotImplementedError


class RequiresRepositoryMixin(require.RequiresMixin, requires="repository"):
    _repository: AbstractRepository


class RequiresAsyncRepositoryMixin(require.RequiresMixin, requires="repository"):
    _repository: AbstractAsyncRepository
