-- zhus;
SELECT t.DEPTNO,
       t.DNAME,
       t.LOC
FROM SCOTT.DEPT t;

-- 注释1
SELECT
    t.ID,  -- z注释1
    t.COMPANY,  -- 公司名称
    t.SALARY
FROM SCOTT.F0126 t;

/*
作用：测试使用；
功能：编写SQL;
*/
select
    sysdate as sys_date
from dual;

select
    *
from USER_LOAD_BREAK;


SELECT
    *
FROM USER_LOAD_BREAK