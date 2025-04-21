from datetime import datetime
from typing import Annotated

from pydantic import Field, PlainSerializer

from u_toolkit.datetime import to_naive, to_utc, to_utc_naive


DBSmallInt = Annotated[int, Field(ge=-32768, le=32767)]
DBInt = Annotated[int, Field(ge=-2147483648, le=2147483647)]
DBBigInt = Annotated[
    int, Field(ge=-9223372036854775808, le=9223372036854775807)
]
DBSmallSerial = Annotated[int, Field(ge=1, le=32767)]
DBIntSerial = Annotated[int, Field(ge=1, le=2147483647)]
DBBigintSerial = Annotated[int, Field(ge=1, le=9223372036854775807)]


# 去除时区信息
NaiveDatetime = Annotated[datetime, PlainSerializer(to_naive)]
# 将时区转成 UTC
UTCDateTime = Annotated[datetime, PlainSerializer(to_utc)]
# 将时间转成 UTC, 并且去除时区信息
UTCNaiveDateTime = Annotated[datetime, PlainSerializer(to_utc_naive)]
