# aquadb

version：1.1.1

下载地址：https://pypi.org/project/aquadb/#files

## 1、配置类

### (1) add_config

相关参数：

```python
Signature: add_config(user, password, host, port, sid, encoding='utf-8')
Docstring:
向配置文件中添加数据库连接配置信息。

Parameters
----------
user : str
    数据库用户名。

password : str
    数据库密码。

host : str
    数据库主机名。

port : str
    数据库端口。

sid : str
    数据库SID。

encoding : str, optional
    配置文件的编码格式，默认为 'utf-8'。

Raises
------
FileNotFoundError
    如果配置文件不存在。

Notes
-----
1. 本函数将指定的数据库连接配置信息加密后添加到配置文件中。
2. 配置文件默认命名为 'ocl.ini'，存放在与 `aquadb` 模块相同的目录中。
3. 如果配置文件不存在，将创建一个空的配置文件。

Examples
--------
>>> user = "my_user"
>>> password = "my_password"
>>> host = "localhost"
>>> port = "1521"
>>> sid = "ORCL"
>>> add_config(user, password, host, port, sid)
Type:      function
```

应用案例：

```python
from aquadb.configurator import add_config

user = 'scott'
passsword = '123456'
host = 'xxx.x.x.x'
port = 'xxxx'
sid = 'orcl'
add_config(user, password, host, port, sid)
```

注意：user、password、host、port、sid都不能为空，其中ini文件会默认使用user作为session。

### (2) set_config

相关参数：

```python
Signature: set_config(session, option, value, encoding='utf-8')
Docstring: <no docstring>
Type:      function
```

应用案例

```python
from aquadb.configurator import set_config

user = "scott"
option = "user"
value = "test"
set_config(session, option, value)
```

注意；不建议使用。

## 2、查询类

### (2) read_table

相关参数：

```python
Signature: read_table(usr, file=None, query=None, index=-1, **kwargs)
Docstring:
从数据库中查询结果并返回DataFrame。

Parameters
----------
usr : str
    数据库用户名。

file : str, optional
    存放SQL查询语句的文件路径。可以一个文件存放多个语句。

query : str, optional
    SQL查询语句。

index : int, optional
    位置索引，用于在SQL文件中获取查询语句。默认为-1，表示取最后一个语句。

kwargs : dict
    与 pandas 模块相关的其他参数。

Returns
-------
pandas.DataFrame
    查询结果的数据表。

Raises
------
cx_Oracle.Error
    如果在数据库连接或查询过程中出现错误。

ValueError
    如果未指定查询语句或无法从文件中获取查询语句。

Notes
-----
1. 本函数从数据库中查询数据，并将结果返回为 DataFrame。
2. 如果未提供查询语句 `query`，将尝试从文件 `file` 中获取语句。
3. `index` 参数指定在文件中选择哪个语句，默认为 -1，表示选择最后一个语句。

Examples
--------
>>> usr = "your_db_username"
>>> query = "SELECT * FROM your_table"
>>> result = read_table(usr, query=query)
>>> print(result)
Type:      function
```

应用案例：

调用query：

```python
from aquadb.query import read_table

usr = "scott"
query = r"""
select * from F0126;
"""
data = read_table(usr, query=query, file=None)
data.head()
```

注意：usr为用户需要访问的数据库名称，在ini文件中为session；query可以是多段SQL查询语句，默认取最后一条，可以通过index修改读取的SQL语句。

调用file：

```python
from aquadb.query import read_table

usr = 'scott'
file = 'SQL测试.sql'
data = read_table(usr, file, index=0)
data.head()
```

注意：usr为用户需要访问的数据库名称，在ini文件中为session；file可以是多段SQL查询语句，默认取最后一条，可以通过index修改读取的SQL语句。

该方法优先判断query是否存在，若存在则优先使用query。

### (2) fetch_all

相关参数：

```python
Signature: fetch_all(usr, file=None, query=None, index=-1, format_table=True, head=5)
Docstring:
使用cx_Oracle游标的方式查询数据并进行格式化输出。

Parameters
----------
usr : str
    数据库用户名。

file : str, optional
    存放SQL查询语句的文件路径，可以一个文件存放多个语句。

query : str, optional
    数据库查询语句。

index : int, optional
    索引位置，用于在SQL文件中获取查询语句。默认为 -1，表示取最后一个。

format_table : bool, optional
    是否格式化输出表格。默认为 True，即默认格式化。

head : int or None, optional
    输出前N条数据，默认值为 5，即默认输出前五条数据。如果 head 为 None 或 0，则输出全部。

Returns
-------
PrettyTable or list of tuples
    格式化后的输出表格（使用 PrettyTable 格式化）或元组列表（如果不格式化）。

Raises
------
cx_Oracle.Error
    如果在数据库连接或查询过程中出现错误。

Notes
-----
1. 本函数使用 cx_Oracle 游标方式查询数据，并提供了格式化输出的选项。
2. 如果未提供查询语句 `query`，将尝试从文件 `file` 中获取语句。
3. 可以通过设置 `format_table` 为 False，输出原始的元组列表。
4. 可以通过设置 `head` 为 None 或 0，输出所有数据。

Examples
--------
>>> usr = "your_db_username"
>>> query = "SELECT * FROM your_table"
>>> result = fetch_all(usr, query=query)
>>> print(result)
Type:      function
```

