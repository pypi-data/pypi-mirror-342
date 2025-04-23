import mysql.connector
from mysql.connector import errorcode
import traceback
import os

from dust.persist.sqlpersist import SqlPersist

from dust import Datatypes, ValueTypes, Operation, MetaProps, FieldProps
from dust.entity import Entity

SQL_TYPE_MAP = {
    Datatypes.INT: "INT",
    Datatypes.NUMERIC: "DOUBLE",
    Datatypes.BOOL: "TINYINT",
    Datatypes.STRING: "TEXT",
    Datatypes.BYTES: "MEDIUMBLOB",
    Datatypes.JSON: "TEXT",
    Datatypes.ENTITY: "TEXT"
}

CREATE_TABLE_TEMPLATE = "\
CREATE TABLE IF NOT EXISTS {{sql_table.table_name}} (\n\
    {% for field in sql_table.fields %}\
    {{ field.field_name }} {{ field.field_type }}{% if field.primary_key %} PRIMARY KEY{% endif %}{% if not loop.last %},{% endif %}\n\
    {% endfor %}\
)\n\
"

CREATE_TABLE_TEMPLATE_MULTI_PK = "\
CREATE TABLE IF NOT EXISTS {{sql_table.table_name}} (\n\
    {% for field in sql_table.fields %}\
    {{ field.field_name }} {{ field.field_type }},\n\
    {% endfor %}\n\
    PRIMARY KEY ({% for field in sql_table.primary_keys %}{{ field.field_name }}{% if not loop.last %},{% endif %}{% endfor %})\n\
)\n\
"

ALTER_TABLE_TEMPLATE = "\
ALTER TABLE {{sql_table.table_name}} \n\
    {% for field_mod in field_modifications %}\
    {{ field_mod }}{% if not loop.last %},{% endif %}\n\
    {% endfor %}\
\n\
"

DROP_TABLE_TEMPLATE = "\
DROP TABLE {{sql_table.table_name}}"

'''
INSERT_INTO_TABLE_TEMPLATE = "\
INSERT INTO {{sql_table.table_name}} (\
{% for field in sql_table.fields %}\
{{ field.field_name }}{% if not loop.last %},{% endif %}\
{% endfor %}\
) VALUES (\
{% for field in sql_table.fields %}\
%({{ field.field_name }})s{% if not loop.last %},{% endif %}\
{% endfor %}\
)\
"
'''
INSERT_INTO_TABLE_TEMPLATE = "\
INSERT INTO {{sql_table.table_name}} (\
{% for field in sql_table.fields %}\
{{ field.field_name }}{% if not loop.last %},{% endif %}\
{% endfor %}\
) VALUES (\
{% for field in sql_table.fields %}\
%s{% if not loop.last %},{% endif %}\
{% endfor %}\
)\
"


SELECT_TEMPLATE = "\
SELECT \
{% for field in sql_table.fields %}\
{{ field.field_name }}{% if not loop.last %},{% endif %} \
{% endfor %}\
FROM {{sql_table.table_name}} \
{% if where_filters %}\
WHERE \
{% for filter in where_filters %}\
{% if filter[1]|lower == 'in' %}\
{{ filter[0] }} {{ filter[1] }} ({% for v in filter[2] %}%({{ filter[0] }}{{loop.index}})s{% if not loop.last %},{% endif %}{% endfor %}) {% if not loop.last %}AND {% endif %}\
{% else %}\
{{ filter[0] }} {{ filter[1] }} %({{ filter[0] }})s {% if not loop.last %}AND {% endif %}\
{% endif %}\
{% endfor %}\
{% endif %}\
"

'''
UPDATE_TEMPLATE = "\
UPDATE {{sql_table.table_name}} SET \
{% for field in sql_table.fields %}\
{% if not field.primary_key and not field.base_field %}{{ field.field_name }} = %({{ field.field_name }})s{% if not loop.last %},{% endif %}{% endif %} \
{% endfor %}\
WHERE \
{% for field in sql_table.primary_keys %}{{ field.field_name }} = %({{ field.field_name }})s{% if not loop.last %},{% endif %}{% endfor %} \
"
'''
UPDATE_TEMPLATE = "\
UPDATE {{sql_table.table_name}} SET \
{% for field in sql_table.fields %}\
{% if not field.primary_key and not field.base_field %}{{ field.field_name }} = %s{% if not loop.last %},{% endif %}{% endif %} \
{% endfor %}\
WHERE \
{% for field in sql_table.primary_keys %}{{ field.field_name }} = %s{% if not loop.last %},{% endif %}{% endfor %} \
"

