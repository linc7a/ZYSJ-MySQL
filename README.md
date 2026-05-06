# MySQL Python 完整教程

一个通过 Python 代码详细演示 MySQL 操作的完整教程项目。

---

## 📁 项目结构

```
mysql-tutorial/
├── docker-compose.yml     # Docker Compose 配置，启动 MySQL 容器
├── mysql_tutorial.py      # Python MySQL 教程代码（超详细注释）
├── requirements.txt       # Python 依赖
├── README.md              # 本文件
└── init-scripts/          # MySQL 初始化脚本目录（可选）
```

---

## 🚀 快速开始

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 MySQL 容器

```bash
cd mysql-tutorial
docker-compose up -d
```

这将：
- 拉取 MySQL 8.0 镜像
- 创建并启动 MySQL 容器
- 容器名称：`mysql-tutorial`
- 端口：3306（映射到本机）
- root 密码：`root123456`

### 3. 运行教程代码

```bash
python mysql_tutorial.py
```

---

## 🔧 Docker Compose 配置说明

| 配置项 | 说明 |
|--------|------|
| 镜像 | mysql:8.0 |
| 容器名 | mysql-tutorial |
| 端口 | 3306:3306 |
| 密码 | root123456 |
| 数据卷 | mysql-data（持久化存储）|

### 常用命令

```bash
# 启动 MySQL
docker-compose up -d

# 查看容器状态
docker-compose ps

# 查看容器日志
docker-compose logs -f

# 停止 MySQL
docker-compose down

# 删除数据卷（彻底清除数据）
docker-compose down -v
```

---

## 📚 教程内容

代码中详细演示了以下 MySQL 知识点：

### 1. DDL - 数据定义语言
- `CREATE DATABASE` - 创建数据库
- `CREATE TABLE` - 创建表
- 约束：主键、外键、唯一、非空、默认值、检查约束
- `ALTER TABLE` - 修改表结构
- `DROP TABLE` - 删除表
- 索引的创建和使用

### 2. DML - 数据操作语言
- `INSERT INTO` - 插入数据（单条/批量）
- `UPDATE SET` - 更新数据
- `DELETE FROM` - 删除数据
- `TRUNCATE TABLE` - 清空表

### 3. DQL - 数据查询语言
- `SELECT` - 基本查询
- `WHERE` - 条件筛选
- `ORDER BY` - 排序
- `LIMIT` - 分页
- `DISTINCT` - 去重
- 聚合函数：`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`
- `GROUP BY` - 分组
- `HAVING` - 分组筛选
- 连接查询：`INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`
- 自连接
- 子查询：标量/列/表子查询

### 4. 视图
- `CREATE VIEW` - 创建视图
- 查询视图
- `DROP VIEW` - 删除视图

### 5. 事务控制
- `BEGIN` / `START TRANSACTION` - 开始事务
- `COMMIT` - 提交事务
- `ROLLBACK` - 回滚事务
- `SAVEPOINT` - 保存点

### 6. 性能优化
- `EXPLAIN` - 分析查询执行计划
- 索引使用和查看

---

## 🐍 Python 代码说明

### 数据库连接

```python
import pymysql

# 建立连接
connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root123456',
    database='tutorial_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor  # 结果转为字典
)
```

### 执行 SQL

```python
cursor = connection.cursor()

# 执行单条 SQL
cursor.execute("SELECT * FROM users WHERE id = %s", (1,))

# 执行多条 SQL
cursor.executemany("INSERT INTO users (name) VALUES (%s)", [('Alice',), ('Bob',)])

# 获取结果
result = cursor.fetchone()      # 获取一条
results = cursor.fetchall()      # 获取所有

# 提交事务
connection.commit()

# 关闭
cursor.close()
connection.close()
```

---

## 📌 注意事项

1. **密码安全**：本教程密码 `root123456` 仅用于演示，生产环境请使用强密码！
2. **数据备份**：重要数据请定期备份，Docker 卷中的数据可以导出备份
3. **端口占用**：如果 3306 端口被占用，可以修改 `docker-compose.yml` 中的端口映射

---

## 🔗 相关资源

- [MySQL 官方文档](https://dev.mysql.com/doc/)
- [PyMySQL 文档](https://pymysql.readthedocs.io/)
- [Docker MySQL 镜像](https://hub.docker.com/_/mysql)

---

祝你学习愉快！🎉
