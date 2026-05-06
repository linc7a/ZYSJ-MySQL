# MySQL Python 完整教程

> 本教程通过 Python 代码详细演示 MySQL 的各种操作，每个知识点都带有详细的中文注释和运行结果。

---

## 目录

1. [数据库连接配置](#1-数据库连接配置)
2. [DDL - 数据定义语言](#2-ddl---数据定义语言)
3. [DML - 数据操作语言](#3-dml---数据操作语言)
4. [DQL - 数据查询语言](#4-dql---数据查询语言)
5. [视图操作](#5-视图操作)
6. [事务控制](#6-事务控制)
7. [性能优化](#7-性能优化)

---

## 1. 数据库连接配置

### 1.1 为什么要用配置文件？

- **集中管理连接参数**：方便修改，不需要在代码中到处找
- **避免硬编码敏感信息**：密码等信息放在配置中更安全
- **便于多环境切换**：开发、测试、生产可以使用不同配置

### 1.2 配置参数说明

| 参数 | 说明 | 示例值 |
|------|------|--------|
| host | MySQL 服务器地址，localhost 表示本机（127.0.0.1） | localhost |
| port | MySQL 服务端口，默认是 3306 | 3306 |
| user | 用户名，root 是 MySQL 的超级管理员账户 | root |
| password | 密码 | root123456 |
| database | 默认连接的数据库名 | tutorial_db |
| charset | 字符编码，utf8mb4 是 UTF-8 的完整实现，支持 emoji 等特殊字符。旧版 utf8 只支持 3 字节，utf8mb4 支持 4 字节 | utf8mb4 |

### 1.3 Python 连接代码

```python
import pymysql
from pymysql.cursors import DictCursor  # 用于将查询结果转为字典格式

# 数据库配置
config = {
    'host': 'localhost',        # MySQL 服务器地址
    'port': 3306,               # 端口
    'user': 'root',             # 用户名
    'password': 'root123456',  # 密码
    'database': 'tutorial_db',  # 数据库名
    'charset': 'utf8mb4',      # 字符编码
    'cursorclass': DictCursor  # 结果转为字典
}

# 建立连接
conn = pymysql.connect(**config)
cursor = conn.cursor()
```

### 1.4 pymysql.connect() 关键参数解释

- **cursorclass=DictCursor**：查询结果返回字典格式。默认为元组格式，字典格式更容易理解和使用
- **游标（Cursor）**：用于执行 SQL 语句和获取结果。就像鼠标指针一样，在数据表上移动并操作数据

### 运行结果

```
============================================================
MySQL Python 完整教程
============================================================
【第1步】连接数据库...
✅ 数据库连接成功！
============================================================
```

---

## 2. DDL - 数据定义语言

> DDL（Database Definition Language）包括：
> - CREATE：创建数据库、表、索引等
> - ALTER：修改表结构
> - DROP：删除数据库、表等
> - TRUNCATE：清空表数据（不可恢复）

### 2.1 创建数据库

#### SQL 语法

```sql
CREATE DATABASE [IF NOT EXISTS] database_name
[DEFAULT CHARACTER SET charset_name]
[DEFAULT COLLATE collation_name];
```

#### 参数说明

| 参数 | 说明 |
|------|------|
| IF NOT EXISTS | 如果数据库已存在，不报错（防止重复创建） |
| DEFAULT CHARACTER SET | 设置默认字符集，utf8mb4 是 MySQL 推荐的全 UTF-8 编码 |
| DEFAULT COLLATE | 设置排序规则，utf8mb4_unicode_ci 是通用的 Unicode 排序，ci 表示不区分大小写（case insensitive） |

#### Python 代码

```python
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
```

### 2.2 创建数据表

#### MySQL 常用数据类型

**数值类型：**
| 类型 | 说明 |
|------|------|
| TINYINT | 1 字节，-128~127（或 0~255 无符号） |
| SMALLINT | 2 字节，-32768~32767 |
| INT/INTEGER | 4 字节，约 ±21 亿 |
| BIGINT | 8 字节，超大整数 |
| DECIMAL(p, s) | 精确数值，p=总位数，s=小数位数 |
| FLOAT/DOUBLE | 浮点数（不精确） |

**字符串类型：**
| 类型 | 说明 |
|------|------|
| CHAR(n) | 固定长度字符串（0-255） |
| VARCHAR(n) | 可变长度字符串（0-65535） |
| TEXT | 长文本（最大 65535 字节） |
| LONGTEXT | 超长文本（最大 4GB） |

**日期时间类型：**
| 类型 | 说明 |
|------|------|
| DATE | 日期（YYYY-MM-DD） |
| TIME | 时间（HH:MM:SS） |
| DATETIME | 日期时间（YYYY-MM-DD HH:MM:SS） |
| TIMESTAMP | 时间戳（自动设置为当前时间） |
| YEAR | 年份 |

**约束（Constraints）：**
| 约束 | 说明 |
|------|------|
| PRIMARY KEY | 主键，唯一标识每行数据 |
| AUTO_INCREMENT | 自增，用于生成唯一 ID |
| NOT NULL | 非空约束 |
| UNIQUE | 唯一约束（值不能重复） |
| DEFAULT value | 默认值 |
| CHECK condition | 检查约束（MySQL 8.0.16+） |
| FOREIGN KEY | 外键，关联其他表 |

#### SQL 语法

```sql
CREATE TABLE table_name (
    column_name datatype [constraints],
    ...
) ENGINE=InnoDB CHARSET=utf8mb4;
```

#### 表1：users 用户表

```sql
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
```

#### 表2：articles 文章表

```sql
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
```

#### 表3：comments 评论表

```sql
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
```

### 2.3 查看表结构

#### SQL 语法

```sql
DESCRIBE table_name;
-- 或
DESC table_name;
```

#### 返回字段说明

| 字段 | 说明 |
|------|------|
| Field | 字段名 |
| Type | 数据类型 |
| Null | 是否允许 NULL |
| Key | 主键/唯一键信息（PRI=主键, UNI=唯一, MUL=索引） |
| Default | 默认值 |
| Extra | 额外信息（如 auto_increment） |

### 2.4 修改表结构

#### ALTER TABLE 语法

- `ALTER TABLE table_name ADD column...`：添加字段
- `ALTER TABLE table_name MODIFY column...`：修改字段
- `ALTER TABLE table_name DROP column...`：删除字段
- `ALTER TABLE table_name RENAME TO...`：重命名表

#### 添加字段示例

```sql
ALTER TABLE users 
ADD COLUMN phone VARCHAR(20) AFTER email;
```

#### 删除字段 ⚠️ 危险操作

```sql
ALTER TABLE users DROP COLUMN phone;
-- 注意：删除字段会丢失该字段的所有数据，请谨慎操作！
```

### 运行结果

```
============================================================
【第2步】DDL - 数据定义语言
============================================================
✅ 数据库已创建/检查
✅ users 表已创建
✅ articles 表已创建
✅ comments 表已创建

📋 数据库中的表：
- articles
- comments
- users

users 表结构：
--------------------------------------------------------------------------------
字段名                  类型                        Null       Key        默认值
--------------------------------------------------------------------------------
id                   int                       NO         PRI        None
username             varchar(50)               NO         UNI        None
email                varchar(100)              NO         UNI        None
password_hash        varchar(255)              NO                    None
age                  tinyint                   YES                   None
status               enum('active','inactive','banned') YES                   active
created_at           datetime                  YES                   CURRENT_TIMESTAMP
updated_at           datetime                  YES                   CURRENT_TIMESTAMP

articles 表结构：
--------------------------------------------------------------------------------
字段名                  类型                        Null       Key        默认值
--------------------------------------------------------------------------------
id                   int                       NO         PRI        None
user_id              int                       NO         MUL        None
title                varchar(200)              NO                    None
content              text                      YES                   None
views                int                       YES                   0
is_published         tinyint(1)                YES        MUL        0
published_at         datetime                  YES                   None
created_at           datetime                  YES                   CURRENT_TIMESTAMP
updated_at           datetime                  YES                   CURRENT_TIMESTAMP

✅ 已添加 phone 字段到 users 表
```

---

## 3. DML - 数据操作语言

> DML（Data Manipulation Language）包括：
> - INSERT：插入数据
> - UPDATE：更新数据
> - DELETE：删除数据

### 3.1 插入数据 INSERT

#### SQL 语法

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

#### 注意事项

- 列名和值要一一对应
- 字符串和日期需要用单引号括起来
- 自增字段可以传 NULL 或不传，会自动生成
- 可以不指定列名，但需要按表结构顺序传入所有值

#### 单条插入

```python
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
cursor.execute(sql, user_data)

# commit() 提交事务，将数据真正写入数据库
# 如果是自动提交模式（默认），可以省略
conn.commit()

# 获取刚插入记录的 ID（自增主键）
inserted_id = cursor.lastrowid
print(f"✅ 插入单条记录成功，ID: {inserted_id}")
```

#### 批量插入

```python
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
# 一次数据库往返插入多条记录，效率高
# 比循环调用 execute() 快很多
# 适合大量数据导入
cursor.executemany(sql, users_data)
conn.commit()

# rowcount 返回受影响的行数
inserted_count = cursor.rowcount
print(f"✅ 批量插入 {inserted_count} 条记录成功")
```

### 3.2 更新数据 UPDATE

#### SQL 语法

```sql
UPDATE table_name
SET column1 = value1, column2 = value2
[WHERE condition];
```

#### ⚠️ 重要提示

- **UPDATE 语句必须带 WHERE 条件！**
- 否则会更新表中所有记录
- 建议先 SELECT 确认要更新的记录

#### WHERE 条件常用操作符

| 操作符 | 说明 |
|--------|------|
| = | 等于 |
| <> 或 != | 不等于 |
| >, <, >=, <= | 大于、小于 |
| AND | 逻辑与 |
| OR | 逻辑或 |
| IN (values) | 在列表中 |
| BETWEEN value1 AND value2 | 在范围内 |
| LIKE 'pattern' | 模糊匹配 |
| IS NULL / IS NOT NULL | 空值判断 |

#### 更新示例

```python
# 示例 1：更新单条记录
# 场景：修改用户名为 'zhangsan' 的用户年龄
sql1 = """
UPDATE users 
SET age = %s, status = %s 
WHERE username = %s;
"""
cursor.execute(sql1, (26, 'active', 'zhangsan'))

# rowcount 返回受影响的行数
if cursor.rowcount > 0:
    print(f"✅ 更新了 {cursor.rowcount} 条记录")
else:
    print("⚠️ 没有找到匹配的记录")

# 示例 2：批量更新
# 场景：将所有年龄小于 25 岁的用户状态设为 'inactive'
sql2 = "UPDATE users SET status = 'inactive' WHERE age < 25;"
cursor.execute(sql2)
print(f"✅ 批量更新了 {cursor.rowcount} 条记录")

conn.commit()
```

### 3.3 删除数据 DELETE

#### SQL 语法

```sql
DELETE FROM table_name
[WHERE condition];
```

#### ⚠️ 危险提示

- **DELETE 必须带 WHERE 条件！**
- 否则会删除表中所有数据（但不会删除表结构）
- 删除的数据可以恢复（如果有备份或事务未提交）
- 如果要清空表数据但保留结构，用 TRUNCATE 更快

#### DELETE vs TRUNCATE vs DROP

| 语句 | 说明 |
|------|------|
| DELETE | 删除数据，保留表结构，可带 WHERE 条件 |
| TRUNCATE | 清空数据，保留表结构，效率更高，自增计数器重置 |
| DROP | 删除整个表（包括结构和数据） |

#### 删除示例

```python
# 示例 1：删除指定记录
# 场景：删除用户名包含 'test' 的用户
sql1 = "DELETE FROM users WHERE username LIKE %s;"
cursor.execute(sql1, ('%test%',))

if cursor.rowcount > 0:
    print(f"✅ 删除了 {cursor.rowcount} 条记录")

conn.commit()
```

### 运行结果

```
============================================================
【第3步】DML - 数据操作语言
============================================================
✅ 插入单条记录成功，ID: 1
✅ 批量插入 5 条记录成功
✅ 插入 4 篇文章
✅ 更新了 1 条记录
✅ 批量更新了 1 条记录
```

---

## 4. DQL - 数据查询语言

> DQL（Data Query Language）核心是 SELECT 语句，是 SQL 中最复杂、功能最强大的部分。

### SELECT 语法顺序

```sql
SELECT [DISTINCT] columns, expressions, aggregates...
FROM table_name
[WHERE conditions]
[GROUP BY columns]
[HAVING group_conditions]
[ORDER BY columns [ASC|DESC]]
[LIMIT number [OFFSET number]];
```

### SELECT 执行顺序（MySQL 实际执行顺序）

1. **FROM** - 确定数据来源
2. **WHERE** - 筛选行
3. **GROUP BY** - 分组
4. **HAVING** - 筛选分组
5. **SELECT** - 选择列
6. **ORDER BY** - 排序
7. **LIMIT** - 限制数量

### 4.1 基础查询

#### 查询所有用户

```python
# SELECT *: 星号表示查询所有列
# FROM users: 从 users 表查询
# 结果：返回 users 表的所有记录和所有字段
sql = "SELECT * FROM users;"
cursor.execute(sql)

# fetchone() 取一条记录
# fetchall() 取所有记录
# fetchmany(n) 取 n 条记录
users = cursor.fetchall()

print("\n📋 所有用户：")
for user in users:
    print(f"   ID: {user['id']}, 用户名: {user['username']}, "
          f"邮箱: {user['email']}, 年龄: {user['age']}, 状态: {user['status']}")
```

#### WHERE 条件筛选

```python
# WHERE 子句：筛选满足条件的记录
# 常用比较运算符：=, <>, >, <, >=, <=
# 逻辑运算符：AND, OR, NOT
sql3 = "SELECT * FROM users WHERE age >= 25 AND status = 'active';"
cursor.execute(sql3)
```

#### LIKE 模糊查询

```python
# LIKE: 模糊匹配
# %: 匹配任意多个字符
# _: 匹配单个字符
# 'zhang%': 以 zhang 开头
# '%@example.com': 以 @example.com 结尾
# '%test%': 包含 test
sql4 = "SELECT * FROM users WHERE email LIKE %s;"
cursor.execute(sql4, ('%@example.com',))
```

#### ORDER BY 排序

```python
# ORDER BY: 排序
# ASC: 升序（从小到大，默认）
# DESC: 降序（从大到小）
# 可以按多个字段排序
sql7 = "SELECT * FROM users ORDER BY age DESC, created_at ASC;"
cursor.execute(sql7)
```

#### LIMIT 分页

```python
# LIMIT: 限制返回记录数
# LIMIT n: 返回前 n 条
# LIMIT offset, count: 从 offset 开始，取 count 条
# LIMIT count OFFSET offset: 同上，语法更清晰

# 分页查询公式：
# 第 1 页：LIMIT 0, 10 或 LIMIT 10 OFFSET 0
# 第 2 页：LIMIT 10, 10 或 LIMIT 10 OFFSET 10
# 第 n 页：LIMIT 10 OFFSET (n-1)*10
sql8 = "SELECT * FROM users ORDER BY id LIMIT 3 OFFSET 0;"
cursor.execute(sql8)
```

#### DISTINCT 去重

```python
# DISTINCT: 去除重复记录
# 注意：DISTINCT 作用于 SELECT 的所有列
# SELECT DISTINCT col1, col2 表示 (col1, col2) 组合去重
sql9 = "SELECT DISTINCT status FROM users;"
cursor.execute(sql9)
```

### 4.2 聚合函数

#### 常用聚合函数

| 函数 | 说明 |
|------|------|
| COUNT(*) | 统计记录数 |
| COUNT(column) | 统计非 NULL 值数量 |
| COUNT(DISTINCT column) | 统计去重后的数量 |
| SUM(column) | 求和 |
| AVG(column) | 平均值 |
| MAX(column) | 最大值 |
| MIN(column) | 最小值 |

#### 特点

- 聚合函数通常与 GROUP BY 一起使用
- 单独使用时，是对整个结果集聚合

#### 示例

```python
# COUNT(*): 统计所有记录数（包含 NULL）
# COUNT(column): 统计指定列非 NULL 的记录数
sql = "SELECT COUNT(*) as total_users FROM users;"
cursor.execute(sql)
result = cursor.fetchone()
print(f"\n📋 用户总数：{result['total_users']}")

# SUM/AVG: 数值统计
sql2 = "SELECT SUM(views) as total_views, AVG(views) as avg_views FROM articles;"
cursor.execute(sql2)

# MAX/MIN
sql3 = "SELECT MAX(age) as max_age, MIN(age) as min_age FROM users;"
cursor.execute(sql3)

# COUNT + DISTINCT
sql4 = "SELECT COUNT(DISTINCT status) as status_count FROM users;"
cursor.execute(sql4)
```

### 4.3 分组查询 GROUP BY

#### GROUP BY 语法

```sql
SELECT column, aggregate_function(column)
FROM table_name
GROUP BY column
[HAVING condition];
```

#### 执行过程

1. 根据 GROUP BY 的列分组
2. 对每个分组应用聚合函数
3. 返回每个分组的聚合结果

#### HAVING vs WHERE

| 子句 | 说明 |
|------|------|
| WHERE | 在分组前筛选行，不能使用聚合函数 |
| HAVING | 在分组后筛选分组，可以使用聚合函数 |

#### 示例

```python
# 按状态分组统计用户数
sql1 = """
SELECT status, COUNT(*) as user_count 
FROM users 
GROUP BY status;
"""
cursor.execute(sql1)

# HAVING: 对分组后的结果进行筛选
# 找出用户数 >= 2 的状态
sql3 = """
SELECT status, COUNT(*) as user_count 
FROM users 
GROUP BY status 
HAVING user_count >= 2;
"""
cursor.execute(sql3)

# 完整流程：WHERE 筛选 → GROUP BY 分组 → HAVING 筛选分组 → ORDER BY 排序
sql4 = """
SELECT status, COUNT(*) as user_count, AVG(age) as avg_age
FROM users 
WHERE age > 20
GROUP BY status 
HAVING user_count > 1
ORDER BY user_count DESC;
"""
cursor.execute(sql4)
```

### 4.4 连接查询 JOIN

#### 连接类型

| 类型 | 说明 |
|------|------|
| INNER JOIN (内连接) | 只返回两个表中匹配的行 |
| LEFT JOIN (左外连接) | 返回左表所有记录，右表没有的显示 NULL |
| RIGHT JOIN (右外连接) | 返回右表所有记录，左表没有的显示 NULL |
| FULL OUTER JOIN (全外连接) | 返回两个表的所有记录，MySQL 不直接支持，可用 UNION 模拟 |

#### 连接语法

```sql
SELECT columns
FROM table1
[INNER|LEFT|RIGHT] JOIN table2
ON table1.column = table2.column
[WHERE conditions];
```

#### INNER JOIN 示例

```python
# 场景：查询所有文章及其作者信息
# INNER JOIN: 只返回有作者的文章
# 即 articles.user_id 必须在 users.id 中存在
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
cursor.execute(sql1)
```

#### LEFT JOIN 示例

```python
# 场景：查询所有用户及其发布的文章数（包括没有发布文章的用户）
# LEFT JOIN: 返回所有用户，没有文章的显示 NULL
sql2 = """
SELECT 
    u.username,
    COUNT(a.id) as article_count
FROM users u
LEFT JOIN articles a ON u.id = a.user_id
GROUP BY u.id, u.username
ORDER BY article_count DESC;
"""
cursor.execute(sql2)
```

#### 自连接示例

```python
# 场景：查询评论及其父评论（回复）
# 自连接：将表与自身连接
# 需要给表起别名来区分
sql4 = """
SELECT 
    c1.content as comment,
    c2.content as reply_to
FROM comments c1
LEFT JOIN comments c2 ON c1.parent_id = c2.id
WHERE c1.parent_id IS NOT NULL;
"""
cursor.execute(sql4)
```

### 4.5 子查询

#### 子查询出现位置

- WHERE 子句中
- FROM 子句中（作为临时表）
- SELECT 子句中（作为计算列）

#### 子查询类型

| 类型 | 说明 |
|------|------|
| 标量子查询 | 返回单个值 |
| 列子查询 | 返回一列值 |
| 表子查询 | 返回多行多列（作为临时表） |

#### 常用操作符

| 操作符 | 说明 |
|--------|------|
| =, <, >, <=, >= | 比较（标量子查询） |
| IN | 在列表中 |
| NOT IN | 不在列表中 |
| EXISTS | 存在（返回布尔值） |
| ANY/SOME | 任意一个满足 |
| ALL | 所有都满足 |

#### WHERE 中的子查询

```python
# 场景：找出年龄大于平均年龄的用户
# 子查询：先计算平均年龄
# 外层查询：找出年龄大于平均年龄的用户
sql1 = """
SELECT username, age
FROM users
WHERE age > (
    -- 子查询：计算平均年龄
    SELECT AVG(age) FROM users
)
ORDER BY age DESC;
"""
cursor.execute(sql1)
```

#### IN 子查询

```python
# 场景：找出发布过文章的用户
# 子查询：从 articles 表找出有文章的用户 ID
# 外层查询：从 users 表找出这些 ID 的用户
sql2 = """
SELECT username, email
FROM users
WHERE id IN (
    -- 子查询：获取发布过文章的用户 ID
    SELECT DISTINCT user_id FROM articles
);
"""
cursor.execute(sql2)
```

#### FROM 中的子查询

```python
# 场景：统计每个用户的文章数、评论数（作为临时表）
# FROM 子查询：将查询结果作为临时表使用
# 需要给子查询起别名（别名 AS xxx）
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
cursor.execute(sql3)
```

### 运行结果

```
============================================================
【第4步】DQL - 数据查询语言
============================================================

[基础查询] 所有用户:
  ID: 1, 用户: zhangsan, 邮箱: zhangsan@example.com, 年龄: 26, 状态: active
  ID: 2, 用户: lisi, 邮箱: lisi@example.com, 年龄: 28, 状态: active
  ID: 3, 用户: wangwu, 邮箱: wangwu@example.com, 年龄: 22, 状态: inactive
  ID: 4, 用户: zhaoliu, 邮箱: zhaoliu@example.com, 年龄: 35, 状态: inactive
  ID: 5, 用户: sunqi, 邮箱: sunqi@example.com, 年龄: 30, 状态: active
  ID: 6, 用户: zhouba, 邮箱: zhouba@example.com, 年龄: 26, 状态: active
  ID: 7, 用户: newuser, 邮箱: newuser@test.com, 年龄: 25, 状态: active
  ID: 9, 用户: user1, 邮箱: user1@test.com, 年龄: None, 状态: active

[聚合函数] 用户数: 8, 平均年龄: 27.4, 最大: 35, 最小: 22

[分组查询] 按状态统计:
  状态: active, 人数: 6
  状态: inactive, 人数: 2

[连接查询] 文章及作者:
  《JavaScript 进阶》- 作者: lisi, 阅读: 200
  《Python 入门教程》- 作者: zhangsan, 阅读: 100
  《MySQL 基础指南》- 作者: zhangsan, 阅读: 50
  《Docker 容器化》- 作者: wangwu, 阅读: 0
  《我的第一篇文章》- 作者: newuser, 阅读: 0
```

---

## 5. 视图操作

### 5.1 什么是视图？

- **视图是一个虚拟表**，不存储数据
- 视图的查询结果基于其他表的查询
- 每次查询视图时，实际上是执行定义视图的 SQL

### 5.2 视图的优点

- **简化复杂查询**（类似保存的查询模板）
- **提高代码复用性**
- **增强安全性**（只暴露需要的字段）
- **不占用额外存储空间**

### 5.3 视图的缺点

- 查询性能可能较低
- 某些视图不可更新（包含聚合函数、DISTINCT、GROUP BY 等）

### 5.4 创建视图

#### SQL 语法

```sql
CREATE [OR REPLACE] VIEW view_name AS
SELECT ...;
```

- **OR REPLACE**：如果视图已存在，则替换（需要相同的列名）

#### 示例：用户文章统计视图

```python
# 场景：创建一个视图，展示用户及其文章统计信息
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
cursor.execute(sql1)
print("✅ 视图 user_article_stats 已创建")
```

#### 示例：文章详情视图

```python
# 场景：创建一个视图，展示完整的文章信息（含作者）
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
cursor.execute(sql2)
print("✅ 视图 article_details 已创建")
```

### 5.5 查询视图

```python
# 查询视图和查询普通表的方式完全一样！
sql = "SELECT * FROM user_article_stats ORDER BY article_count DESC;"
cursor.execute(sql)
```

### 5.6 删除视图

```sql
DROP VIEW [IF EXISTS] view_name;
-- 注意：删除视图不会影响底层表的数据
```

### 运行结果

```
============================================================
【第5步】视图操作
============================================================
✅ 视图 user_article_stats 已创建
✅ 视图 article_details 已创建

📋 查询 user_article_stats 视图：
zhangsan: 2 篇文章, 150 阅读
lisi: 1 篇文章, 200 阅读
wangwu: 1 篇文章, 0 阅读
zhaoliu: 0 篇文章, 0 阅读
sunqi: 0 篇文章, 0 阅读
zhouba: 0 篇文章, 0 阅读

📋 查询 article_details 视图：
《Python 入门教程》- 作者: zhangsan, 评论: 3
《MySQL 基础指南》- 作者: zhangsan, 评论: 1
《JavaScript 进阶》- 作者: lisi, 评论: 0
《Docker 容器化》- 作者: wangwu, 评论: 0
```

---

## 6. 事务控制

### 6.1 什么是事务？

事务（Transaction）是一组 SQL 语句的执行单元，事务中的所有 SQL 要么全部成功，要么全部失败。

### 6.2 事务特性（ACID）

| 特性 | 说明 |
|------|------|
| Atomicity（原子性） | 事务是最小执行单位，不可分割 |
| Consistency（一致性） | 事务执行前后，数据库状态保持一致 |
| Isolation（隔离性） | 并发事务之间互不干扰 |
| Duration（持久性） | 事务提交后，修改永久保存 |

### 6.3 TCL 常用语句

| 语句 | 说明 |
|------|------|
| BEGIN / START TRANSACTION | 开始事务 |
| COMMIT | 提交事务，保存所有修改 |
| ROLLBACK | 回滚事务，撤销所有修改 |
| SAVEPOINT name | 创建保存点 |
| ROLLBACK TO SAVEPOINT name | 回滚到保存点 |

### 6.4 提交事务示例

```python
# 场景：用户注册并发布文章（需要两条 INSERT）
# 如果任何一条失败，整个事务都应该回滚
try:
    # 开启事务
    cursor.execute("START TRANSACTION")
    
    # 步骤 1：创建新用户
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, age)
        VALUES ('newuser', 'newuser@test.com', 'hash123', 25);
    """)
    new_user_id = cursor.lastrowid
    print(f"   ✅ 插入用户 ID: {new_user_id}")
    
    # 步骤 2：为该用户创建文章
    cursor.execute("""
        INSERT INTO articles (user_id, title, content, is_published)
        VALUES (%s, '我的第一篇文章', '内容...', 1);
    """, (new_user_id,))
    print(f"   ✅ 插入文章")
    
    # 提交事务
    conn.commit()
    print("   ✅ 事务提交成功！")
    
except Exception as e:
    # 发生错误，回滚事务
    conn.rollback()
    print(f"   ❌ 事务回滚: {e}")
```

### 6.5 回滚事务示例

```python
# 场景：模拟操作失败，自动回滚
try:
    cursor.execute("START TRANSACTION")
    
    # 更新用户状态
    cursor.execute("""
        UPDATE users SET status = 'banned' WHERE username = 'newuser';
    """)
    print("   ✅ 更新用户状态")
    
    # 模拟错误（故意插入一个会失败的 SQL）
    # 这里插入一个重复的用户名（唯一约束会失败）
    cursor.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES ('newuser', 'another@test.com', 'hash');
    """)
    
    # 如果上面没报错，提交
    conn.commit()
    
except Exception as e:
    # 发生错误，回滚
    conn.rollback()
    print(f"   ⚠️ 发生错误，事务已回滚: {str(e)[:50]}")
```

### 6.6 保存点示例

```python
# 保存点（SAVEPOINT）允许回滚到事务中的某个点，
# 而不是全部回滚。
# 场景：多次插入，可以回滚到任意保存点

cursor.execute("START TRANSACTION")

# 插入第一个用户
cursor.execute("""
    INSERT INTO users (username, email, password_hash)
    VALUES ('user1', 'user1@test.com', 'hash1');
""")
print("   ✅ 插入 user1")

# 创建保存点 1
cursor.execute("SAVEPOINT sp1;")

# 插入第二个用户
cursor.execute("""
    INSERT INTO users (username, email, password_hash)
    VALUES ('user2', 'user2@test.com', 'hash2');
""")
print("   ✅ 插入 user2（即将回滚）")

# 回滚到保存点 1（撤销 user2 的插入，保留 user1）
cursor.execute("ROLLBACK TO SAVEPOINT sp1;")
print("   ↩️ 回滚到保存点 sp1（user2 被撤销，user1 保留）")

# 提交
conn.commit()

# 验证结果
cursor.execute("SELECT username FROM users WHERE username IN ('user1', 'user2');")
remaining = [row['username'] for row in cursor.fetchall()]
print(f"   结果：只保留了 {remaining}")
```

### 运行结果

```
============================================================
【第6步】事务控制
============================================================

============================================================
🔄 事务控制示例
============================================================

📋 提交事务示例：
✅ 插入用户 ID: 7
✅ 插入文章
✅ 事务提交成功！

📋 回滚事务示例：
✅ 更新用户状态
⚠️ 发生错误，事务已回滚: (1062, "Duplicate entry 'newuser' for key 'users.u

📋 保存点示例：
✅ 插入 user1
✅ 插入 user2（即将回滚）
↩️ 回滚到保存点 sp1（user2 被撤销，user1 保留）
结果：只保留了 ['user1']
```

---

## 7. 性能优化

### 7.1 使用 EXPLAIN 分析查询

#### 什么是 EXPLAIN？

- 显示 MySQL 如何执行查询
- 帮助发现查询问题（如全表扫描）
- 是优化的第一步

#### 重要字段说明

| 字段 | 说明 |
|------|------|
| type | 连接类型：system/const > eq_ref > ref > range > index > ALL（全表扫描最差） |
| possible_keys | 可能使用的索引 |
| key | 实际使用的索引 |
| rows | 预计扫描的行数（越小越好） |
| Extra | 额外信息 |

#### 连接类型说明

| 类型 | 说明 |
|------|------|
| system/const | 最佳，主键或唯一索引查询 |
| eq_ref | 唯一索引扫描 |
| ref | 非唯一索引扫描 |
| range | 索引范围扫描 |
| index | 全索引扫描 |
| ALL | **全表扫描**（最差，需要优化） |

#### 示例

```python
# 场景：分析按用户名查询的 SQL
sql1 = "SELECT * FROM users WHERE username = 'zhangsan';"

print("\n📋 SQL: SELECT * FROM users WHERE username = 'zhangsan'")
print("-" * 60)

cursor.execute(f"EXPLAIN {sql1}")
result = cursor.fetchone()

print(f"   type: {result['type']} (连接类型)")
print(f"   possible_keys: {result['possible_keys']} (可用索引)")
print(f"   key: {result['key']} (实际使用索引)")
print(f"   rows: {result['rows']} (预计扫描行数)")
```

### 7.2 索引

#### 什么是索引？

- 就像书的目录，可以快速定位数据
- 索引会占用额外存储空间
- 适当的索引可以大幅提升查询速度

#### 创建索引

```sql
CREATE INDEX idx_name ON table(column);
CREATE UNIQUE INDEX idx_name ON table(column);
CREATE INDEX idx_name ON table(col1, col2);  -- 复合索引
```

#### 删除索引

```sql
DROP INDEX idx_name ON table;
```

#### 查看索引

```sql
SHOW INDEX FROM table_name;
```

### 运行结果

```
============================================================
【第7步】性能优化
============================================================

============================================================
📈 查询性能分析（EXPLAIN）
============================================================

📋 SQL: SELECT * FROM users WHERE username = 'zhangsan'
------------------------------------------------------------
type: const (连接类型)
possible_keys: username,idx_username (可用索引)
key: username (实际使用索引)
rows: 1 (预计扫描行数)

📋 SQL: JOIN 查询
------------------------------------------------------------
表: a, 类型: ref, 索引: idx_published, 行数: 4
表: u, 类型: eq_ref, 索引: PRIMARY, 行数: 1

============================================================
🔑 索引使用示例
============================================================

📋 users 表的索引：
- PRIMARY on id (BTREE)
- username on username (BTREE)
- email on email (BTREE)
- idx_username on username (BTREE)
```

---

## 8. 清理资源

```python
# 删除视图
cursor.execute("DROP VIEW IF EXISTS user_article_stats")

# 关闭连接
cursor.close()
conn.close()
```

### 运行结果

```
============================================================
【第8步】清理资源
============================================================
✅ 视图已删除
✅ 游标已关闭
✅ 数据库连接已关闭
============================================================
教程演示完成！
============================================================
```

---

## 附录：SQL 知识点速查表

| 类别 | 语句 | 说明 |
|------|------|------|
| **DDL** | CREATE DATABASE/TABLE | 创建数据库/表 |
| **DDL** | ALTER TABLE | 修改表结构 |
| **DDL** | DROP TABLE | 删除表 |
| **DML** | INSERT INTO | 插入数据 |
| **DML** | UPDATE SET | 更新数据 |
| **DML** | DELETE FROM | 删除数据 |
| **DQL** | SELECT | 查询数据 |
| **DQL** | WHERE | 条件筛选 |
| **DQL** | ORDER BY | 排序 |
| **DQL** | GROUP BY | 分组 |
| **DQL** | HAVING | 分组筛选 |
| **DQL** | JOIN | 表连接 |
| **TCL** | COMMIT | 提交事务 |
| **TCL** | ROLLBACK | 回滚事务 |
| **TCL** | SAVEPOINT | 保存点 |

---

> 教程演示完成！