DELETE_TEMPLATE = "\
DELETE FROM {{sql_table.table_name}} \
WHERE _global_id = %s\
"

DELETE_TEMPLATE_WITH_WHERE = "\
DELETE FROM {{sql_table}} \
WHERE \
{% for where_filter in where_filters %}{{ where_filter[0] }} {{ where_filter[1] }} %({{ where_filter[0] }})s{% if not loop.last %} and {% endif %}{% endfor %} \
"

MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DB = os.environ.get('MYSQL_DB')

class MySQLPersist(SqlPersist):
    def __init__(self):
        super().__init__(**self.__db_api_kwargs())

    def __create_connection(self):
        conn = None
        try:
            conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, database=MYSQL_DB, charset='utf8', use_unicode=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        return conn

    def __close_connection(self, conn):
        if conn:
            conn.commit()
            conn.close()

    def __create_cursor(self, conn, prepared=False, buffered=True):
        if conn:
            return conn.cursor(buffered=buffered, prepared=prepared)

    def __close_cursor(self, c):
        if c:
            c.close()

    def __db_api_kwargs(self):
        return {
            "_create_connection": self.__create_connection,
            "_close_connection": self.__close_connection,
            "_create_cursor": self.__create_cursor,
            "_close_cursor": self.__close_cursor
        }

    def create_exectute_params(self, named_param=True):
        if named_param:
            return {}
        else:
            return []

    def add_execute_param(self, values, name, value, operator="=", named_param=True):
        if named_param:
            if operator and operator.lower() == "in":
                cnt = 1
                for v in value:
                    values[name+str(cnt)] = v
                    cnt += 1
            else:
                values[name] = value
        else:
            if operator and operator.lower() == "in":
                cnt = 1
                for v in value:
                    values.append(v)
            else:
                values.append(value)

    def table_exits(self, table_name, conn):
        try:
            cursor = self.__create_cursor(conn)
            cursor.execute("SELECT * FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s LIMIT 1;", {"table_schema": MYSQL_DB, "table_name": table_name})
            rows = cursor.fetchall()

            for row in rows:
                if row[2] == table_name:
                    return True
        except:
            traceback.print_exc()
        finally:
            self.__close_cursor(cursor)

        return False

    def create_table_template(self, sql_table):
        if len(sql_table.primary_keys) > 1:
            return CREATE_TABLE_TEMPLATE_MULTI_PK
        else:
            return CREATE_TABLE_TEMPLATE 

    def alter_table_template(self):
        return ALTER_TABLE_TEMPLATE 

    def delete_table_template(self):
        return DROP_TABLE_TEMPLATE 

    def alter_table(self, sql, conn):
        cursor = None
        try:
            cursor = self.__create_cursor(conn)
            cursor.execute(sql)
        except:
            print(sql)
            traceback.print_exc()
        finally:
            self.__close_cursor(cursor)

    def insert_into_table_template(self):
        return INSERT_INTO_TABLE_TEMPLATE

    def select_template(self, where_filters):
        return SELECT_TEMPLATE

    def update_template(self):
        return UPDATE_TEMPLATE

    def delete_template(self, where_filters=None):
        if where_filters:
            return DELETE_TEMPLATE_WITH_WHERE
        else:
            return DELETE_TEMPLATE

    def convert_value_to_db(self, field, value):
        if field.datatype == Datatypes.BOOL:
            if value == True:
                return 1
            else:
                return 0
        elif field.datatype == Datatypes.ENTITY and isinstance(value, Entity):
            return value.global_id()
        elif SQL_TYPE_MAP[field.datatype] == "TEXT":
            if value is not None and len(value) > 65500:
                print(f"Trunctating value to 65500 for {field.name}")
                return value[:65500]
            else:
                return value
        elif SQL_TYPE_MAP[field.datatype] == "MEDIUMBLOB":
            if value is not None and len(value) > 16777000:
                print(f"Value is longer than max size, returning None for {field.name}")
                return None
            else:
                return value
        else:
            return value

    def convert_value_from_db(self, field, value):
        if field.datatype == Datatypes.BOOL:
            if value == 1:
                return True
            else:
                return False
        else:
            return value

    def sql_type(self, datatype, valuetype, primary_key=False):
        if primary_key and datatype == Datatypes.STRING:
            return "VARCHAR(100)"
        elif valuetype:
            return SQL_TYPE_MAP[datatype]
        else:
            return "TEXT"
