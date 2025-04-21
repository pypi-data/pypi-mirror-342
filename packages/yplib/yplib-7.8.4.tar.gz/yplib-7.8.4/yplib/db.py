from yplib import *

# 创建一个线程本地存储对象
__THREAD_LOCAL_DB_DATA = threading.local()


# 有关数据库操作的类
def get_connect(database=None, user=None, password=None, charset='utf8mb4', port=3306, host=None):
    return pymysql.connect(database=database, user=user, password=password, charset=charset, port=port, host=host)


def get_connect_from_config(db_config='db', database=None, user=None, password=None, charset=None, port=None, host=None):
    config_db = get_config_data(db_config)
    database = database or config_db.get('database')
    user = user or config_db.get('user')
    host = host or config_db.get('host')
    password = password or config_db.get('password')
    port = port or config_db.get('port', 3306)
    charset = charset or config_db.get('charset', 'utf8mb4')
    # 生成线程标识
    thread_key = f"{db_config}_{database}" if database else db_config
    conn_pool = getattr(__THREAD_LOCAL_DB_DATA, 'get_connect_from_config', {})
    # 获取连接，如果没有，则创建新的连接并保存到线程本地存储
    if thread_key not in conn_pool:
        conn_pool[thread_key] = get_connect(database=database, user=user, password=password, charset=charset, port=port, host=host)
        __THREAD_LOCAL_DB_DATA.get_connect_from_config = conn_pool  # 确保保存到线程本地存储
    return conn_pool[thread_key]


def exec_sql(sql='', db_conn=None, db_config='db', commit=True, is_log=False, database=None):
    """
    执行 SQL 语句，并提交（默认提交）。

    :param sql: 需要执行的 SQL 语句（字符串或列表）。
    :param db_conn: 数据库连接对象，若为空则自动获取。
    :param db_config: 数据库配置名称。
    :param commit: 是否提交事务（默认提交）。
    :param is_log: 是否记录日志。
    :param database: 具体的数据库，会覆盖 db_config 中的设置。
    """
    if not sql:
        is_log and to_log_file("db_conn is None or sql is None or sql == '', so return")
        return
    # 获取数据库连接（使用线程本地存储）
    db_conn = db_conn or get_connect_from_config(db_config, database=database)
    db_cursor = db_conn.cursor()
    # 处理 SQL 语句
    sql_list = sql if isinstance(sql, (list, set)) else [sql]
    for s in sql_list:
        is_log and to_log_file(s)
        db_cursor.execute(str(s))
    if commit:
        db_conn.commit()


def get_doris_conn(db_config='doris'):
    return get_connect_from_config(db_config)


# 执行 sql 语句, 并且提交, 默认值提交的了
def exec_doris_sql(sql='', db_config='doris', database='mx_risk'):
    exec_sql(sql, db_config=db_config, database=database)


def get_data_from_doris(sql='', db_config='doris'):
    conn_doris = get_connect_from_config(db_config)
    cursor = conn_doris.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_data_line_one_from_doris(sql='', db_config='doris'):
    data_list = get_data_from_doris(sql, db_config=db_config)
    if len(data_list):
        return list(data_list[0])
    return None


# 执行 sql 语句, 不提交
def exec_sql_un_commit(sql='', db_conn=None, db_config='db', database=None):
    exec_sql(sql=sql, db_conn=db_conn, db_config=db_config, commit=False, database=database)


# 执行 sql 获得 数据
def get_data_from_sql(sql='', db_conn=None, db_config='db', is_log=False, database=None, save_to_thread=False):
    if not sql:
        is_log and to_log_file("db_conn is None or sql is None or sql == '', so return")
        return
    db_conn = db_conn or get_connect_from_config(db_config, database=database)
    db_cursor = db_conn.cursor()
    is_log and to_log_file(sql)
    db_cursor.execute(str(sql))
    return db_cursor.fetchall()