应用案例：

调用query:

```python
from aquadb.query import fetch_all

usr = 'scott'
query = 'select * from F0126; select * from F0126'
result = fetch_all(usr, query=query, head=5, format_table=True)
result
```

注意：usr为用户使用的数据库用户名，在ini文件中为session；query可以同时写多段SQL，默认取最后一段SQL；head为默认取前5行；format_table为是否格式化成表格，默认是格式化，若不格式化，则输出的是列表。

调用file：

```python
from aquadb.query import fetch_all

usr = 'scott'
file = 'SQL测试.sql'
result = fetch_all(usr, file, index=0, head=5, format_table=True)
result
```

注意：usr为用户使用的数据库用户名，在ini文件中为session；query可以同时写多段SQL，默认取最后一段SQL；head为默认取前5行；format_table为是否格式化成表格，默认是格式化，若不格式化，则输出的是列表。

该方法主要应用于校验数据。优先判断query是否存在，若存在则优先使用query。

### (3) fetch_one

相关参数：

```python
Signature: fetch_one(usr, file=None, query=None, index=-1, format_table=True)
Docstring:
使用cx_Oracle游标的方式查询单条数据并进行格式化输出。

Parameters
----------
usr : str
    数据库用户名。

file : str, optional
    存放SQL查询语句的文件路径，可以一个文件存放多个语句。

query : str, optional
    数据库查询语句。

index : int, optional
    索引位置，用于在SQL文件中获取查询语句。默认为 -1，表示取最后一个。

format_table : bool, optional
    是否格式化输出表格。默认为 True，即默认格式化。

Returns
-------
PrettyTable or tuple
    格式化后的输出表格（使用 PrettyTable 格式化）或单条记录的元组。

Raises
------
cx_Oracle.Error
    如果在数据库连接或查询过程中出现错误。

Notes
-----
1. 本函数使用 cx_Oracle 游标方式查询单条数据，并提供了格式化输出的选项。
2. 如果未提供查询语句 `query`，将尝试从文件 `file` 中获取语句。

Examples
--------
>>> usr = "your_db_username"
>>> query = "SELECT * FROM your_table WHERE id = 1"
>>> result = fetch_one(usr, query=query)
>>> print(result)
Type:      function
```

应用案例：

调用query:

```python
from aquadb.query import fetch_one

usr = 'scott'
query = 'select * from F0126'
result = fetch_one(usr, query=query, index=-1, format_table=True)
result
```

注意：usr为用户使用的数据库用户名，在ini文件中为session；query可以同时写多段SQL，默认取最后一段SQL；head为默认取前5行；format_table为是否格式化成表格，默认是格式化，若不格式化，则输出的是列表。

调用file：

```python
from aquadb.query import fetch_one

usr = 'scott'
file = 'SQL测试.sql'
result = fetch_one(usr, file, index=0, format_table=True)
result
```

注意：usr为用户使用的数据库用户名，在ini文件中为session；query可以同时写多段SQL，默认取最后一段SQL；head为默认取前5行；format_table为是否格式化成表格，默认是格式化，若不格式化，则输出的是列表。

该方法优只会输出一条数据，用于数据校验。先判断query是否存在，若存在则优先使用query。

## 3、执行类

### (1) to_execute

相关参数：

```python
Signature:
to_execute(
    usr,
    file=None,
    query=None,
    index=None,
    commit=False,
    series=False,
    tolerant=False,
)
Docstring:
执行数据库查询或语句，即只执行增、删、改。

Parameters
----------
usr : str
    数据库用户名。

file : str, optional
    存放SQL查询语句的文件路径，默认为 None。

query : str or list of str, optional
    要执行的SQL查询语句，可以是字符串或字符串列表，默认为 None。

index : int, optional
    当 query 是字符串列表时，指定要执行的语句索引，默认为 None。

commit : bool, optional
    是否执行提交操作，即提交事务，默认为 False。

series : bool, optional
    是否逐条执行多个语句，默认为 False。

tolerant : bool, optional
    是否容忍异常，即遇到异常是否继续执行，默认为 False。

Raises
------
cx_Oracle.Error
    如果在连接数据库时出现错误。

Exception
    如果在执行数据库查询或语句时出现错误。

Notes
-----
1. 本函数执行数据库查询或语句，并提供了一些选项来控制执行行为。
2. 可以选择执行单个语句或多个语句，以及是否提交事务。

Examples
--------
>>> query = "SELECT * FROM employees"
>>> to_execute('my_user', query=query, commit=True)
Type:      function
```

