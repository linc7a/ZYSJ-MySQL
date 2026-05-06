"""
================================================================================
                    MySQL Python 操作完整教程
================================================================================

本文件是一个 MySQL 入门教程，通过 Python 代码详细演示 MySQL 的各种操作。
每个知识点都带有详细的中文注释，相当于一个完整的教程文档。

教程目录：
    1. 数据库连接
    2. DDL - 数据定义语言（创建数据库、表、约束、索引）
    3. DML - 数据操作语言（插入、更新、删除数据）
    4. DQL - 数据查询语言（各种查询语法）
    5. 聚合函数与分组
    6. 多表连接查询
    7. 子查询
    8. 视图操作
    9. 事务控制
    10. 存储过程
    11. 性能优化（EXPLAIN）

================================================================================
"""

# ================================================================================
# 第零章：导入必要的库
# ================================================================================

# -*- coding: utf-8 -*-
"""
================================================================================
                    MySQL Python 操作完整教程
================================================================================

本文件是一个 MySQL 入门教程，通过 Python 代码详细演示 MySQL 的各种操作。
每个知识点都带有详细的中文注释，相当于一个完整的教程文档。

教程目录：
    1. 数据库连接
    2. DDL - 数据定义语言（创建数据库、表、约束、索引）
    3. DML - 数据操作语言（插入、更新、删除数据）
    4. DQL - 数据查询语言（各种查询语法）
    5. 聚合函数与分组
    6. 多表连接查询
    7. 子查询
    8. 视图操作
    9. 事务控制
    10. 存储过程
    11. 性能优化（EXPLAIN）

================================================================================
"""

import sys
import io

# 设置 stdout 编码为 UTF-8，解决 Windows 控制台 emoji 显示问题
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

# 移除 emoji 字符的 print 函数
import builtins
_original_print = print

def _safe_print(*args, **kwargs):
    """安全的 print 函数，移除 emoji 字符"""
    cleaned_args = []
    for arg in args:
        if isinstance(arg, str):
            # 移除常见 emoji 字符
            emoji_chars = ['\U0001f393', '\U0001f4ca', '\U0001f50c', '\U0001f4dd', 
                          '\U0001f3e2', '\U0001f4c1', '\U0001f527', '\U0001f50d',
                          '\U0001f3c6', '\U0001f389', '\U0001f6a7', '\U0001f4a1',
                          '\U0001f4c4', '\U0001f4dd', '\U0001f4e7', '\U0001f4bb',
                          '\U0001f426', '\U0001f4d0', '\U0001f4f1', '\U0001f3af',
                          '\U0001f440', '\U0001f44d', '\U0001f44e', '\U0001f3a8',
                          '\U0001f3df', '\U0001f6b2', '\U0001f6a9', '\U0001f308']
            for emoji in emoji_chars:
                arg = arg.replace(emoji, '')
            arg = arg.strip()
        cleaned_args.append(arg)
    _original_print(*cleaned_args, **kwargs)

builtins.print = _safe_print

# ================================================================================
# 第零章：导入必要的库
# ================================================================================

import pymysql
from pymysql.cursors import DictCursor  # 用于将查询结果转为字典格式
from datetime import datetime, date
from typing import List, Dict, Any, Tuple


# ================================================================================
# 第一章：数据库连接配置
# ================================================================================

class MySQLConfig:
    """
    MySQL 数据库连接配置类
    
    为什么要用配置文件？
    - 集中管理连接参数，方便修改
    - 避免在代码中硬编码敏感信息
    - 便于在不同环境（开发、测试、生产）使用不同配置
    
    配置参数说明：
    - host: MySQL 服务器地址
        * localhost 表示本机（127.0.0.1）
        * 如果连接远程服务器，改为对应的 IP 地址
    - port: MySQL 服务端口
        * 默认是 3306，修改需在 docker-compose 中同步修改
    - user: 用户名
        * root 是 MySQL 的超级管理员账户
    - password: 密码
        * 这里使用 root123456，与 docker-compose.yml 中的一致
    - database: 默认连接的数据库名
        * 如果不存在，会在连接后创建
    - charset: 字符编码
        * utf8mb4 是 UTF-8 的完整实现，支持 emoji 等特殊字符
        * 旧版 utf8 只支持 3 字节，utf8mb4 支持 4 字节
    """
    
    # 数据库连接配置 - 根据你的实际情况修改
    HOST = 'localhost'           # MySQL 服务器地址（本地用 localhost）
    PORT = 3306                 # MySQL 端口（默认 3306）
    USER = 'root'               # 用户名
    PASSWORD = 'root123456'     # 密码（与 docker-compose.yml 中设置的一致）
    DATABASE = 'tutorial_db'    # 要操作的数据库名
    CHARSET = 'utf8mb4'         # 字符编码（推荐使用 utf8mb4）


class DatabaseConnection:
    """
    数据库连接管理类
    
    封装了数据库的连接、游标获取、关闭等操作，
    使用上下文管理器（with 语句）可以自动管理资源。
    """
    
    def __init__(self, config: MySQLConfig = None):
        """
        初始化数据库连接
        
        参数:
            config: MySQLConfig 配置对象，如果为 None 则使用默认配置
        """
        self.config = config or MySQLConfig()
        self.connection = None
        self.cursor = None
    
    def connect(self) -> 'DatabaseConnection':
        """
        建立数据库连接
        
        pymysql.connect() 参数说明：
        - host: 服务器地址
        - port: 端口号（必须是整数）
        - user: 用户名
        - password: 密码
        - database: 默认数据库
        - charset: 字符编码
        
        返回:
            self - 方便链式调用
        """
        try:
            # 建立数据库连接
            self.connection = pymysql.connect(
                host=self.config.HOST,
                port=self.config.PORT,
                user=self.config.USER,
                password=self.config.PASSWORD,
                database=self.config.DATABASE,
                charset=self.config.CHARSET,
                # cursorclass=DictCursor 表示查询结果返回字典格式
                # 默认为元组格式，字典格式更容易理解和使用
                cursorclass=DictCursor
            )
            # 创建游标对象
            # 游标（Cursor）用于执行 SQL 语句和获取结果
            # 就像鼠标指针一样，在数据表上移动并操作数据
            self.cursor = self.connection.cursor()
            print("✅ 数据库连接成功！")
            return self
        except pymysql.Error as e:
            print(f"❌ 数据库连接失败：{e}")
            raise
    
    def close(self):
        """
        关闭数据库连接和游标
        
        为什么要关闭？
        - 释放数据库连接资源
        - 避免连接泄漏导致数据库负载过高
        - 在生产环境中尤为重要
        """
        if self.cursor:
            self.cursor.close()
            print("✅ 游标已关闭")
        if self.connection:
            self.connection.close()
            print("✅ 数据库连接已关闭")
    
    def __enter__(self):
        """上下文管理器入口 - with 语句开始时执行"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口 - with 语句结束时执行"""
        self.close()
        # 返回 False 表示不吞掉异常，让异常继续传播
        return False


# ================================================================================
# 第二章：DDL - 数据定义语言（Database Definition Language）
# ================================================================================

