import shutil
import unittest

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.orm import declarative_base

from src.fastapi_quickcrud_codegen import crud_router_builder, CrudMethods
from test.misc.common import *

Base = declarative_base()
metadata = Base.metadata


class SampleTable(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key', 'int4_value', 'float4_value']
    __tablename__ = 'test_build_myself'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )
    primary_key = Column(Integer, primary_key=True, info={'alias_name': 'primary_key'}, autoincrement=True,
                         server_default="nextval('test_build_myself_id_seq'::regclass)")
    bool_value = Column(Boolean, nullable=False, server_default=text("false"))
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text("now()"))
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text("10.10"))
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, server_default=text("99"))
    interval_value = Column(INTERVAL)
    json_value = Column(JSON)
    jsonb_value = Column(JSONB(astext_type=Text()))
    numeric_value = Column(Numeric)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    uuid_value = Column(UUID(as_uuid=True))
    varchar_value = Column(String)
    array_value = Column(ARRAY(Integer()))
    array_str__value = Column(ARRAY(String()))


class SampleTableTwo(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key']
    __tablename__ = 'test_build_myself_two'
    __table_args__ = (
        UniqueConstraint('primary_key'),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)


class Testing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        is_async = False
        if is_async:
            database_url = "postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres"
        else:
            database_url = "postgresql://postgres:1234@127.0.0.1:5432/postgres"

        crud_router_builder(
            db_model_list=[
                {
                    "db_model": SampleTable,
                    "prefix": "/my_first_api",
                    "tags": ["sample api"],
                    "exclude_columns": ['bytea_value'],
                    "crud_methods": [CrudMethods.PATCH_MANY],

                },
                {
                    "db_model": SampleTableTwo,
                    "prefix": "/my_second_api",
                    "tags": ["sample api"],
                    "exclude_columns": ['bytea_value'],
                    "crud_methods": [CrudMethods.PATCH_MANY],

                }
            ],
            is_async=is_async,
            database_url=database_url
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(template_root_directory)

    def test_hardcode(self):
        hard_code_validate()

    def test_project_generation(self):
        # root
        #   app
        app_expected = \
            """import uvicorn
from fastapi import FastAPI

from fastapi_quick_crud_template.route.test_build_myself import api as test_build_myself_router
from fastapi_quick_crud_template.route.test_build_myself_two import api as test_build_myself_two_router
app = FastAPI()

[app.include_router(api_route) for api_route in [
test_build_myself_router,test_build_myself_two_router,
]]

uvicorn.run(app, host="0.0.0.0", port=8000)"""
        validate_app(expected=app_expected)

        # common
        #   sql_session
        common_sql_session_expected='''import asyncio
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool


from fastapi_quick_crud_template.model.test_build_myself import SampleTable
from fastapi_quick_crud_template.model.test_build_myself_two import SampleTableTwo


SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:1234@127.0.0.1:5432/postgres"



engine = create_engine(SQLALCHEMY_DATABASE_URL,
                                        future=True,
                                        echo=True,
                                        pool_pre_ping=True,
                                        pool_recycle=7200,
                                        
                                        poolclass=StaticPool)
session = sessionmaker(bind=engine, autocommit=False)


def db_session() -> Generator:
    try:
        db = session()
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()'''
        validate_common_sql_session(common_sql_session_expected)

        # model
        model_test_build_myself_two_expected = '''from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import List, NewType, Optional, Union
import pydantic, uuid
from pydantic import BaseModel
from fastapi import Body, Query
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from fastapi_quick_crud_template.common.utils import ExcludeUnsetBaseModel, filter_none, value_of_list_to_str
from fastapi_quick_crud_template.common.db import Base
from fastapi_quick_crud_template.common.typing import ExtraFieldTypePrefix, ItemComparisonOperators, MatchingPatternInStringBase, PGSQLMatchingPatternInString, RangeFromComparisonOperators, RangeToComparisonOperators





class SampleTableTwo(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key']
    __tablename__ = 'test_build_myself_two'
    __table_args__ = (
        UniqueConstraint('primary_key'),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)





@dataclass
class SampleTableTwoPrimaryKeyModel:
    primary_key: int = Query(None, description=None)



    
PRIMARY_KEY_NAME = "primary_key"
    
    
UNIQUE_LIST = "primary_key"
    


@dataclass
class SampleTableTwoPatchManyRequestQueryModel:
    primary_key____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    primary_key____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    primary_key____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    primary_key____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    primary_key____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    primary_key____list: Optional[List[int]] = Query(None, description=None)
    bool_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    bool_value____list: Optional[List[bool]] = Query(None, description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


@dataclass
class SampleTableTwoPatchManyRequestBodyModel:
    bool_value: bool = Body(None, description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        filter_none(self)


class SampleTableTwoPatchManyItemResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None)
    bool_value: bool = Body(False)
    class Config:
        orm_mode = True


class SampleTableTwoPatchManyItemListResponseModel(BaseModel):
    __root__: List[SampleTableTwoPatchManyItemResponseModel]
    class Config:
        orm_mode = True'''
        validate_model("test_build_myself_two", model_test_build_myself_two_expected)

        model_test_build_myself_expected = '''from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import List, NewType, Optional, Union
import pydantic, uuid
from pydantic import BaseModel
from fastapi import Body, Query
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from fastapi_quick_crud_template.common.utils import ExcludeUnsetBaseModel, filter_none, value_of_list_to_str
from fastapi_quick_crud_template.common.db import Base
from fastapi_quick_crud_template.common.typing import ExtraFieldTypePrefix, ItemComparisonOperators, MatchingPatternInStringBase, PGSQLMatchingPatternInString, RangeFromComparisonOperators, RangeToComparisonOperators





class SampleTable(Base):
    primary_key_of_table = "primary_key"
    unique_fields = ['primary_key', 'int4_value', 'float4_value']
    __tablename__ = 'test_build_myself'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )
    primary_key = Column(Integer, primary_key=True, info={'alias_name': 'primary_key'}, autoincrement=True,
                         server_default="nextval('test_build_myself_id_seq'::regclass)")
    bool_value = Column(Boolean, nullable=False, server_default=text("false"))
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10))
    date_value = Column(Date, server_default=text("now()"))
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, server_default=text("10.10"))
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, server_default=text("99"))
    interval_value = Column(INTERVAL)
    json_value = Column(JSON)
    jsonb_value = Column(JSONB(astext_type=Text()))
    numeric_value = Column(Numeric)
    text_value = Column(Text)
    time_value = Column(Time)
    timestamp_value = Column(DateTime)
    timestamptz_value = Column(DateTime(True))
    timetz_value = Column(Time(True))
    uuid_value = Column(UUID(as_uuid=True))
    varchar_value = Column(String)
    array_value = Column(ARRAY(Integer()))
    array_str__value = Column(ARRAY(String()))





@dataclass
class SampleTablePrimaryKeyModel:
    primary_key: int = Query(None, description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        value_of_list_to_str(self, ['uuid_value'])



    
PRIMARY_KEY_NAME = "primary_key"
    
    
UNIQUE_LIST = "primary_key", "int4_value", "float4_value"
    


@dataclass
class SampleTablePatchManyRequestQueryModel:
    primary_key____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    primary_key____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    primary_key____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    primary_key____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    primary_key____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    primary_key____list: Optional[List[int]] = Query(None, description=None)
    bool_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    bool_value____list: Optional[List[bool]] = Query(None, description=None)
    char_value____str_____matching_pattern: Optional[List[PGSQLMatchingPatternInString]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    char_value____str: Optional[List[str]] = Query(None, description=None)
    char_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    char_value____list: Optional[List[str]] = Query(None, description=None)
    date_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    date_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    date_value____from: Optional[NewType(ExtraFieldTypePrefix.From, date)] = Query(None, description=None)
    date_value____to: Optional[NewType(ExtraFieldTypePrefix.To, date)] = Query(None, description=None)
    date_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    date_value____list: Optional[List[date]] = Query(None, description=None)
    float4_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    float4_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    float4_value____from: Optional[NewType(ExtraFieldTypePrefix.From, float)] = Query(None, description=None)
    float4_value____to: Optional[NewType(ExtraFieldTypePrefix.To, float)] = Query(None, description=None)
    float4_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    float4_value____list: Optional[List[float]] = Query(None, description=None)
    float8_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    float8_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    float8_value____from: Optional[NewType(ExtraFieldTypePrefix.From, float)] = Query(None, description=None)
    float8_value____to: Optional[NewType(ExtraFieldTypePrefix.To, float)] = Query(None, description=None)
    float8_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    float8_value____list: Optional[List[float]] = Query(None, description=None)
    int2_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    int2_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    int2_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    int2_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    int2_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    int2_value____list: Optional[List[int]] = Query(None, description=None)
    int4_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    int4_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    int4_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    int4_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    int4_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    int4_value____list: Optional[List[int]] = Query(None, description=None)
    int8_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    int8_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    int8_value____from: Optional[NewType(ExtraFieldTypePrefix.From, int)] = Query(None, description=None)
    int8_value____to: Optional[NewType(ExtraFieldTypePrefix.To, int)] = Query(None, description=None)
    int8_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    int8_value____list: Optional[List[int]] = Query(None, description=None)
    numeric_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    numeric_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    numeric_value____from: Optional[NewType(ExtraFieldTypePrefix.From, Decimal)] = Query(None, description=None)
    numeric_value____to: Optional[NewType(ExtraFieldTypePrefix.To, Decimal)] = Query(None, description=None)
    numeric_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    numeric_value____list: Optional[List[Decimal]] = Query(None, description=None)
    text_value____str_____matching_pattern: Optional[List[PGSQLMatchingPatternInString]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    text_value____str: Optional[List[str]] = Query(None, description=None)
    text_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    text_value____list: Optional[List[str]] = Query(None, description=None)
    time_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    time_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    time_value____from: Optional[NewType(ExtraFieldTypePrefix.From, time)] = Query(None, description=None)
    time_value____to: Optional[NewType(ExtraFieldTypePrefix.To, time)] = Query(None, description=None)
    time_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    time_value____list: Optional[List[time]] = Query(None, description=None)
    timestamp_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    timestamp_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    timestamp_value____from: Optional[NewType(ExtraFieldTypePrefix.From, datetime)] = Query(None, description=None)
    timestamp_value____to: Optional[NewType(ExtraFieldTypePrefix.To, datetime)] = Query(None, description=None)
    timestamp_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    timestamp_value____list: Optional[List[datetime]] = Query(None, description=None)
    timestamptz_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    timestamptz_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    timestamptz_value____from: Optional[NewType(ExtraFieldTypePrefix.From, datetime)] = Query(None, description=None)
    timestamptz_value____to: Optional[NewType(ExtraFieldTypePrefix.To, datetime)] = Query(None, description=None)
    timestamptz_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    timestamptz_value____list: Optional[List[datetime]] = Query(None, description=None)
    timetz_value____from_____comparison_operator: Optional[RangeFromComparisonOperators] = Query(RangeFromComparisonOperators.Greater_than_or_equal_to, description=None)
    timetz_value____to_____comparison_operator: Optional[RangeToComparisonOperators] = Query(RangeToComparisonOperators.Less_than.Less_than_or_equal_to, description=None)
    timetz_value____from: Optional[NewType(ExtraFieldTypePrefix.From, time)] = Query(None, description=None)
    timetz_value____to: Optional[NewType(ExtraFieldTypePrefix.To, time)] = Query(None, description=None)
    timetz_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    timetz_value____list: Optional[List[time]] = Query(None, description=None)
    uuid_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    uuid_value____list: Optional[List[uuid.UUID]] = Query(None, description=None)
    varchar_value____str_____matching_pattern: Optional[List[PGSQLMatchingPatternInString]] = Query([MatchingPatternInStringBase.case_sensitive], description=None)
    varchar_value____str: Optional[List[str]] = Query(None, description=None)
    varchar_value____list_____comparison_operator: Optional[ItemComparisonOperators] = Query(ItemComparisonOperators.In, description=None)
    varchar_value____list: Optional[List[str]] = Query(None, description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        value_of_list_to_str(self, ['uuid_value'])
        filter_none(self)


@dataclass
class SampleTablePatchManyRequestBodyModel:
    bool_value: bool = Body(None, description=None)
    char_value: str = Body(None, description=None)
    date_value: date = Body(None, description=None)
    float4_value: float = Body(None, description=None)
    float8_value: float = Body(None, description=None)
    int2_value: int = Body(None, description=None)
    int4_value: int = Body(None, description=None)
    int8_value: int = Body(None, description=None)
    interval_value: timedelta = Body(None, description=None)
    json_value: dict = Body(None, description=None)
    jsonb_value: Union[dict, list] = Body(None, description=None)
    numeric_value: Decimal = Body(None, description=None)
    text_value: str = Body(None, description=None)
    time_value: time = Body(None, description=None)
    timestamp_value: datetime = Body(None, description=None)
    timestamptz_value: datetime = Body(None, description=None)
    timetz_value: time = Body(None, description=None)
    uuid_value: uuid.UUID = Body(None, description=None)
    varchar_value: str = Body(None, description=None)
    array_value: List[int] = Body(None, description=None)
    array_str__value: List[str] = Body(None, description=None)
    def __post_init__(self):
        """
        auto gen by FastApi quick CRUD
        """
        value_of_list_to_str(self, ['uuid_value'])
        filter_none(self)


class SampleTablePatchManyItemResponseModel(BaseModel):
    """
    auto gen by FastApi quick CRUD
    """
    primary_key: int = Body(None)
    bool_value: bool = Body(None)
    char_value: str = Body(None)
    date_value: date = Body(None)
    float4_value: float = Body(...)
    float8_value: float = Body(None)
    int2_value: int = Body(...)
    int4_value: int = Body(...)
    int8_value: int = Body(None)
    interval_value: timedelta = Body(None)
    json_value: dict = Body(None)
    jsonb_value: Union[dict, list] = Body(None)
    numeric_value: Decimal = Body(None)
    text_value: str = Body(None)
    time_value: time = Body(None)
    timestamp_value: datetime = Body(None)
    timestamptz_value: datetime = Body(None)
    timetz_value: time = Body(None)
    uuid_value: uuid.UUID = Body(None)
    varchar_value: str = Body(None)
    array_value: List[int] = Body(None)
    array_str__value: List[str] = Body(None)
    class Config:
        orm_mode = True


class SampleTablePatchManyItemListResponseModel(BaseModel):
    __root__: List[SampleTablePatchManyItemResponseModel]
    class Config:
        orm_mode = True'''
        validate_model("test_build_myself", model_test_build_myself_expected)

        # route
        route_test_build_myself_two_expected = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from fastapi_quick_crud_template.common.utils import find_query_builder
from fastapi_quick_crud_template.common.sql_session import db_session
from sqlalchemy.exc import IntegrityError
from pydantic import parse_obj_as
from fastapi_quick_crud_template.model.test_build_myself_two import SampleTableTwo, SampleTableTwoPatchManyItemListResponseModel, SampleTableTwoPatchManyRequestBodyModel, SampleTableTwoPatchManyRequestQueryModel



api = APIRouter(tags=['sample api'],prefix="/my_second_api")



@api.patch("", status_code=200, response_model=SampleTableTwoPatchManyItemListResponseModel)
def partial_update_many_by_query(
                                                response: Response,
                                                update_data: SampleTableTwoPatchManyRequestBodyModel = Depends(),
                                                extra_query: SampleTableTwoPatchManyRequestQueryModel = Depends(),
                                                session=Depends(db_session)):
    model = SampleTableTwo

    extra_args = extra_query.__dict__
    update_args = update_data.__dict__
    filter_list: List[BinaryExpression] = find_query_builder(param=extra_args,
                                                             model=model)
    stmt = select(model).where(and_(*filter_list))
    sql_executed_result = session.execute(stmt)
    data_instance_list = [i for i in sql_executed_result.scalars()]


    if not data_instance_list:
        return Response(status_code=HTTPStatus.NOT_FOUND, headers={"x-total-count": str(0)})
    try:
        response_data = []
        for i in data_instance_list:
            for update_arg_name, update_arg_value in update_args.items():
                        setattr(i, update_arg_name, update_arg_value)
            response_data.append(i)

        result = parse_obj_as(SampleTableTwoPatchManyItemListResponseModel, response_data)
        response.headers["x-total-count"] = str(len(response_data))

        return result

    except IntegrityError as e:
        err_msg, = e.orig.args
        if 'unique constraint' not in err_msg.lower():
            raise e
        result = Response(status_code=HTTPStatus.CONFLICT, headers={"x-total-count": str(0)})
        return result'''
        validate_route("test_build_myself_two", route_test_build_myself_two_expected)
        route_test_build_myself_expected = '''from http import HTTPStatus
from typing import List, Union
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends, Response
from sqlalchemy.sql.elements import BinaryExpression
from fastapi_quick_crud_template.common.utils import find_query_builder
from fastapi_quick_crud_template.common.sql_session import db_session
from sqlalchemy.exc import IntegrityError
from pydantic import parse_obj_as
from fastapi_quick_crud_template.model.test_build_myself import SampleTable, SampleTablePatchManyItemListResponseModel, SampleTablePatchManyRequestBodyModel, SampleTablePatchManyRequestQueryModel



api = APIRouter(tags=['sample api'],prefix="/my_first_api")



@api.patch("", status_code=200, response_model=SampleTablePatchManyItemListResponseModel)
def partial_update_many_by_query(
                                                response: Response,
                                                update_data: SampleTablePatchManyRequestBodyModel = Depends(),
                                                extra_query: SampleTablePatchManyRequestQueryModel = Depends(),
                                                session=Depends(db_session)):
    model = SampleTable

    extra_args = extra_query.__dict__
    update_args = update_data.__dict__
    filter_list: List[BinaryExpression] = find_query_builder(param=extra_args,
                                                             model=model)
    stmt = select(model).where(and_(*filter_list))
    sql_executed_result = session.execute(stmt)
    data_instance_list = [i for i in sql_executed_result.scalars()]


    if not data_instance_list:
        return Response(status_code=HTTPStatus.NOT_FOUND, headers={"x-total-count": str(0)})
    try:
        response_data = []
        for i in data_instance_list:
            for update_arg_name, update_arg_value in update_args.items():
                        setattr(i, update_arg_name, update_arg_value)
            response_data.append(i)

        result = parse_obj_as(SampleTablePatchManyItemListResponseModel, response_data)
        response.headers["x-total-count"] = str(len(response_data))

        return result

    except IntegrityError as e:
        err_msg, = e.orig.args
        if 'unique constraint' not in err_msg.lower():
            raise e
        result = Response(status_code=HTTPStatus.CONFLICT, headers={"x-total-count": str(0)})
        return result'''
        validate_route("test_build_myself", route_test_build_myself_expected)