应用案例：

调用query:

```python
from aquadb.executor import to_execute

usr = 'scott'
query = """
drop table USER_LOAD_BREAK_TEST1;

create table USER_LOAD_BREAK_TEST1 AS
SELECT
    *
FROM USER_LOAD_BREAK;

drop table USER_LOAD_BREAK_TEST2;
create table USER_LOAD_BREAK_TEST2 AS
SELECT
    *
FROM USER_LOAD_BREAK;

drop table USER_LOAD_BREAK_TEST3;
create table USER_LOAD_BREAK_TEST3 AS
SELECT
    *
FROM USER_LOAD_BREAK;
"""
res = to_execute(usr, query=query, index=1)
```

注意：该方法是应用于增删改。usr为数据库用户名，在ini文件中为session；query可以写多段SQL语句，但index默认取最后一句，可以通过index按位置索引；commit为是否提交事务，默认不提交；series为是否将query中的SQL语句全部执行，默认为不全部执行，若需要全部执行，需要将index改为None；tolerant为是否在异常出现时继续执行下一段，常用于series生效时。

调用file：

```python
from aquadb.executor import to_execute

usr = 'scott'
file = 'SQL测试.sql'
res = to_execute(usr, query=query, index=-1)
```

注意：该方法是应用于增删改。usr为数据库用户名，在ini文件中为session；query可以写多段SQL语句，但index默认取最后一句，可以通过index按位置索引；commit为是否提交事务，默认不提交；series为是否将query中的SQL语句全部执行，默认为不全部执行，若需要全部执行，需要将index改为None；tolerant为是否在异常出现时继续执行下一段，常用于series生效时。

该方法应用于增删改。优先判断query是否存在，若存在则优先使用query。

### (2) to_proceduce

相关参数：

```python
Signature:
to_proceduce(
    usr,
    file=None,
    query=None,
    index=None,
    series=False,
    tolerant=False,
)
Docstring:
执行存储过程或 SQL 匿名块。

Parameters
----------
usr : str
    数据库用户名。

file : str, optional
    存放存储过程或 SQL 匿名块语句的文件路径，默认为 None。

query : str or list of str, optional
    要执行的存储过程或 SQL 匿名块语句，可以是字符串或字符串列表，默认为 None。

index : int, optional
    当 query 是字符串列表时，指定要执行的语句索引，默认为 None。

series : bool, optional
    是否逐条执行多个语句，默认为 False。

tolerant : bool, optional
    是否容忍异常，即遇到异常是否继续执行，默认为 False。

Raises
------
cx_Oracle.Error
    如果在连接数据库时出现错误。

Exception
    如果在执行存储过程或 SQL 匿名块时出现错误。

Notes
-----
1. 本函数执行存储过程或 SQL 匿名块，并提供了一些选项来控制执行行为。
2. 可以选择执行单个语句或多个语句。

Examples
--------
>>> procedure = "BEGIN my_procedure; END;"
>>> to_procedure('my_user', query=procedure)
Type:      function
```

应用案例：usr为数据库用户名，在ini文件中为session；query可以写多段SQL语句，但index默认取最后一句，可以通过index按位置索引；commit为是否提交事务，默认不提交；series为是否将query中的SQL语句全部执行，默认为不全部执行，若需要全部执行，需要将index改为None；tolerant为是否在异常出现时继续执行下一段，常用于series生效时。

调用query:

```python
from aquadb.executor import to_proceduce

usr = 'scott'
query = r"""
/*
这是一个注释
*/
declare
    view_exist number;
begin
    select count(1)
    into view_exist
    from all_tables
    where table_NAME = 'USER_LOAD_BREAK_TEST3';

    if view_exist > 0 then
        execute immediate 'drop table USER_LOAD_BREAK_TEST3';
    end if;

    /*运行*/
    -- ///
    execute immediate '
    create table USER_LOAD_BREAK_TEST3 AS
    SELECT
        *
    FROM USER_LOAD_BREAK
    ';
end;
"""
res = to_proceduce(usr, query=query, index=-1)
```

注意：usr为数据库用户名，在ini文件中为session；query可以写多段SQL语句，但index默认取最后一句，可以通过index按位置索引；commit为是否提交事务，默认不提交；series为是否将query中的SQL语句全部执行，默认为不全部执行，若需要全部执行，需要将index改为None；tolerant为是否在异常出现时继续执行下一段，常用于series生效时。

调用file：

```python
from aquadb.executor import to_proceduce

usr = 'scott'
file = 'SQL12.sql'
res = to_proceduce(usr, file, index=-1)
```

注意：

该方法应用于执行匿名块。优先判断query是否存在，若存在则优先使用query。





