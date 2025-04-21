import dataclasses
import decimal
import os

import marshmallow as mm

from kit_up.impl.mm import conf


#schema = conf.BaseConfSchema()
#
# OS_ENV = {}
# print(schema.load(OS_ENV))
#
# OS_ENV = dict(APP__CATEGORY__OPTION="VALUE")
# print(schema.load(OS_ENV))

for k, v in [
    ("DB__HOST", "db.fix.ru"),                            # str
    ("DB__PORT", "5432"),                                 # int
    ("FEATURES__ONE_ENABLED", "1"),                       # bool
    ("FEATURES__TWO_ENABLED", "true"),                    # bool
    ("FEATURES__THREE_ENABLED", "0"),                     # bool
    ("FEATURES__FOUR_ENABLED", "False"),                  # bool
    ("FEATURES__FIVE_ENABLED", "false"),                  # bool
    # ("API__TOKENS", "token1, token2,  token3,token4"),  # str seq ','-separated
    # ("API__OTHER_TOKENS", "[\"ports\",\"other\"]"),     # json seq escaped
    # ("API__ANOTHER_TOKENS", '["ports","other"]'),       # json seq
    ("GLOBAL__CPM", "123.45"),                            # float
    ("LOG_LEVEL", "INFO"),                                # non set with default
    # ("SPECIAL_CONFIG", "{\"ports\":{\"80\":\"asdfa\"}}"),
    # # dict very specific (json format)
    # ("SPECIAL_CONFIG_OTHER", '{"ports":{"80":"asdfa"}}'),
    # # dict very specific (json format)
]:
    os.environ["APP__" + k] = v


class DatabaseConfSchema(mm.Schema):
    host = mm.fields.String()
    port = mm.fields.Integer()

@dataclasses.dataclass(frozen=True, slots=True)
class DatabaseConfDto(
    conf.LoadEnvConfMixin,
    schema=DatabaseConfSchema,
    group=conf.EnvironGroup("db"),
):
    host: str
    port: int

class FeaturesConfSchema(mm.Schema):
    one_enabled = mm.fields.Boolean()
    two_enabled = mm.fields.Boolean()
    three_enabled = mm.fields.Boolean()
    four_enabled = mm.fields.Boolean()
    five_enabled = mm.fields.Boolean()

@dataclasses.dataclass(frozen=True, slots=True)
class FeaturesConfDto(
    conf.LoadEnvConfMixin,
    schema=FeaturesConfSchema,
    group=conf.EnvironGroup("Features"),
):
    one_enabled: bool
    two_enabled: bool
    three_enabled: bool
    four_enabled: bool
    five_enabled: bool
    six_enabled: bool = dataclasses.field(default=1)



class GlobalConfSchema(mm.Schema):
    cpm = mm.fields.Decimal()

@dataclasses.dataclass(frozen=True, slots=True)
class GlobalConfDto(
    conf.LoadEnvConfMixin,
    schema=GlobalConfSchema,
    group=conf.EnvironGroup("global"),
):
    cpm: decimal.Decimal


from pprint import pp
print(DatabaseConfDto.from_env("app"))
pp(FeaturesConfDto.from_env("app"))
print(GlobalConfDto.from_env("app"))
