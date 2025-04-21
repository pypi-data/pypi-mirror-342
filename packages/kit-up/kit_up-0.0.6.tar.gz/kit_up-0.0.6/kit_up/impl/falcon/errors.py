import http
import typing as t

import falcon
from izulu import root


class ApiError(root.Error):
    STATUS_CODE: t.ClassVar[http.HTTPStatus]

    __template__ = "{title}: {description}"

    description: str
    title: str = root.factory(
        default_factory=lambda self: self.__class__.__name__,
        self=True,
    )

    @staticmethod
    def handle(req, resp, ex, params):  # noqa: ARG004
        # TODO(i.markevich): Log the error
        raise falcon.HTTPError(
            ex.STATUS_CODE,
            title=ex.title,
            description=ex.description,
        )


class BadRequestError(ApiError):
    STATUS_CODE = http.HTTPStatus.BAD_REQUEST


class NotFoundError(ApiError):
    STATUS_CODE = http.HTTPStatus.NOT_FOUND


class DuplicateEntryError(ApiError):
    STATUS_CODE = http.HTTPStatus.CONFLICT


class InternalServerError(ApiError):
    STATUS_CODE = http.HTTPStatus.INTERNAL_SERVER_ERROR


class ServiceUnavailableError(ApiError):
    STATUS_CODE = http.HTTPStatus.SERVICE_UNAVAILABLE
