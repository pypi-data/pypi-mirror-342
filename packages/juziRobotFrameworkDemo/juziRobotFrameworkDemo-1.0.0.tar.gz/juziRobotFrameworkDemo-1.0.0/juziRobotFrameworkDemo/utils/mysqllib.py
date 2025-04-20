import logger
import pymysql

'''
Documentation: 查询操作mysql数据库的。
引用包名是atBasicLibrary，引用本python文件，请使用Library  atBasicLibrary/mysqlLib.py。
如果您觉得引用代码不方便，也可以使用框架提供的关键字Resource   atBasicLibray/keywords/[ ../keywords/sc/mysql.html | mysql.robot ],
文档在[ ../keywords/mysql.doc.html | 这里 ]。
'''


def _at_get_mysql_connection_with_config(config):
    '''
    通过标准配置连接数据库。底层方法。
   【config】: 字典类型，含有host,port,user,password,db等信息的配置.方法加了默认配置是charset=utf8
    RETURN: Connection类型

    Examples:
        |   方法                              |          参数                                                                                            |
        | at get mysql connection with config | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |                                    |
    '''
    try:
        logger.info("数据库连接" + str(config))
        if config.get("charset") is None:
            config['charset']='utf8'
        connection = pymysql.connect(**config)
        return connection
    except pymysql.OperationalError as e:
        logger.error('连接数据库失败，原因：%s' % e)
        raise AssertionError(e)
    except pymysql.MySQLError as e:
        logger.error('连接数据库失败，原因：%s' % e)
        raise AssertionError('连接数据库失败，原因：%s' % e)