def extract_all_sql(log_content):
    """
    从字符串中提取所有 SQL 语句，并将 `?` 替换为参数，同时提取日志中的 total 信息。
    参数：
        log_content (str): 包含日志信息的字符串。
    返回：
        list: 包含 SQL 语句和总数的元组列表。
              每个元组的第一个元素是 SQL 语句，第二个元素是 total（如果存在）。
    示例：
           log_content = 如下， 返回 list([sql, total])
11:15:27.259 INFO o.s.c.n.e.c.DiscoveryClientOptionalArgsConfiguration : Eureka HTTP Client uses RestTemplate.
11:15:27.315 WARN o.s.c.l.c.LoadBalancerCacheAutoConfiguration$LoadBalancerCaffeineWarnLogger : Spring Cloud LoadBalancer is currently working with the default cache. While this cache implementation is useful for development and tests, it's recommended to use Caffeine cache in production.You can switch to using Caffeine cache, by adding it and org.springframework.cache.caffeine.CaffeineCacheManager to the classpath.
11:15:27.347 INFO o.s.b.a.e.w.EndpointLinksResolver : Exposing 1 endpoint beneath base path '/actuator'
11:15:27.471 INFO c.u.m.r.f.CheckReportCreatorTests : Started CheckReportCreatorTests in 11.792 seconds (process running for 13.368)
11:15:28.843 DEBUG c.u.m.r.f.m.A.findInfo : ==>  Preparing: select t.order_id, t.report_data as report_data_java, l.report_data from analyze_report_java t left join analyze_report_loan l on t.order_id = l.order_id and t.report_type = l.report_type where t.report_type = ? and t.create_time > ? and t.phase_code = 'LOAN' and l.report_data != t.report_data and t.id > 0 order by t.id desc
11:15:28.987 DEBUG c.u.m.r.f.m.A.findInfo : ==> Parameters: smsNewCommon.all(String), 2025-01-09 15:22:00(String)
11:15:33.884 DEBUG c.u.m.r.f.m.A.findInfo : <==      Total: 0
11:15:33.885 DEBUG c.u.m.r.f.m.A.findInfoCredit : ==>  Preparing: select t.order_id, t.report_data as report_data_java, l.report_data from analyze_report_java t left join analyze_report_credit l on t.order_id = l.order_id and t.report_type = l.report_type where t.report_type = ? and t.create_time > ? and t.phase_code = 'PRELOAN' and l.report_data != t.report_data and t.id > 0 order by t.id desc
11:15:33.886 DEBUG c.u.m.r.f.m.A.findInfoCredit : ==> Parameters: smsNewCommon.all(String), 2025-01-09 15:22:00(String)
11:15:36.782 DEBUG c.u.m.r.f.m.A.findInfoCredit : <==      Total: 0
11:15:37.493 INFO c.z.h.HikariDataSource : HikariPool-1 - Shutdown initiated...
11:15:38.426 INFO c.z.h.HikariDataSource : HikariPool-1 - Shutdown completed.
    """
    if len(log_content.split('\n')) == 2:
        log_content += '\n'
    # 匹配 SQL 语句和参数
    sql_pattern = r"Preparing: (.*?)\n.*?Parameters: (.*?)\n"
    # 匹配 total 记录
    total_pattern = r"Total:\s*(\d+)"
    # 查找所有 SQL 语句和参数
    matches = re.findall(sql_pattern, log_content, re.DOTALL)
    # 查找所有 Total 值
    totals = re.findall(total_pattern, log_content)

    sql_list = []
    total_index = 0  # 记录 total 匹配的位置

    for sql, parameters in matches:
        sql = sql.strip()
        # 解析参数
        params_list = [
            param.split("(")[0].strip() for param in parameters.split(", ")
        ]

        # 依次替换 `?` 为参数值
        for param in params_list:
            sql = sql.replace("?", f"'{param}'", 1)

        # 取对应的 total 值
        total = int(totals[total_index]) if total_index < len(totals) else None
        total_index += 1

        sql_list.append((sql, total))
    return sql_list


def format_sql(sql):
    return sqlparse.format(sql, reindent=True, keyword_case="upper")


def deal_sql(sql):
    sql = sql.replace('\n', ' ')
    sql = re.sub(r'\s+', ' ', sql).strip()
    return sql


def compress_sql(sql):
    return re.sub(r'\s+', ' ', str(sql).replace('\n', ' ').replace('\r', ' ')).strip()
