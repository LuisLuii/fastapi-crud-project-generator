# Fastapi CRUD Project Generator
[![Coverage Status](https://coveralls.io/repos/github/LuisLuii/fastapi-crud-project-generator/badge.svg?branch=main)](https://coveralls.io/github/LuisLuii/fastapi-crud-project-generator?branch=main)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1c2b9ba9a4fb497383429daa57d9c485)](https://www.codacy.com/gh/LuisLuii/fastapi-crud-project-generator/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LuisLuii/fastapi-crud-project-generator&amp;utm_campaign=Badge_Grade)
[![PyPI version](https://badge.fury.io/py/fastapi-crud-code-generator.svg)](https://badge.fury.io/py/fastapi-crud-code-generator)

A code generator that help you to establish a fastapi project with CRUD router from your Sqlalchemy model. Which supports following api:
>- Get one
>- Get many
>- Insert one
>- Insert many
>- Update one
>- Update many
>- Patch one
>- Patch many
>- Delete one
>- Delete many

## Quick Start with in-memory DB (or see the other ([example](https://github.com/LuisLuii/fastapi-crud-project-generator/tree/feature/fix_code_style/tutorial))


### Install
```python
pip install fastapi-crud-code-generator
```
### Prepare your Sqlalchemy schema
* You can use sqlacodegen to generate SQLAlchemy models for your table. This project is based on the model development and testing generated by sqlacodegen

```
from sqlalchemy import *
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata

class SampleTable(Base):
    __tablename__ = 'test_build_myself_memory'
    __table_args__ = (
        UniqueConstraint('primary_key', 'int4_value', 'float4_value'),
    )
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)
    char_value = Column(CHAR(10, collation='NOCASE'))
    date_value = Column(Date)
    float4_value = Column(Float, nullable=False)
    float8_value = Column(Float(53), nullable=False, default=10.10)
    int2_value = Column(SmallInteger, nullable=False)
    int4_value = Column(Integer, nullable=False)
    int8_value = Column(BigInteger, default=99)
    text_value = Column(Text)
    varchar_value = Column(String)

class SampleTableTwo(Base):
    __tablename__ = 'test_build_myself_memory_two'
    primary_key = Column(Integer, primary_key=True, autoincrement=True)
    bool_value = Column(Boolean, nullable=False, default=False)
    bytea_value = Column(LargeBinary)
```

### Use `crud_router_builder()` to generate the project to the executing folder (using in-memory sqlite db here)

```python
from fastapi_quickcrud_codegen.db_model import DbModel
from fastapi_quickcrud_codegen.misc.type import CrudMethods

from fastapi_quickcrud_codegen import crud_router_builder

model_list = [DbModel(db_model=SampleTable, prefix="/my_first_api", tags=["sample api"],
                      exclude_columns=['bytea_value']),
              DbModel(db_model=SampleTableTwo, prefix="/my_second_api", tags=["sample api"],
                      exclude_columns=['bytea_value'],crud_methods=[CrudMethods.FIND_ONE])]
crud_router_builder(
    db_model_list=model_list,
    # is_async=True,
    # database_url="sqlite+aiosqlite://",
    is_async=False,
    database_url="sqlite://"
)

```
<img width="1292" alt="image" src="https://user-images.githubusercontent.com/31765235/200206184-a16a8622-7db6-4c62-bb56-99cdee126493.png">


**crud_router_builder args**
- db_model_list `[Required[List[DbModel]]] `
    >  Model list of dict for code generate
  - `List[]`
    - `DbModel`
      - db_model `[Required[DeclarativeMeta]]`
      - prefix `[Required[str]]`
         > prefix for Fastapi's end point 
      - tags `[Required[List[str]]]`
         > list of tag for Fastapi's end point 
      - exclude_columns `[Optional[List[str]]]`
         > set the columns that not to be operated but the columns should nullable or set the default value)
      - crud_methods `[Opional[List[CrudMethods]]]`
        > - Create the following apis for that model, but default: [CrudMethods.FIND_MANY, CrudMethods.FIND_ONE, CrudMethods.CREATE_MANY, CrudMethods.PATCH_ONE, CrudMethods.PATCH_MANY, CrudMethods.PATCH_ONE, CrudMethods.UPDATE_MANY, CrudMethods.UPDATE_ONE, CrudMethods.DELETE_MANY, CrudMethods.DELETE_ONE] 
        ```
        - CrudMethods.FIND_ONE
        - CrudMethods.FIND_MANY
        - CrudMethods.UPDATE_ONE
        - CrudMethods.UPDATE_MANY
        - CrudMethods.PATCH_ONE
        - CrudMethods.PATCH_MANY
        - CrudMethods.CREATE_ONE
        - CrudMethods.CREATE_MANY
        - CrudMethods.DELETE_ONE
        - CrudMethods.DELETE_MANY
        ```
      
- is_async `[Required]`
    
    >  True for async; False for sync
    
- database_url  `[Optional (str)]`
    >  A database URL. The URL is passed directly to SQLAlchemy's create_engine() method so please refer to SQLAlchemy's documentation for instructions on how to construct a proper URL.
    
# Known limitations
* ❌ Please use composite unique constraints instead of multiple unique constraints
* ❌ Composite primary key is not supported
* ❌ Sqlalchemy table type model schema is not supported

# Design:
The model generation part and api router part refer to my another [project](https://github.com/LuisLuii/FastAPIQuickCRUD); The code generation part is using Jinja

## How to contribute more apis?
It will be super excited if you have any idea with api router/ model template. then you can follow the step as below to try to contribute.
1. Model generation
   1. Prepare Jinja template to `fastapi-crud-project-generator/src/fastapi_quickcrud_codegen/model/template`
   2. Prepare model code generation method from `fastapi_quickcrud_codegen.utils.schema_builder.ApiParameterSchemaBuilder`
   3. Generate the code from `fastapi_quickcrud_codegen/model/model_builder.py` 
2. CRUD Method Generation
   1. After the model generation, you can try to build your own api by your own model
   2. Modify `fastapi_quickcrud_codegen.utils.sqlalchemy_to_pydantic.sqlalchemy_to_pydantic`, `fastapi_quickcrud_codegen.misc.type.CrudMethods` and `fastapi_quickcrud_codegen.misc.crud_model.CRUDModel` to let project supports your api
   3. Prepare your api router Jinja template from `src/fastapi_quickcrud_codegen/model/template/route`
   4. Generate the code from `fastapi_quickcrud_codegen/model/crud_builder.py` 
   5. Update the api_register from `src/fastapi_quickcrud_codegen/crud_generator.py`
* use Sqlalchemy's sql.expression instead custom statement when building sql statement for your api
# Road map
#### Current State: Stable
#### Will do:
>- Support foreign tree in find api
>- Support foreign tree in insert api
>- Support foreign tree in update api
>- Support foreign tree in delete api
#### Good to have:
>- Support Sqlalchemy Table type model
