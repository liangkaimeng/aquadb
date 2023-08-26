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
/

declare
    view_exist number;
begin
    select count(1)
    into view_exist
    from all_tables
    where table_NAME = 'USER_LOAD_BREAK_TEST4';

    if view_exist > 0 then
        execute immediate 'drop table USER_LOAD_BREAK_TEST4';
    end if;

    /*运行*/
    -- ///
    execute immediate '
    create table USER_LOAD_BREAK_TEST4 AS
    SELECT
        *
    FROM USER_LOAD_BREAK
    ';
end;
/