def _at_get_mysql_connection_with_host_and_port_config(config):
    '''
    通过适应proplus的配置(非标准配置,类似于host_and_port=127.0.0.1:3306)连接数据库。底层方法。
   【config】: 字典类型，含有host_and_port,user,password,db等信息的配置
    RETURN: Connection

    Examples:
        |   方法                                             |          参数                                                                                              |
        | at get mysql connection with host and port config | {"host_and_port":"127.0.0.1:3306","user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    logger.info("数据库连接" + str(config) + ",需要转化成标准配置。")
    host_and_port = config.get('host_and_port')
    if host_and_port is None:
        raise AssertionError("数据库连接配置host_and_port不存在")
    host_and_port_list = str.split(host_and_port, ":")
    if len(host_and_port_list) != 2:
        raise AssertionError("格式错误，请选择类似格式127.0.0.1:3306：  【" + host_and_port + "】")
    host = host_and_port_list[0]
    port = int(host_and_port_list[1])
    #del config['host_and_port']
    config['host']= host
    config['port'] = port
    if config.get("charset") is None:
        config['charset'] = 'utf8'
    newConfig = {}
    for key in  config:
        if key=='host_and_port':
            continue
        newConfig[key]=config.get(key)
    return _at_get_mysql_connection_with_config(newConfig)

def _at_execute_sql(conn,sql):
    '''
    操作数据库数据。
   【conn】:Connection类型，数据库连接,
   【sql】: String类型，执行的sql,
    RETURN: Int类型，影响数据库数据行数.

    Examples:
        | 方法            |      参数      |  参数 |
        | at execute sql |  <Connection> | <sql> |
    '''
    cursor = conn.cursor()
    try:
        logger.info("\n数据库执行SQL: " + sql, html=True, also_console=True)
        count = cursor.execute(sql)
        logger.info("被影响的行数: " + str(count), html=True, also_console=True)
        conn.commit()  # 提交事务
        return count
    except pymysql.MySQLError as e:
        conn.rollback()  # 若出错了，则回滚
        logger.error("数据库错误: " + e)
        raise AssertionError("数据库错误: "+e)

    finally:
        try:
            cursor.close()
        except pymysql.MySQLError as e:
            logger.error("关闭cursor出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭cursor出错: " + e)
        try:
            conn.close()
        except pymysql.MySQLError as e:
            logger.error("关闭数据库连接出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭数据库连接出错: " + e)

def _at_query(conn,sql):
    '''
    查询所有数据。返回嵌套字典的列表。
   【conn】:Connection类型，数据库连接
   【sql】: String类型，执行的sql
    RETURN: 列表，列表里嵌套字典

    Examples:
        |    方法     |      参数     |  参数  |
        | at query   |  <Connection> | <sql> |
    '''
    cursor = conn.cursor()
    try:
        logger.info("\n数据库执行SQL: " + sql, html=True, also_console=True)
        count = cursor.execute(sql)
        # 取出所有行
        result = cursor.fetchall()
        fields_list=[]
        for field in cursor.description:
            #field[0]是field名字，如果使用别名，就是别名
            fields_list.append(field[0])
        conn.commit()  # 提交事务
        if result is None or len(result) == 0:
            logger.info("数据库返回结果: None", html=True, also_console=True)
            return None
        result_list=[]
        for i in range(len(result)):
            row_dict={}
            row=result[i]
            for j in range(len(row)):
                row_dict[fields_list[j]]=row[j]
            result_list.append(row_dict)
        logger.info("数据库返回结果: " + str(result_list), html=True, also_console=False)
        return result_list
    except pymysql.MySQLError as e:
        conn.rollback()  # 若出错了，则回滚
        logger.error("数据库错误: " + e)
        raise AssertionError("数据库错误: " + e)

    finally:
        try:
            cursor.close()
        except pymysql.MySQLError as e:
            logger.error("关闭cursor出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭cursor出错: " + e)
        try:
            conn.close()
        except pymysql.MySQLError as e:
            logger.error("关闭数据库连接出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭数据库连接出错: " + e)

def _at_query_one(conn,sql):
    '''
    查询一条数据。返回字典。
   【conn】:Connection类型，数据库连接
   【sql】: String类型，执行的sql
    RETURN: 字典类型

    Examples:
        |       方法     |      参数     |  参数  |
        | at query one  |  <Connection> | <sql> |
    '''
    cursor = conn.cursor()
    try:
        logger.info("\n数据库执行SQL: " + sql, html=True, also_console=True)
        count = cursor.execute(sql)
        # 取出所有行
        result = cursor.fetchone()
        fields_list=[]
        for field in cursor.description:
            #field[0]是field名字，如果使用别名，就是别名
            fields_list.append(field[0])
        conn.commit()  # 提交事务
        result_dict={}
        if result is None or len(result)==0:
            logger.info("数据库返回结果: None", html=True, also_console=True)
            return None
        for index in range(len(result)):
            result_dict[fields_list[index]]=result[index]
        logger.info("数据库返回结果: " + str(result_dict), html=True, also_console=True)
        return result_dict
    except pymysql.MySQLError as e:
        conn.rollback()  # 若出错了，则回滚
        logger.error("数据库错误: " + e)
        raise AssertionError("数据库错误: " + e)

    finally:
        try:
            cursor.close()
        except pymysql.MySQLError as e:
            logger.error("关闭cursor出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭cursor出错: " + e)
        try:
            conn.close()
        except pymysql.MySQLError as e:
            logger.error("关闭数据库连接出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭数据库连接出错: " + e)

def at_execute_sql_with_config(sql,config):
    '''
    通过配置configure，获得数据库连接。然后根据sql操作数据库，返回数据是影响的行数int。
   【sql】: String类型,查询的sql
   【config】: 字典类型,含有host,port,user,password,db等信息的配置
    RETURN: Int类型，影响的行数。

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#Execute%20database%20mysql%20data | Execute database mysql data],
    [../keywords/mysql.doc.html#操作数据库mysql数据 | 操作数据库mysql数据],


    Examples:
        |       关键字                | 参数   |  参数                                                                                                     |
        | at execute sql with config | <sql>  | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    conn = _at_get_mysql_connection_with_config(config)
    return _at_execute_sql(conn, sql)

def at_execute_mysql_sql(sql,config):
    '''
    通过配置configure，获得数据库连接。然后根据sql操作数据库，返回数据是影响的行数int。
   【sql】: String类型,查询的sql
   【config】: 字典类型,含有host_and_port,user,password,db等信息的配置
    RETURN: tulple类型数据。

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#Execute%20mysql%20data | Execute mysql data],
    [../keywords/mysql.doc.html#操作mysql数据 | 操作mysql数据],

    Examples:
        |       关键字          | 参数   |  参数                                                                                                     |
        | at execute mysql sql | <sql>  | {"host_and_port":"127.0.0.1:3306","user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    conn = _at_get_mysql_connection_with_host_and_port_config(config)
    return _at_execute_sql(conn,sql)

def at_call_function(function,config,arguments=None):
    '''
    通过配置configure，获得数据库连接。然后根据function和arguments调用存储过程或者函数
    :param function: 存储过程或者函数名，String类型
    :param arguments: 列表，参数
    :param config: 数据库配置
    :return:
    '''
    conn = _at_get_mysql_connection_with_host_and_port_config(config)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if arguments is None:
        return cursor.callproc(function)
    else:
        cursor.callproc(function,tuple(arguments))
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result

def at_query_mysql_with_config(sql,config):
    '''
    通过配置configure，获得数据库连接。然后根据sql查询所有数据。返回结果是嵌套字典的列表。
   【sql】: String类型,查询的sql
   【config】: 字典类型,含有host,port,user,password,db等信息的配置
    RETURN: 列表，嵌套字典。

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#Query%20database%20mysql%20data | Query database mysql data],
    [../keywords/mysql.doc.html#查询数据库mysql数据 | 查询数据库mysql数据],

    Examples:
        |       关键字                | 参数   |  参数                                                                                                     |
        | at query mysql with config | <sql>  | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    conn = _at_get_mysql_connection_with_config(config)
    return _at_query(conn,sql)

def at_query_mysql(sql,config):
    '''
    通过host:port风格的configure配置，获得数据库连接。然后根据sql查询所有数据。返回结果是嵌套字典的列表。
   【sql】: String类型,查询的sql
   【config】: 字典类型,含有host,port,user,password,db等信息的配置
    RETURN: 列表，嵌套字典。

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#query%20mysql%20data | query mysql data],
    [../keywords/mysql.doc.html#查询mysql数据 | 查询mysql数据],

    Examples:
        |       关键字    | 参数   |  参数                                                                                                       |
        | at query mysql | <sql>  | {"host_and_port":"127.0.0.1:3306","user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    conn = _at_get_mysql_connection_with_host_and_port_config(config)
    return _at_query (conn,sql)

def at_query_one_with_config(sql,config):
    '''
    通过configure配置，获得数据库连接。然后根据sql查询1条数据。返回结果是字典。
   【sql】: String类型,查询的sql。
   【config】: 字典类型,含有host,port,user,password,db等信息的配置。
    RETURN: 字典类型数据。

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#Query%20database%20Only%20One%20mysql%20data | Query database only one mysql data],
    [../keywords/mysql.doc.html#查询数据库mysql一条数据 | 查询数据库mysql一条数据],

    Examples:
        |       关键字              | 参数   |  参数                                                                                                     |
        | at query one with config | <sql>  | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    conn = _at_get_mysql_connection_with_config(config)
    return _at_query_one(conn,sql)

def at_mysql_query_one(sql,config):
    '''
    通过host:port配置的configure，获得数据库连接。然后根据sql查询1条数据。返回结果是字典.
   【sql】: String类型,查询的sql.
   【config】: 字典类型,含有host,port,user,password,db等信息的配置.
    RETURN: 字典类型数据.

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#query%20mysql%20only%20one%20data | query mysql only one data],
    [../keywords/mysql.doc.html#查询mysql一条数据 | 查询mysql一条数据],

    Examples:
        |       关键字         | 参数   |  参数                                                                                                       |
        | at mysql query one  | <sql>  | {"host_and_port":"127.0.0.1:3306","user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    conn = _at_get_mysql_connection_with_host_and_port_config(config)
    return _at_query_one(conn,sql)

def at_get_row_column_value(dict_list,row_index,field_name):
    '''
    通过查询的数据结果，行数，field名 查询具体的mysql数据。查询一条数据不需要用这个方法。
    【dict_list】: list类型，存字典。
    【row_index】:是列表的行数。Int类型，从0开始。
    【field_name】:是字典的key。String类型。
    RETURN 不定类型

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#Get%20mysql%20dict%20data| Get mysql dict data],
    [../keywords/mysql.doc.html#获得mysql字典数据 | 获得mysql字典数据],

    Examples:
        |   关键字                 |                         参数                   | 参数 | 参数 |  结果  |
        | at get row column value | [{"aa":123,"bb":"333"},{"aa":456,"bb":"666"}] |  1   |  bb  |   666 |
    '''
    if dict_list is None or len(dict_list)==0:
        logger.info("数据为空")
        return None
    if row_index  >= len(dict_list):
        logger.info("选择行数大于数据数目")
        return None
    dictionary= dict_list[row_index]
    return dictionary.get(field_name)

