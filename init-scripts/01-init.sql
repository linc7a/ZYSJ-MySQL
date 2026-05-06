-- =====================================================
-- MySQL 初始化脚本
-- 容器启动时自动执行
-- =====================================================

-- 创建示例数据库
CREATE DATABASE IF NOT EXISTS tutorial_db 
DEFAULT CHARSET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE tutorial_db;

-- 创建示例表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INT,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入示例数据
INSERT INTO users (username, email, age, status) VALUES
('zhangsan', 'zhangsan@example.com', 25, 'active'),
('lisi', 'lisi@example.com', 30, 'active'),
('wangwu', 'wangwu@example.com', 28, 'inactive');

SELECT '✅ 数据库初始化完成！' as message;
