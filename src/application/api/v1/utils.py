from pydantic import BaseModel, Field
from collections import namedtuple


LimitOffset = namedtuple("LimitOffset", ["limit", "offset"])



class Paginator(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(default=10, ge=1)


    def get_limit_and_offset(self) ->LimitOffset:
        offset = (self.page - 1) * self.page_size
        limit = offset + self.page_size
        return LimitOffset(limit, offset)