class DDLOperations:
    """
    DDL 操作类 - 负责创建和管理数据库结构
    
    DDL 包括：
    - CREATE: 创建数据库、表、索引等
    - ALTER: 修改表结构
    - DROP: 删除数据库、表等
    - TRUNCATE: 清空表数据（不可恢复）
    """
    
    @staticmethod
    def create_database(db: DatabaseConnection):
        """
        创建数据库
        
        SQL 语法：
        CREATE DATABASE [IF NOT EXISTS] database_name
        [DEFAULT CHARACTER SET charset_name]
        [DEFAULT COLLATE collation_name];
        
        参数说明：
        - IF NOT EXISTS: 如果数据库已存在，不报错（防止重复创建）
        - DEFAULT CHARACTER SET: 设置默认字符集，utf8mb4 是 MySQL 推荐的全 UTF-8 编码
        - DEFAULT COLLATE: 设置排序规则，utf8mb4_unicode_ci 是通用的 Unicode 排序
        """
        sql = """
        -- 创建数据库（如果不存在）
        -- tutorial_db: 数据库名称
        -- DEFAULT CHARSET utf8mb4: 默认字符集为 utf8mb4（支持 emoji 等特殊字符）
        -- COLLATE utf8mb4_unicode_ci: 排序规则，ci 表示不区分大小写（case insensitive）
        CREATE DATABASE IF NOT EXISTS tutorial_db 
        DEFAULT CHARSET utf8mb4 
        COLLATE utf84_unicode_ci;
        """
        
        # 先尝试创建数据库（不指定 database 参数）
        temp_conn = pymysql.connect(
            host=MySQLConfig.HOST,
            port=MySQLConfig.PORT,
            user=MySQLConfig.USER,
            password=MySQLConfig.PASSWORD,
            charset=MySQLConfig.CHARSET
        )
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("CREATE DATABASE IF NOT EXISTS tutorial_db DEFAULT CHARSET utf8mb4")
        temp_cursor.close()
        temp_conn.close()
        print("✅ 数据库已创建/检查")
    
    @staticmethod
    def create_tables(db: DatabaseConnection):
        """
        创建数据表
        
        SQL 语法：
        CREATE TABLE table_name (
            column_name datatype [constraints],
            ...
        ) ENGINE=InnoDB CHARSET=utf8mb4;
        
        MySQL 常用数据类型：
        - 数值类型：
          * TINYINT: 1 字节，-128~127（或 0~255 无符号）
          * SMALLINT: 2 字节，-32768~32767
          * INT/INTEGER: 4 字节，约 ±21 亿
          * BIGINT: 8 字节，超大整数
          * DECIMAL(p, s): 精确数值，p=总位数，s=小数位数
          * FLOAT/DOUBLE: 浮点数（不精确）
        
        - 字符串类型：
          * CHAR(n): 固定长度字符串（0-255）
          * VARCHAR(n): 可变长度字符串（0-65535）
          * TEXT: 长文本（最大 65535 字节）
          * LONGTEXT: 超长文本（最大 4GB）
        
        - 日期时间类型：
          * DATE: 日期（YYYY-MM-DD）
          * TIME: 时间（HH:MM:SS）
          * DATETIME: 日期时间（YYYY-MM-DD HH:MM:SS）
          * TIMESTAMP: 时间戳（自动设置为当前时间）
          * YEAR: 年份
        
        约束（Constraints）：
        - PRIMARY KEY: 主键，唯一标识每行数据
        - AUTO_INCREMENT: 自增，用于生成唯一 ID
        - NOT NULL: 非空约束
        - UNIQUE: 唯一约束（值不能重复）
        - DEFAULT value: 默认值
        - CHECK condition: 检查约束（MySQL 8.0.16+）
        - FOREIGN KEY: 外键，关联其他表
        """
        
        # -------------------- 表1：用户表 --------------------
        """
        users 表结构说明：
        - id: 主键，自增
        - username: 用户名，唯一且非空
        - email: 邮箱，唯一且非空
        - password_hash: 密码哈希，存储加密后的密码
        - age: 年龄，有范围检查（18-100）
        - status: 账户状态，默认 'active'
        - created_at: 创建时间，默认为当前时间戳
        - updated_at: 更新时间，默认为当前时间戳
        """
        create_users_sql = """
        CREATE TABLE IF NOT EXISTS users (
            -- id: 主键字段
            -- INT: 整数类型
            -- PRIMARY KEY: 设为主键（唯一标识每行记录）
            -- AUTO_INCREMENT: 自增，每次插入自动加 1
            id INT PRIMARY KEY AUTO_INCREMENT,
            
            -- username: 用户名
            -- VARCHAR(50): 可变字符串，最大 50 个字符
            -- NOT NULL: 必填字段，不能为空
            -- UNIQUE: 唯一约束，该字段值不能重复
            username VARCHAR(50) NOT NULL UNIQUE,
            
            -- email: 邮箱
            -- VARCHAR(100): 最大 100 个字符
            -- NOT NULL + UNIQUE: 非空且唯一
            email VARCHAR(100) NOT NULL UNIQUE,
            
            -- password_hash: 密码哈希
            -- VARCHAR(255): 存储加密后的密码哈希值
            password_hash VARCHAR(255) NOT NULL,
            
            -- age: 年龄
            -- TINYINT: 微小整数，-128~127
            -- CHECK(age >= 18 AND age <= 100): 检查约束，限制年龄范围
            -- （MySQL 8.0.16+ 支持）
            age TINYINT CHECK (age >= 18 AND age <= 100),
            
            -- status: 账户状态
            -- ENUM('active', 'inactive', 'banned'): 枚举类型，只能是这三个值之一
            -- DEFAULT 'active': 默认值为 'active'
            status ENUM('active', 'inactive', 'banned') DEFAULT 'active',
            
            -- created_at: 创建时间
            -- DATETIME: 日期时间类型
            -- DEFAULT CURRENT_TIMESTAMP: 默认为当前时间戳
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            -- updated_at: 更新时间
            -- DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP:
            -- 插入时默认为当前时间，更新时自动更新为最新时间
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            -- 为 username 字段创建索引（加速查询）
            INDEX idx_username (username)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        # -------------------- 表2：文章表 --------------------
        """
        articles 表结构说明：
        - id: 主键，自增
        - user_id: 发布者 ID，外键关联 users 表
        - title: 文章标题
        - content: 文章内容（长文本）
        - views: 阅读次数，默认 0
        - is_published: 是否发布，默认 False
        - published_at: 发布时间
        - created_at/updated_at: 创建和更新时间
        """
        create_articles_sql = """
        CREATE TABLE IF NOT EXISTS articles (
            -- id: 主键，自增
            id INT PRIMARY KEY AUTO_INCREMENT,
            
            -- user_id: 发布者 ID
            -- INT: 整数类型
            -- NOT NULL: 非空
            -- FOREIGN KEY (user_id) REFERENCES users(id): 
            --   外键约束，关联 users 表的 id 字段
            --   确保 user_id 必须是 users 表中存在的 ID
            -- ON DELETE CASCADE: 级联删除，当 users 表中的记录被删除时，
            --   同时删除该用户发布的所有文章
            user_id INT NOT NULL,
            
            -- title: 文章标题
            -- VARCHAR(200): 最大 200 字符
            -- NOT NULL: 非空
            title VARCHAR(200) NOT NULL,
            
            -- content: 文章内容
            -- TEXT: 长文本类型，最大 65535 字节
            -- 可以存储较大的文章内容
            content TEXT,
            
            -- views: 阅读次数
            -- INT DEFAULT 0: 默认为 0
            views INT DEFAULT 0,
            
            -- is_published: 是否发布
            -- BOOLEAN/TINYINT(1): 布尔类型（0 或 1）
            -- DEFAULT 0: 默认未发布
            is_published TINYINT(1) DEFAULT 0,
            
            -- published_at: 发布时间
            -- DATETIME: 日期时间类型
            -- 可以为空（NULL），表示未发布
            published_at DATETIME,
            
            -- created_at/updated_at: 时间戳
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            -- FOREIGN KEY: 定义外键约束
            -- 语法: FOREIGN KEY (本表字段) REFERENCES 其他表(字段)
            -- 含义: user_id 的值必须在 users 表的 id 字段中存在
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            
            -- INDEX: 创建索引
            -- 索引用于加速查询，就像书的目录一样
            INDEX idx_user_id (user_id),
            INDEX idx_published (is_published, published_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        # -------------------- 表3：评论表 --------------------
        """
        comments 表结构说明：
        - id: 主键
        - article_id: 文章 ID，外键
        - user_id: 评论者 ID，外键
        - parent_id: 父评论 ID（用于回复功能，实现评论嵌套）
        - content: 评论内容
        - created_at: 评论时间
        """
        create_comments_sql = """
        CREATE TABLE IF NOT EXISTS comments (
            -- id: 主键
            id INT PRIMARY KEY AUTO_INCREMENT,
            
            -- article_id: 文章 ID，外键关联 articles 表
            article_id INT NOT NULL,
            
            -- user_id: 评论者 ID，外键关联 users 表
            user_id INT NOT NULL,
            
            -- parent_id: 父评论 ID
            -- 用于实现评论的回复功能（自关联）
            -- 可以为空（NULL），表示顶级评论
            parent_id INT,
            
            -- content: 评论内容
            -- VARCHAR(1000): 最大 1000 字符
            content VARCHAR(1000) NOT NULL,
            
            -- created_at: 评论时间
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            -- 外键约束
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            -- 自关联外键（允许为 NULL）
            FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE,
            
            -- 索引
            INDEX idx_article_id (article_id),
            INDEX idx_user_id (user_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        # 先删除旧表（确保表结构正确）
        db.cursor.execute("DROP TABLE IF EXISTS comments")
        db.cursor.execute("DROP TABLE IF EXISTS articles")
        db.cursor.execute("DROP TABLE IF EXISTS users")
        
        # 执行创建表 SQL
        db.cursor.execute(create_users_sql)
        print("✅ users 表已创建")
        
        db.cursor.execute(create_articles_sql)
        print("✅ articles 表已创建")
        
        db.cursor.execute(create_comments_sql)
        print("✅ comments 表已创建")
    
    @staticmethod
    def show_tables(db: DatabaseConnection):
        """
        查看数据库中的所有表
        
        SQL 语法：
        SHOW TABLES;
        - 显示当前数据库中的所有表
        - 返回表名列表
        """
        sql = "SHOW TABLES;"
        db.cursor.execute(sql)
        
        # fetchall() 获取所有查询结果
        # 返回格式: [(table_name1,), (table_name2,), ...]
        tables = db.cursor.fetchall()
        
        print("\n📋 数据库中的表：")
        for table in tables:
            # table 是一个字典（因为设置了 cursorclass=DictCursor）
            # 或者元组，取决于游标类型
            table_name = list(table.values())[0] if isinstance(table, dict) else table[0]
            print(f"   - {table_name}")
    
    @staticmethod
    def describe_table(db: DatabaseConnection, table_name: str):
        """
        查看表结构（字段信息）
        
        SQL 语法：
        DESCRIBE table_name;
        或
        DESC table_name;
        
        返回字段的详细信息：
        - Field: 字段名
        - Type: 数据类型
        - Null: 是否允许 NULL
        - Key: 主键/唯一键信息（PRI=主键, UNI=唯一, MUL=索引）
        - Default: 默认值
        - Extra: 额外信息（如 auto_increment）
        """
        sql = f"DESCRIBE {table_name};"
        db.cursor.execute(sql)
        
        print(f"\n📊 {table_name} 表结构：")
        print("-" * 80)
        print(f"{'字段名':<20} {'类型':<25} {'Null':<10} {'Key':<10} {'默认值':<15}")
        print("-" * 80)
        
        for row in db.cursor.fetchall():
            # row 是字典格式
            print(f"{row['Field']:<20} {row['Type']:<25} {row['Null']:<10} {row['Key']:<10} {row['Default']}")
    
    @staticmethod
    def alter_table(db: DatabaseConnection):
        """
        修改表结构
        
        ALTER TABLE 语法：
        - ALTER TABLE table_name ADD column...
        - ALTER TABLE table_name MODIFY column...
        - ALTER TABLE table_name DROP column...
        - ALTER TABLE table_name RENAME TO...
        """
        
        # 示例 1：添加新字段
        """
        ALTER TABLE table_name ADD new_column datatype [constraints] [AFTER existing_column];
        
        场景：为 users 表添加手机号字段
        """
        sql_add = """
        ALTER TABLE users 
        ADD COLUMN phone VARCHAR(20) AFTER email;
        """
        
        # 检查字段是否存在（MySQL 8.0+ 可用）
        db.cursor.execute("""
            SELECT COUNT(*) as cnt 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = 'tutorial_db' 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'phone'
        """)
        if db.cursor.fetchone()['cnt'] == 0:
            try:
                db.cursor.execute(sql_add)
                print("✅ 已添加 phone 字段到 users 表")
            except Exception as e:
                print(f"⚠️ 添加字段失败（可能已存在）: {e}")
        
        # 示例 2：修改字段类型
        """
        ALTER TABLE table_name MODIFY column_name new_datatype [constraints];
        
        场景：修改 phone 字段长度
        """
        sql_modify = "ALTER TABLE users MODIFY COLUMN phone VARCHAR(30);"
        
        # 示例 3：删除字段
        """
        ALTER TABLE table_name DROP COLUMN column_name;
        
        ⚠️ 注意：删除字段会丢失该字段的所有数据，请谨慎操作！
        """
        # sql_drop = "ALTER TABLE users DROP COLUMN phone;"
    
    @staticmethod
    def drop_table(db: DatabaseConnection, table_name: str):
        """
        删除表
        
        SQL 语法：
        DROP TABLE [IF EXISTS] table_name;
        
        ⚠️ 危险操作：
        - DROP TABLE 会永久删除表及其所有数据
        - 无法恢复，请务必谨慎！
        - 建议先备份数据，或者使用 TRUNCATE（可保留结构）
        
        IF EXISTS: 如果表不存在，不报错（防止重复删除）
        """
        sql = f"DROP TABLE IF EXISTS {table_name};"
        try:
            db.cursor.execute(sql)
            print(f"✅ 表 {table_name} 已删除")
        except Exception as e:
            print(f"❌ 删除失败: {e}")


# ================================================================================
# 第三章：DML - 数据操作语言（Data Manipulation Language）
# ================================================================================

class DMLOperations:
    """
    DML 操作类 - 负责数据的增删改
    
    DML 包括：
    - INSERT: 插入数据
    - UPDATE: 更新数据
    - DELETE: 删除数据
    """
    
    @staticmethod
    def insert_single_record(db: DatabaseConnection):
        """
        插入单条记录
        
        SQL 语法：
        INSERT INTO table_name (column1, column2, ...)
        VALUES (value1, value2, ...);
        
        注意事项：
        - 列名和值要一一对应
        - 字符串和日期需要用单引号括起来
        - 自增字段可以传 NULL 或不传，会自动生成
        - 可以不指定列名，但需要按表结构顺序传入所有值
        """
        
        sql = """
        INSERT INTO users (username, email, password_hash, age, status)
        VALUES (%s, %s, %s, %s, %s);
        """
        
        # 准备数据
        user_data = (
            'zhangsan',                    # username
            'zhangsan@example.com',        # email
            'hashed_password_123',         # password_hash
            25,                            # age
            'active'                       # status
        )
        
        # execute() 执行单条 SQL
        # 返回受影响的行数
        db.cursor.execute(sql, user_data)
        
        # commit() 提交事务，将数据真正写入数据库
        # 如果是自动提交模式（默认），可以省略
        db.connection.commit()
        
        # 获取刚插入记录的 ID（自增主键）
        inserted_id = db.cursor.lastrowid
        print(f"✅ 插入单条记录成功，ID: {inserted_id}")
        
        return inserted_id
    
    @staticmethod
    def insert_multiple_records(db: DatabaseConnection):
        """
        批量插入多条记录
        
        SQL 语法：
        INSERT INTO table_name (column1, column2, ...)
        VALUES 
            (value1, value2, ...),
            (value3, value4, ...),
            (value5, value6, ...);
        
        executemany() 优点：
        - 一次数据库往返插入多条记录，效率高
        - 比循环调用 execute() 快很多
        - 适合大量数据导入
        """
        
        sql = """
        INSERT INTO users (username, email, password_hash, age, status)
        VALUES (%s, %s, %s, %s, %s);
        """
        
        # 批量准备数据 - 列表格式
        users_data = [
            ('lisi', 'lisi@example.com', 'hash_456', 28, 'active'),
            ('wangwu', 'wangwu@example.com', 'hash_789', 22, 'active'),
            ('zhaoliu', 'zhaoliu@example.com', 'hash_101', 35, 'inactive'),
            ('sunqi', 'sunqi@example.com', 'hash_202', 30, 'active'),
            ('zhouba', 'zhouba@example.com', 'hash_303', 26, 'active'),
        ]
        
        # executemany() 批量执行
        # 第一个参数是 SQL，第二个是数据列表
        db.cursor.executemany(sql, users_data)
        db.connection.commit()
        
        # rowcount 返回受影响的行数
        inserted_count = db.cursor.rowcount
        print(f"✅ 批量插入 {inserted_count} 条记录成功")
    
    @staticmethod
    def insert_articles(db: DatabaseConnection):
        """
        插入文章数据（带外键）
        
        注意：由于有外键约束，user_id 必须是 users 表中存在的 ID
        """
        
        sql = """
        INSERT INTO articles (user_id, title, content, views, is_published, published_at)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        
        articles_data = [
            (1, 'Python 入门教程', 
             '这是一篇 Python 入门教程...', 
             100, 1, datetime.now()),
            (1, 'MySQL 基础指南',
             'MySQL 是最流行的开源数据库...',
             50, 1, datetime.now()),
            (2, 'JavaScript 进阶',
             '本文介绍 JavaScript 的高级特性...',
             200, 1, datetime.now()),
            (3, 'Docker 容器化',
             'Docker 让应用部署更简单...',
             0, 0, None),  # 未发布
        ]
        
        db.cursor.executemany(sql, articles_data)
        db.connection.commit()
        print(f"✅ 插入 {len(articles_data)} 篇文章")
    
    @staticmethod
    def update_records(db: DatabaseConnection):
        """
        更新数据
        
        SQL 语法：
        UPDATE table_name
        SET column1 = value1, column2 = value2
        [WHERE condition];
        
        ⚠️ 重要提示：
        - UPDATE 语句必须带 WHERE 条件！
        - 否则会更新表中所有记录
        - 建议先 SELECT 确认要更新的记录
        
        WHERE 条件常用操作符：
        - =: 等于
        - <> 或 !=: 不等于
        - >, <, >=, <=: 大于、小于
        - AND: 逻辑与
        - OR: 逻辑或
        - IN (values): 在列表中
        - BETWEEN value1 AND value2: 在范围内
        - LIKE 'pattern': 模糊匹配
        - IS NULL / IS NOT NULL: 空值判断
        """
        
        # 示例 1：更新单条记录
        """
        场景：修改用户名为 'zhangsan' 的用户年龄
        """
        sql1 = """
        UPDATE users 
        SET age = %s, status = %s 
        WHERE username = %s;
        """
        db.cursor.execute(sql1, (26, 'active', 'zhangsan'))
        
        # rowcount 返回受影响的行数
        if db.cursor.rowcount > 0:
            print(f"✅ 更新了 {db.cursor.rowcount} 条记录")
        else:
            print("⚠️ 没有找到匹配的记录")
        
        # 示例 2：批量更新
        """
        场景：将所有年龄小于 25 岁的用户状态设为 'inactive'
        """
        sql2 = "UPDATE users SET status = 'inactive' WHERE age < 25;"
        db.cursor.execute(sql2)
        print(f"✅ 批量更新了 {db.cursor.rowcount} 条记录")
        
        db.connection.commit()
    
    @staticmethod
    def delete_records(db: DatabaseConnection):
        """
        删除数据
        
        SQL 语法：
        DELETE FROM table_name
        [WHERE condition];
        
        ⚠️ 危险提示：
        - DELETE 必须带 WHERE 条件！
        - 否则会删除表中所有数据（但不会删除表结构）
        - 删除的数据可以恢复（如果有备份或事务未提交）
        - 如果要清空表数据但保留结构，用 TRUNCATE 更快
        
        与 DROP TABLE 的区别：
        - DELETE: 删除数据，保留表结构
        - TRUNCATE: 清空数据，保留表结构，效率更高
        - DROP: 删除整个表（包括结构和数据）
        """
        
        # 示例 1：删除指定记录
        """
        场景：删除用户名包含 'test' 的用户
        """
        sql1 = "DELETE FROM users WHERE username LIKE %s;"
        db.cursor.execute(sql1, ('%test%',))
        
        if db.cursor.rowcount > 0:
            print(f"✅ 删除了 {db.cursor.rowcount} 条记录")
        
        # 示例 2：使用子查询删除
        """
        场景：删除没有任何文章的用户
        """
        sql2 = """
        DELETE FROM users 
        WHERE id NOT IN (
            SELECT DISTINCT user_id FROM articles WHERE user_id IS NOT NULL
        );
        """
        # 注意：MySQL 不允许在子查询中直接操作同一张表
        # 需要使用临时表或嵌套查询
        # 这里简单示例，实际可能需要分步操作
        
        db.connection.commit()
    
    @staticmethod
    def truncate_table(db: DatabaseConnection):
        """
        清空表数据
        
        SQL 语法：
        TRUNCATE [TABLE] table_name;
        
        与 DELETE 的区别：
        - TRUNCATE: 快速清空，删除并重建表，自增计数器重置
        - DELETE: 逐行删除，可以带 WHERE 条件，速度较慢
        
        ⚠️ 注意：
        - TRUNCATE 无法回滚！
        - 除非在事务中并且事务未提交
        """
        # 示例：清空 comments 表（如果有的话）
        # db.cursor.execute("TRUNCATE TABLE comments;")
        # print("✅ 表已清空")
        pass


# ================================================================================
# 第四章：DQL - 数据查询语言（Data Query Language）
# ================================================================================

class DQLOperations:
    """
    DQL 操作类 - 负责查询数据
    
    DQL 核心是 SELECT 语句，是 SQL 中最复杂、功能最强大的部分。
    
    SELECT 语法顺序：
    SELECT [DISTINCT] columns, expressions, aggregates...
    FROM table_name
    [WHERE conditions]
    [GROUP BY columns]
    [HAVING group_conditions]
    [ORDER BY columns [ASC|DESC]]
    [LIMIT number [OFFSET number]];
    
    执行顺序（MySQL 实际执行顺序）：
    1. FROM - 确定数据来源
    2. WHERE - 筛选行
    3. GROUP BY - 分组
    4. HAVING - 筛选分组
    5. SELECT - 选择列
    6. ORDER BY - 排序
    7. LIMIT - 限制数量
    """
    
    @staticmethod
    def basic_select(db: DatabaseConnection):
        """
        基础查询
        
        SELECT 基础语法：
        SELECT column1, column2, ... FROM table_name;
        SELECT * FROM table_name;  -- 查询所有列
        """
        
        print("\n" + "="*60)
        print("📖 基础查询示例")
        print("="*60)
        
        # -------------------- 示例 1：查询所有用户 --------------------
        """
        SELECT *: 星号表示查询所有列
        FROM users: 从 users 表查询
        
        结果：返回 users 表的所有记录和所有字段
        """
        sql = "SELECT * FROM users;"
        db.cursor.execute(sql)
        
        # fetchone() 取一条记录
        # fetchall() 取所有记录
        # fetchmany(n) 取 n 条记录
        users = db.cursor.fetchall()
        
        print("\n📋 所有用户：")
        for user in users:
            print(f"   ID: {user['id']}, 用户名: {user['username']}, "
                  f"邮箱: {user['email']}, 年龄: {user['age']}, 状态: {user['status']}")
        
        # -------------------- 示例 2：查询指定列 --------------------
        """
        只查询 username 和 email 字段
        """
        sql2 = "SELECT username, email FROM users;"
        db.cursor.execute(sql2)
        
        print("\n📋 用户名和邮箱：")
        for user in db.cursor.fetchall():
            print(f"   {user['username']} -> {user['email']}")
        
        # -------------------- 示例 3：WHERE 条件筛选 --------------------
        """
        WHERE 子句：筛选满足条件的记录
        
        常用比较运算符：
        - =: 等于
        - <> 或 !=: 不等于
        - >: 大于
        - <: 小于
        - >=: 大于等于
        - <=: 小于等于
        
        逻辑运算符：
        - AND: 所有条件都满足
        - OR: 任意一个条件满足
        - NOT: 取反
        """
        sql3 = "SELECT * FROM users WHERE age >= 25 AND status = 'active';"
        db.cursor.execute(sql3)
        
        print("\n📋 年龄 >= 25 且状态为 active 的用户：")
        for user in db.cursor.fetchall():
            print(f"   {user['username']}, {user['age']}岁")
        
        # -------------------- 示例 4：LIKE 模糊查询 --------------------
        """
        LIKE: 模糊匹配
        - %: 匹配任意多个字符
        - _: 匹配单个字符
        
        'zhang%': 以 zhang 开头
        '%@example.com': 以 @example.com 结尾
        '%test%': 包含 test
        """
        sql4 = "SELECT * FROM users WHERE email LIKE %s;"
        db.cursor.execute(sql4, ('%@example.com',))
        
        print("\n📋 使用 @example.com 邮箱的用户：")
        for user in db.cursor.fetchall():
            print(f"   {user['username']} -> {user['email']}")
        
        # -------------------- 示例 5：IN 操作符 --------------------
        """
        IN: 在指定的值列表中
        相当于多个 OR 条件
        """
        sql5 = "SELECT * FROM users WHERE status IN ('active', 'inactive');"
        db.cursor.execute(sql5)
        
        print("\n📋 状态为 active 或 inactive 的用户：")
        print(f"   共找到 {db.cursor.rowcount} 条记录")
        
        # -------------------- 示例 6：BETWEEN 范围查询 --------------------
        """
        BETWEEN ... AND ...: 在范围内（包含边界）
        """
        sql6 = "SELECT * FROM users WHERE age BETWEEN 20 AND 30;"
        db.cursor.execute(sql6)
        
        print("\n📋 年龄在 20-30 岁之间的用户：")
        for user in db.cursor.fetchall():
            print(f"   {user['username']}, {user['age']}岁")
        
        # -------------------- 示例 7：ORDER BY 排序 --------------------
        """
        ORDER BY: 排序
        - ASC: 升序（从小到大，默认）
        - DESC: 降序（从大到小）
        
        可以按多个字段排序
        """
        sql7 = "SELECT * FROM users ORDER BY age DESC, created_at ASC;"
        db.cursor.execute(sql7)
        
        print("\n📋 按年龄降序、创建时间升序排列：")
        for user in db.cursor.fetchall():
            print(f"   {user['username']}, {user['age']}岁, 创建于 {user['created_at']}")
        
        # -------------------- 示例 8：LIMIT 分页 --------------------
        """
        LIMIT: 限制返回记录数
        - LIMIT n: 返回前 n 条
        - LIMIT offset, count: 从 offset 开始，取 count 条
        - LIMIT count OFFSET offset: 同上，语法更清晰
        
        分页查询公式：
        - 第 1 页：LIMIT 0, 10 或 LIMIT 10 OFFSET 0
        - 第 2 页：LIMIT 10, 10 或 LIMIT 10 OFFSET 10
        - 第 n 页：LIMIT 10 OFFSET (n-1)*10
        """
        sql8 = "SELECT * FROM users ORDER BY id LIMIT 3 OFFSET 0;"
        db.cursor.execute(sql8)
        
        print("\n📋 前 3 条用户（分页示例）：")
        for user in db.cursor.fetchall():
            print(f"   {user['id']}. {user['username']}")
        
        # -------------------- 示例 9：DISTINCT 去重 --------------------
        """
        DISTINCT: 去除重复记录
        
        注意：DISTINCT 作用于 SELECT 的所有列
        SELECT DISTINCT col1, col2 表示 (col1, col2) 组合去重
        """
        sql9 = "SELECT DISTINCT status FROM users;"
        db.cursor.execute(sql9)
        
        print("\n📋 用户状态（去重）：")
        for row in db.cursor.fetchall():
            print(f"   {row['status']}")
    
    @staticmethod
    def aggregate_functions(db: DatabaseConnection):
        """
        聚合函数
        
        聚合函数对一组值进行计算，返回单个结果。
        常用聚合函数：
        - COUNT(*): 统计记录数
        - COUNT(column): 统计非 NULL 值数量
        - COUNT(DISTINCT column): 统计去重后的数量
        - SUM(column): 求和
        - AVG(column): 平均值
        - MAX(column): 最大值
        - MIN(column): 最小值
        
        特点：
        - 聚合函数通常与 GROUP BY 一起使用
        - 单独使用时，是对整个结果集聚合
        """
        
        print("\n" + "="*60)
        print("📊 聚合函数示例")
        print("="*60)
        
        # -------------------- 示例 1：COUNT 统计数量 --------------------
        """
        COUNT(*): 统计所有记录数（包含 NULL）
        COUNT(column): 统计指定列非 NULL 的记录数
        """
        sql = "SELECT COUNT(*) as total_users FROM users;"
        db.cursor.execute(sql)
        result = db.cursor.fetchone()
        print(f"\n📋 用户总数：{result['total_users']}")
        
        # -------------------- 示例 2：SUM/AVG 数值统计 --------------------
        sql2 = "SELECT SUM(views) as total_views, AVG(views) as avg_views FROM articles;"
        db.cursor.execute(sql2)
        result = db.cursor.fetchone()
        print(f"\n📋 文章总阅读：{result['total_views']}, 平均阅读：{result['avg_views']:.1f}")
        
        # -------------------- 示例 3：MAX/MIN --------------------
        sql3 = "SELECT MAX(age) as max_age, MIN(age) as min_age FROM users;"
        db.cursor.execute(sql3)
        result = db.cursor.fetchone()
        print(f"\n📋 用户年龄范围：{result['min_age']} - {result['max_age']} 岁")
        
        # -------------------- 示例 4：COUNT + DISTINCT --------------------
        sql4 = "SELECT COUNT(DISTINCT status) as status_count FROM users;"
        db.cursor.execute(sql4)
        result = db.cursor.fetchone()
        print(f"\n📋 状态类型数：{result['status_count']}")
    
    @staticmethod
    def group_by(db: DatabaseConnection):
        """
        GROUP BY 分组查询
        
        GROUP BY 语法：
        SELECT column, aggregate_function(column)
        FROM table_name
        GROUP BY column
        [HAVING condition];
        
        执行过程：
        1. 根据 GROUP BY 的列分组
        2. 对每个分组应用聚合函数
        3. 返回每个分组的聚合结果
        
        HAVING vs WHERE：
        - WHERE: 在分组前筛选行
        - HAVING: 在分组后筛选分组
        - WHERE 不能使用聚合函数，HAVING 可以
        """
        
        print("\n" + "="*60)
        print("📊 分组查询示例")
        print("="*60)
        
        # -------------------- 示例 1：简单分组 --------------------
        """
        按状态分组统计用户数
        """
        sql1 = """
        SELECT status, COUNT(*) as user_count 
        FROM users 
        GROUP BY status;
        """
        db.cursor.execute(sql1)
        
        print("\n📋 按状态分组统计用户数：")
        for row in db.cursor.fetchall():
            print(f"   状态: {row['status']}, 人数: {row['user_count']}")
        
        # -------------------- 示例 2：多字段分组 --------------------
        """
        按状态和年龄分组
        """
        sql2 = """
        SELECT status, age, COUNT(*) as count 
        FROM users 
        GROUP BY status, age
        ORDER BY status, age;
        """
        db.cursor.execute(sql2)
        
        print("\n📋 按状态和年龄分组：")
        for row in db.cursor.fetchall():
            print(f"   状态: {row['status']}, 年龄: {row['age']}, 人数: {row['count']}")
        
        # -------------------- 示例 3：HAVING 筛选分组 --------------------
        """
        HAVING: 对分组后的结果进行筛选
        找出用户数 >= 2 的状态
        """
        sql3 = """
        SELECT status, COUNT(*) as user_count 
        FROM users 
        GROUP BY status 
        HAVING user_count >= 2;
        """
        db.cursor.execute(sql3)
        
        print("\n📋 用户数 >= 2 的状态：")
        for row in db.cursor.fetchall():
            print(f"   状态: {row['status']}, 人数: {row['user_count']}")
        
        # -------------------- 示例 4：带 WHERE + GROUP BY + HAVING --------------------
        """
        完整流程：
        1. WHERE 筛选年龄 > 20 的记录
        2. 按状态分组
        3. HAVING 筛选用户数 > 1 的分组
        4. 按用户数降序排序
        """
        sql4 = """
        SELECT status, COUNT(*) as user_count, AVG(age) as avg_age
        FROM users 
        WHERE age > 20
        GROUP BY status 
        HAVING user_count > 1
        ORDER BY user_count DESC;
        """
        db.cursor.execute(sql4)
        
        print("\n📋 年龄 > 20 的用户，按状态分组（筛选后）：")
        for row in db.cursor.fetchall():
            print(f"   状态: {row['status']}, 人数: {row['user_count']}, 平均年龄: {row['avg_age']:.1f}")
    
    @staticmethod
    def join_queries(db: DatabaseConnection):
        """
        多表连接查询
        
        连接（JOIN）用于合并多个表的数据。
        
        连接类型：
        1. INNER JOIN (内连接)
           - 只返回两个表中匹配的行
           - A INNER JOIN B: 只返回 A 和 B 都有的记录
        
        2. LEFT JOIN (左外连接)
           - 返回左表所有记录，右表没有的显示 NULL
           - A LEFT JOIN B: 返回 A 的所有记录
        
        3. RIGHT JOIN (右外连接)
           - 返回右表所有记录，左表没有的显示 NULL
           - A RIGHT JOIN B: 返回 B 的所有记录
        
        4. FULL OUTER JOIN (全外连接)
           - 返回两个表的所有记录，没有的显示 NULL
           - MySQL 不直接支持，可用 UNION 模拟
        
        连接语法：
        SELECT columns
        FROM table1
        [INNER|LEFT|RIGHT] JOIN table2
        ON table1.column = table2.column
        [WHERE conditions];
        """
        
        print("\n" + "="*60)
        print("🔗 多表连接查询示例")
        print("="*60)
        
        # -------------------- 示例 1：INNER JOIN --------------------
        """
        场景：查询所有文章及其作者信息
        
        INNER JOIN: 只返回有作者的文章
        即 articles.user_id 必须在 users.id 中存在
        """
        sql1 = """
        SELECT 
            a.title as article_title,
            a.views,
            u.username as author,
            u.email as author_email
        FROM articles a
        INNER JOIN users u ON a.user_id = u.id
        WHERE a.is_published = 1
        ORDER BY a.views DESC;
        """
        db.cursor.execute(sql1)
        
        print("\n📋 已发布文章及其作者（INNER JOIN）：")
        for row in db.cursor.fetchall():
            print(f"   《{row['article_title']}》- 作者: {row['author']}, 阅读: {row['views']}")
        
        # -------------------- 示例 2：LEFT JOIN --------------------
        """
        场景：查询所有用户及其发布的文章数（包括没有发布文章的用户）
        
        LEFT JOIN: 返回所有用户，没有文章的显示 NULL
        """
        sql2 = """
        SELECT 
            u.username,
            COUNT(a.id) as article_count
        FROM users u
        LEFT JOIN articles a ON u.id = a.user_id
        GROUP BY u.id, u.username
        ORDER BY article_count DESC;
        """
        db.cursor.execute(sql2)
        
        print("\n📋 所有用户及文章数（LEFT JOIN）：")
        for row in db.cursor.fetchall():
            print(f"   {row['username']}: {row['article_count']} 篇文章")
        
        # -------------------- 示例 3：多表连接 --------------------
        """
        场景：查询文章、作者、评论数
        需要连接：articles -> users -> comments
        """
        sql3 = """
        SELECT 
            a.title as article_title,
            u.username as author,
            COUNT(DISTINCT c.id) as comment_count
        FROM articles a
        INNER JOIN users u ON a.user_id = u.id
        LEFT JOIN comments c ON a.id = c.article_id
        WHERE a.is_published = 1
        GROUP BY a.id, a.title, u.username
        ORDER BY comment_count DESC;
        """
        db.cursor.execute(sql3)
        
        print("\n📋 文章、作者、评论数（多表连接）：")
        for row in db.cursor.fetchall():
            print(f"   《{row['article_title']}》- 作者: {row['author']}, 评论: {row['comment_count']}")
        
        # -------------------- 示例 4：自连接 --------------------
        """
        场景：查询评论及其父评论（回复）
        
        自连接：将表与自身连接
        需要给表起别名来区分
        """
        # 先插入一些评论数据
        db.cursor.execute("""
            INSERT INTO comments (article_id, user_id, parent_id, content) VALUES
            (1, 1, NULL, '写得很好！'),
            (1, 2, 1, '同意楼上观点'),
            (1, 3, 1, '补充一点...'),
            (2, 1, NULL, '期待更新');
        """)
        db.connection.commit()
        
        # 自连接查询
        sql4 = """
        SELECT 
            c1.content as comment,
            c2.content as reply_to
        FROM comments c1
        LEFT JOIN comments c2 ON c1.parent_id = c2.id
        WHERE c1.parent_id IS NOT NULL;
        """
        db.cursor.execute(sql4)
        
        print("\n📋 评论回复关系（自连接）：")
        for row in db.cursor.fetchall():
            print(f"   回复: {row['reply_to']}")
            print(f"      -> {row['comment']}")
    
    @staticmethod
    def subqueries(db: DatabaseConnection):
        """
        子查询
        
        子查询：在一个 SELECT 中嵌套另一个 SELECT。
        可以出现在：
        - WHERE 子句中
        - FROM 子句中（作为临时表）
        - SELECT 子句中（作为计算列）
        
        子查询类型：
        1. 标量子查询：返回单个值
        2. 列子查询：返回一列值
        3. 表子查询：返回多行多列（作为临时表）
        
        常用操作符：
        - =, <, >, <=, >=: 比较（标量子查询）
        - IN: 在列表中
        - NOT IN: 不在列表中
        - EXISTS: 存在（返回布尔值）
        - ANY/SOME: 任意一个满足
        - ALL: 所有都满足
        """
        
        print("\n" + "="*60)
        print("🔍 子查询示例")
        print("="*60)
        
        # -------------------- 示例 1：WHERE 中的子查询 --------------------
        """
        场景：找出年龄大于平均年龄的用户
        
        子查询：先计算平均年龄
        外层查询：找出年龄大于平均年龄的用户
        """
        sql1 = """
        SELECT username, age
        FROM users
        WHERE age > (
            -- 子查询：计算平均年龄
            SELECT AVG(age) FROM users
        )
        ORDER BY age DESC;
        """
        db.cursor.execute(sql1)
        
        print("\n📋 年龄大于平均年龄的用户：")
        for row in db.cursor.fetchall():
            print(f"   {row['username']}, {row['age']}岁")
        
        # -------------------- 示例 2：IN 子查询 --------------------
        """
        场景：找出发布过文章的用户
        
        子查询：从 articles 表找出有文章的用户 ID
        外层查询：从 users 表找出这些 ID 的用户
        """
        sql2 = """
        SELECT username, email
        FROM users
        WHERE id IN (
            -- 子查询：获取发布过文章的用户 ID
            SELECT DISTINCT user_id FROM articles
        );
        """
        db.cursor.execute(sql2)
        
        print("\n📋 发布过文章的用户：")
        for row in db.cursor.fetchall():
            print(f"   {row['username']} ({row['email']})")
        
        # -------------------- 示例 3：FROM 中的子查询 --------------------
        """
        场景：统计每个用户的文章数、评论数（作为临时表）
        
        FROM 子查询：将查询结果作为临时表使用
        需要给子查询起别名（别名 AS xxx）
        """
        sql3 = """
        SELECT 
            u.username,
            IFNULL(ac.article_count, 0) as article_count,
            IFNULL(cc.comment_count, 0) as comment_count
        FROM users u
        LEFT JOIN (
            -- 子查询1：每个用户的文章数
            SELECT user_id, COUNT(*) as article_count
            FROM articles
            GROUP BY user_id
        ) ac ON u.id = ac.user_id
        LEFT JOIN (
            -- 子查询2：每个用户的评论数
            SELECT user_id, COUNT(*) as comment_count
            FROM comments
            GROUP BY user_id
        ) cc ON u.id = cc.user_id
        ORDER BY article_count DESC, comment_count DESC;
        """
        db.cursor.execute(sql3)
        
        print("\n📋 用户文章数和评论数（FROM 子查询）：")
        for row in db.cursor.fetchall():
            print(f"   {row['username']}: 文章 {row['article_count']}, 评论 {row['comment_count']}")
        
        # -------------------- 示例 4：EXISTS 子查询 --------------------
        """
        EXISTS: 检查子查询是否返回任何行
        返回 True/False
        
        场景：找出有评论的文章
        """
        sql4 = """
        SELECT a.title
        FROM articles a
        WHERE EXISTS (
            -- 检查是否有评论
            SELECT 1 FROM comments c WHERE c.article_id = a.id
        );
        """
        db.cursor.execute(sql4)
        
        print("\n📋 有评论的文章（EXISTS 子查询）：")
        for row in db.cursor.fetchall():
            print(f"   {row['title']}")
        
        # -------------------- 示例 5：比较子查询 --------------------
        """
        ALL: 所有都满足
        ANY/SOME: 任意一个满足
        
        场景：找出年龄最大的用户
        """
        sql5 = """
        SELECT username, age
        FROM users
        WHERE age >= ALL (
            SELECT age FROM users
        );
        """
        db.cursor.execute(sql5)
        
        print("\n📋 年龄最大的用户（ALL 子查询）：")
        for row in db.cursor.fetchall():
            print(f"   {row['username']}, {row['age']}岁")


# ================================================================================
# 第五章：视图操作
# ================================================================================

class ViewOperations:
    """
    视图（VIEW）操作
    
    视图是什么？
    - 视图是一个虚拟表，不存储数据
    - 视图的查询结果基于其他表的查询
    - 每次查询视图时，实际上是执行定义视图的 SQL
    
    视图的优点：
    - 简化复杂查询（类似保存的查询模板）
    - 提高代码复用性
    - 增强安全性（只暴露需要的字段）
    - 不占用额外存储空间
    
    视图的缺点：
    - 查询性能可能较低
    - 某些视图不可更新（包含聚合函数、DISTINCT、GROUP BY 等）
    """
    
    @staticmethod
    def create_view(db: DatabaseConnection):
        """
        创建视图
        
        SQL 语法：
        CREATE [OR REPLACE] VIEW view_name AS
        SELECT ...;
        
        OR REPLACE: 如果视图已存在，则替换（需要相同的列名）
        """
        
        # -------------------- 示例 1：创建用户文章统计视图 --------------------
        """
        场景：创建一个视图，展示用户及其文章统计信息
        """
        sql1 = """
        CREATE OR REPLACE VIEW user_article_stats AS
        SELECT 
            u.id as user_id,
            u.username,
            u.email,
            COUNT(a.id) as article_count,
            COALESCE(SUM(a.views), 0) as total_views,
            MAX(a.created_at) as latest_article
        FROM users u
        LEFT JOIN articles a ON u.id = a.user_id
        GROUP BY u.id, u.username, u.email;
        """
        db.cursor.execute(sql1)
        print("✅ 视图 user_article_stats 已创建")
        
        # -------------------- 示例 2：创建文章详情视图 --------------------
        """
        场景：创建一个视图，展示完整的文章信息（含作者）
        """
        sql2 = """
        CREATE OR REPLACE VIEW article_details AS
        SELECT 
            a.id as article_id,
            a.title,
            a.content,
            a.views,
            a.is_published,
            a.published_at,
            a.created_at,
            u.username as author,
            u.email as author_email,
            (SELECT COUNT(*) FROM comments c WHERE c.article_id = a.id) as comment_count
        FROM articles a
        INNER JOIN users u ON a.user_id = u.id;
        """
        db.cursor.execute(sql2)
        print("✅ 视图 article_details 已创建")
        
        # 提交
        db.connection.commit()
    
    @staticmethod
    def query_view(db: DatabaseConnection):
        """
        查询视图
        
        查询视图和查询普通表的方式完全一样！
        """
        
        print("\n📋 查询 user_article_stats 视图：")
        sql = "SELECT * FROM user_article_stats ORDER BY article_count DESC;"
        db.cursor.execute(sql)
        
        for row in db.cursor.fetchall():
            print(f"   {row['username']}: {row['article_count']} 篇文章, "
                  f"{row['total_views']} 阅读")
        
        print("\n📋 查询 article_details 视图：")
        sql2 = "SELECT title, author, comment_count FROM article_details;"
        db.cursor.execute(sql2)
        
        for row in db.cursor.fetchall():
            print(f"   《{row['title']}》- 作者: {row['author']}, "
                  f"评论: {row['comment_count']}")
    
    @staticmethod
    def drop_view(db: DatabaseConnection):
        """
        删除视图
        
        SQL 语法：
        DROP VIEW [IF EXISTS] view_name;
        
        注意：删除视图不会影响底层表的数据
        """
        sql = "DROP VIEW IF EXISTS user_article_stats;"
        db.cursor.execute(sql)
        print("✅ 视图已删除")


# ================================================================================
# 第六章：事务控制（TCL - Transaction Control Language）
# ================================================================================

class TransactionOperations:
    """
    事务控制操作
    
    事务（Transaction）是一组 SQL 语句的执行单元，
    事务中的所有 SQL 要么全部成功，要么全部失败。
    
    事务特性（ACID）：
    - Atomicity（原子性）：事务是最小执行单位，不可分割
    - Consistency（一致性）：事务执行前后，数据库状态保持一致
    - Isolation（隔离性）：并发事务之间互不干扰
    - Duration（持久性）：事务提交后，修改永久保存
    
    TCL 常用语句：
    - BEGIN / START TRANSACTION: 开始事务
    - COMMIT: 提交事务，保存所有修改
    - ROLLBACK: 回滚事务，撤销所有修改
    - SAVEPOINT name: 创建保存点
    - ROLLBACK TO SAVEPOINT name: 回滚到保存点
    """
    
    @staticmethod
    def basic_transaction(db: DatabaseConnection):
        """
        基本事务操作
        """
        
        print("\n" + "="*60)
        print("🔄 事务控制示例")
        print("="*60)
        
        # -------------------- 示例 1：成功提交事务 --------------------
        """
        场景：用户注册并发布文章（需要两条 INSERT）
        如果任何一条失败，整个事务都应该回滚
        """
        print("\n📋 提交事务示例：")
        
        try:
            # 开启事务
            db.cursor.execute("START TRANSACTION")
            
            # 步骤 1：创建新用户
            db.cursor.execute("""
                INSERT INTO users (username, email, password_hash, age)
                VALUES ('newuser', 'newuser@test.com', 'hash123', 25);
            """)
            new_user_id = db.cursor.lastrowid
            print(f"   ✅ 插入用户 ID: {new_user_id}")
            
            # 步骤 2：为该用户创建文章
            db.cursor.execute("""
                INSERT INTO articles (user_id, title, content, is_published)
                VALUES (%s, '我的第一篇文章', '内容...', 1);
            """, (new_user_id,))
            print(f"   ✅ 插入文章")
            
            # 提交事务
            db.connection.commit()
            print("   ✅ 事务提交成功！")
            
        except Exception as e:
            # 发生错误，回滚事务
            db.connection.rollback()
            print(f"   ❌ 事务回滚: {e}")
        
        # -------------------- 示例 2：回滚事务 --------------------
        """
        场景：模拟操作失败，自动回滚
        """
        print("\n📋 回滚事务示例：")
        
        try:
            db.cursor.execute("START TRANSACTION")
            
            # 更新用户状态
            db.cursor.execute("""
                UPDATE users SET status = 'banned' WHERE username = 'newuser';
            """)
            print("   ✅ 更新用户状态")
            
            # 模拟错误（故意插入一个会失败的 SQL）
            # 这里插入一个重复的用户名（唯一约束会失败）
            db.cursor.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES ('newuser', 'another@test.com', 'hash');
            """)
            
            # 如果上面没报错，提交
            db.connection.commit()
            
        except Exception as e:
            # 发生错误，回滚
            db.connection.rollback()
            print(f"   ⚠️ 发生错误，事务已回滚: {str(e)[:50]}")
        
        # -------------------- 示例 3：保存点 --------------------
        """
        保存点（SAVEPOINT）允许回滚到事务中的某个点，
        而不是全部回滚。
        
        场景：多次插入，可以回滚到任意保存点
        """
        print("\n📋 保存点示例：")
        
        db.cursor.execute("START TRANSACTION")
        
        # 插入第一个用户
        db.cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES ('user1', 'user1@test.com', 'hash1');
        """)
        print("   ✅ 插入 user1")
        
        # 创建保存点 1
        db.cursor.execute("SAVEPOINT sp1;")
        
        # 插入第二个用户
        db.cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES ('user2', 'user2@test.com', 'hash2');
        """)
        print("   ✅ 插入 user2（即将回滚）")
        
        # 回滚到保存点 1（撤销 user2 的插入，保留 user1）
        db.cursor.execute("ROLLBACK TO SAVEPOINT sp1;")
        print("   ↩️ 回滚到保存点 sp1（user2 被撤销，user1 保留）")
        
        # 提交
        db.connection.commit()
        
        # 验证结果
        db.cursor.execute("SELECT username FROM users WHERE username IN ('user1', 'user2');")
        remaining = [row['username'] for row in db.cursor.fetchall()]
        print(f"   结果：只保留了 {remaining}")


# ================================================================================
# 第七章：性能优化
# ================================================================================

class PerformanceOptimization:
    """
    MySQL 性能优化技巧
    """
    
    @staticmethod
    def explain_query(db: DatabaseConnection):
        """
        使用 EXPLAIN 分析查询执行计划
        
        EXPLAIN / DESCRIBE:
        - 显示 MySQL 如何执行查询
        - 帮助发现查询问题（如全表扫描）
        - 是优化的第一步
        
        重要字段：
        - type: 连接类型
          * system/const: 最佳，主键或唯一索引查询
          * eq_ref: 唯一索引扫描
          * ref: 非唯一索引扫描
          * range: 索引范围扫描
          * index: 全索引扫描
          * ALL: 全表扫描（最差，需要优化）
        - possible_keys: 可能使用的索引
        - key: 实际使用的索引
        - rows: 预计扫描的行数（越小越好）
        - Extra: 额外信息
        """
        
        print("\n" + "="*60)
        print("📈 查询性能分析（EXPLAIN）")
        print("="*60)
        
        # -------------------- 示例 1：分析简单查询 --------------------
        """
        场景：分析按用户名查询的 SQL
        """
        sql1 = "SELECT * FROM users WHERE username = 'zhangsan';"
        
        print("\n📋 SQL: SELECT * FROM users WHERE username = 'zhangsan'")
        print("-" * 60)
        
        db.cursor.execute(f"EXPLAIN {sql1}")
        result = db.cursor.fetchone()
        
        print(f"   type: {result['type']} (连接类型)")
        print(f"   possible_keys: {result['possible_keys']} (可用索引)")
        print(f"   key: {result['key']} (实际使用索引)")
        print(f"   rows: {result['rows']} (预计扫描行数)")
        
        # -------------------- 示例 2：分析 JOIN 查询 --------------------
        """
        场景：分析连接查询
        """
        sql2 = """
        SELECT a.title, u.username 
        FROM articles a 
        INNER JOIN users u ON a.user_id = u.id 
        WHERE a.is_published = 1;
        """
        
        print("\n📋 SQL: JOIN 查询")
        print("-" * 60)
        
        db.cursor.execute(f"EXPLAIN {sql2}")
        
        for result in db.cursor.fetchall():
            print(f"   表: {result['table']}, 类型: {result['type']}, "
                  f"索引: {result['key']}, 行数: {result['rows']}")
    
    @staticmethod
    def index_usage(db: DatabaseConnection):
        """
        索引使用示例
        
        索引（Index）：
        - 就像书的目录，可以快速定位数据
        - 索引会占用额外存储空间
        - 适当的索引可以大幅提升查询速度
        
        创建索引：
        CREATE INDEX idx_name ON table(column);
        CREATE UNIQUE INDEX idx_name ON table(column);
        CREATE INDEX idx_name ON table(col1, col2);  -- 复合索引
        
        删除索引：
        DROP INDEX idx_name ON table;
        """
        
        print("\n" + "="*60)
        print("🔑 索引使用示例")
        print("="*60)
        
        # 查看索引
        sql = "SHOW INDEX FROM users;"
        db.cursor.execute(sql)
        
        print("\n📋 users 表的索引：")
        for row in db.cursor.fetchall():
            print(f"   - {row['Key_name']} on {row['Column_name']} "
                  f"({row['Index_type']})")


# ================================================================================
# 主程序入口
# ================================================================================

def main():
    """
    主函数 - 演示所有 MySQL 操作
    
    执行顺序：
    1. 建立数据库连接
    2. DDL: 创建数据库和表
    3. DML: 插入测试数据
    4. DQL: 各种查询演示
    5. 视图操作
    6. 事务控制
    7. 性能优化
    8. 关闭连接
    """
    
    print("\n" + "="*60)
    print("🎓 MySQL Python 完整教程")
    print("="*60)
    
    try:
        # ===== 1. 建立数据库连接 =====
        print("\n【第1步】连接数据库...")
        db = DatabaseConnection()
        db.connect()
        
        # ===== 2. DDL 操作 =====
        print("\n" + "="*60)
        print("【第2步】DDL - 数据定义语言")
        print("="*60)
        
        # 创建数据库
        DDLOperations.create_database(db)
        
        # 创建表
        DDLOperations.create_tables(db)
        
        # 查看表
        DDLOperations.show_tables(db)
        
        # 查看表结构
        DDLOperations.describe_table(db, 'users')
        DDLOperations.describe_table(db, 'articles')
        
        # 修改表结构
        DDLOperations.alter_table(db)
        
        # ===== 3. DML 操作 =====
        print("\n" + "="*60)
        print("【第3步】DML - 数据操作语言")
        print("="*60)
        
        # 插入数据
        DMLOperations.insert_single_record(db)
        DMLOperations.insert_multiple_records(db)
        DMLOperations.insert_articles(db)
        
        # 更新数据
        DMLOperations.update_records(db)
        
        # 删除数据
        # DMLOperations.delete_records(db)
        
        # ===== 4. DQL 操作 =====
        print("\n" + "="*60)
        print("【第4步】DQL - 数据查询语言")
        print("="*60)
        
        # 基础查询
        DQLOperations.basic_select(db)
        
        # 聚合函数
        DQLOperations.aggregate_functions(db)
        
        # 分组查询
        DQLOperations.group_by(db)
        
        # 连接查询
        DQLOperations.join_queries(db)
        
        # 子查询
        DQLOperations.subqueries(db)
        
        # ===== 5. 视图操作 =====
        print("\n" + "="*60)
        print("【第5步】视图操作")
        print("="*60)
        
        # 创建视图
        ViewOperations.create_view(db)
        
        # 查询视图
        ViewOperations.query_view(db)
        
        # ===== 6. 事务控制 =====
        print("\n" + "="*60)
        print("【第6步】事务控制")
        print("="*60)
        
        TransactionOperations.basic_transaction(db)
        
        # ===== 7. 性能优化 =====
        print("\n" + "="*60)
        print("【第7步】性能优化")
        print("="*60)
        
        PerformanceOptimization.explain_query(db)
        PerformanceOptimization.index_usage(db)
        
        # ===== 8. 清理和关闭 =====
        print("\n" + "="*60)
        print("【第8步】清理资源")
        print("="*60)
        
        # 删除测试视图
        ViewOperations.drop_view(db)
        
        # 关闭连接
        db.close()
        
        print("\n" + "="*60)
        print("🎉 教程演示完成！")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
