from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.types import Boolean


class fts_match_word(GenericFunction):
    type = None
    name = 'fts_match_word'