import cx_Oracle

def connectToOracle():
    dsn_tns = cx_Oracle.makedsn('devengdb1.ip.devcerner.net', 1521, service_name='mstr.world')
    db = cx_Oracle.connect('v500', 'v500', dsn_tns)
    return  db

def returnChildTables(parent_table):
    db = connectToOracle()
    cur = db.cursor()
    query = """		SELECT
            UC1.TABLE_NAME AS CHILD_TABLE_NAME,
            UCC1.COLUMN_NAME AS CHILD_COLUMN_NAME,
        	UC2.TABLE_NAME AS PARENT_TABLE_NAME,
            UCC2.COLUMN_NAME AS PARENT_COLUMN_NAME
        FROM USER_CONSTRAINTS UC1
        INNER JOIN USER_CONSTRAINTS UC2
            ON UC1.R_CONSTRAINT_NAME = UC2.CONSTRAINT_NAME
            AND UC2.TABLE_NAME = '{}'
        INNER JOIN USER_CONS_COLUMNS UCC1
            ON UCC1.CONSTRAINT_NAME = UC1.CONSTRAINT_NAME
        INNER JOIN USER_CONS_COLUMNS UCC2
            ON UCC2.CONSTRAINT_NAME = UC2.CONSTRAINT_NAME
        ORDER BY CHILD_TABLE_NAME, CHILD_COLUMN_NAME"""

    cur.execute(query.format(parent_table))
    result = cur.fetchall()

    return result

def insertData(parent_table, child_tables, loop_cntr, varchar_prefix, begin_dttm):
    dsn_tns = cx_Oracle.makedsn('devengdb1.ip.devcerner.net', 1521, service_name='mstr.world')
    db2 = cx_Oracle.connect('v500', 'v500', dsn_tns)
    cur = db2.cursor()
    parent_table = parent_table
    child_tables = child_tables
    child_tables_varray = cur.arrayvar(cx_Oracle.STRING, child_tables)
    loop_cntr = loop_cntr
    ip_varchar_prefix = varchar_prefix
    ip_begin_dttm = begin_dttm
    output_childs = cur.var(cx_Oracle.STRING)
    output_inserts = cur.var(cx_Oracle.CLOB)


    l_query = cur.callproc("PKG_DYNAMIC_INSERTS_V1.SP_DYNAMIC_INSERTS",
                           [parent_table, child_tables_varray, loop_cntr, ip_varchar_prefix, ip_begin_dttm,
                            output_childs, output_inserts])


    output = []

    pks = l_query[5]
    output.append(pks)
    inserts = l_query[6]
    inserts_res = str(inserts).split('||')
    for i in inserts_res:
        output.append(i)

    db2.close()

    return output