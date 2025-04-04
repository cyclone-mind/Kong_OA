from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `oa_dept` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除' DEFAULT 0,
    `sub_count` INT COMMENT '子部门数量',
    `name` VARCHAR(64) NOT NULL UNIQUE COMMENT '部门名',
    `enabled` BOOL NOT NULL COMMENT '状态' DEFAULT 1,
    `dept_sort` INT COMMENT '排序',
    `pid_id` INT COMMENT '父部门id',
    CONSTRAINT `fk_oa_dept_oa_dept_e8b89e44` FOREIGN KEY (`pid_id`) REFERENCES `oa_dept` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COMMENT='id, 父部门id, 子部门数目, name,';
CREATE TABLE IF NOT EXISTS `oa_job` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除' DEFAULT 0,
    `name` VARCHAR(32) COMMENT '岗位名称',
    `enabled` BOOL NOT NULL COMMENT '岗位状态' DEFAULT 0,
    `job_sort` INT NOT NULL UNIQUE COMMENT '排序'
) CHARACTER SET utf8mb4 COMMENT='岗位名称， 岗位状态， 排序，';
CREATE TABLE IF NOT EXISTS `oa_menu` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除' DEFAULT 0,
    `sub_count` INT COMMENT '子菜单数目',
    `type` INT COMMENT '菜单类型',
    `title` VARCHAR(32) UNIQUE COMMENT '菜单标题',
    `name` VARCHAR(255) UNIQUE COMMENT '前端组件名称',
    `component` VARCHAR(255) COMMENT '前端组件',
    `menu_sort` INT COMMENT '菜单排序',
    `icon` VARCHAR(255) COMMENT '菜单图标',
    `path` VARCHAR(255) COMMENT '菜单链接地址',
    `i_frame` BOOL NOT NULL COMMENT '是否外链' DEFAULT 0,
    `cache` BOOL NOT NULL COMMENT '缓存' DEFAULT 0,
    `hidden` BOOL NOT NULL COMMENT '是否隐藏' DEFAULT 0,
    `permission` VARCHAR(255) COMMENT '权限',
    `is_menu` BOOL NOT NULL COMMENT '是否是菜单' DEFAULT 0,
    `pid_id` INT COMMENT '父菜单id',
    CONSTRAINT `fk_oa_menu_oa_menu_393bc584` FOREIGN KEY (`pid_id`) REFERENCES `oa_menu` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COMMENT='上级菜单id, 子菜单数目， 菜单类型， 菜单标题， 组件名称， 组件， 排序， 图标， 连接地址， 是否外链， 缓存， 隐藏';
CREATE TABLE IF NOT EXISTS `oa_role` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除' DEFAULT 0,
    `name` VARCHAR(32) UNIQUE COMMENT '角色名',
    `level` INT COMMENT '角色级别',
    `description` VARCHAR(255) COMMENT '描述信息',
    `data_scope` VARCHAR(32) COMMENT '权限描述,唯一编码',
    `status` BOOL NOT NULL COMMENT '是否启用?状态：1启用、0禁用' DEFAULT 1
) CHARACTER SET utf8mb4 COMMENT='name, 级别， 描述， 数据权限，';
CREATE TABLE IF NOT EXISTS `OA_users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除' DEFAULT 0,
    `username` VARCHAR(150) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL COMMENT '用户密码',
    `is_active` BOOL NOT NULL COMMENT '是否是活跃用户' DEFAULT 1,
    `email` VARCHAR(32) COMMENT '邮箱',
    `nick_name` VARCHAR(32) UNIQUE COMMENT '用户昵称',
    `gender` VARCHAR(16) COMMENT '性别',
    `phone` VARCHAR(11) UNIQUE COMMENT '电话号码',
    `avatar` VARCHAR(64) NOT NULL COMMENT '头像' DEFAULT 'avatar/default.png',
    `enabled` BOOL NOT NULL COMMENT '是否启用?状态：1启用、0禁用' DEFAULT 1,
    `is_superuser` BOOL NOT NULL COMMENT '是否是超级用户' DEFAULT 0,
    `dept_id` INT COMMENT '用户和部门的关联表',
    CONSTRAINT `fk_OA_users_oa_dept_96eee14c` FOREIGN KEY (`dept_id`) REFERENCES `oa_dept` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COMMENT='用户信息类，继承自Model基类。';
CREATE TABLE IF NOT EXISTS `OA_online_user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除' DEFAULT 0,
    `browser` VARCHAR(128) COMMENT '浏览器',
    `ip` VARCHAR(64) COMMENT 'ip地址',
    `key` VARCHAR(64) COMMENT 'Token',
    `user_id` INT COMMENT '用户名',
    CONSTRAINT `fk_OA_onlin_OA_users_d8d64a8a` FOREIGN KEY (`user_id`) REFERENCES `OA_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `oa_roles_menus` (
    `oa_role_id` INT NOT NULL,
    `menu_id` INT NOT NULL,
    FOREIGN KEY (`oa_role_id`) REFERENCES `oa_role` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`menu_id`) REFERENCES `oa_menu` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_oa_roles_me_oa_role_374069` (`oa_role_id`, `menu_id`)
) CHARACTER SET utf8mb4 COMMENT='角色和菜单的关联表';
CREATE TABLE IF NOT EXISTS `oa_roles_depts` (
    `oa_role_id` INT NOT NULL,
    `dept_id` INT NOT NULL,
    FOREIGN KEY (`oa_role_id`) REFERENCES `oa_role` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`dept_id`) REFERENCES `oa_dept` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_oa_roles_de_oa_role_e266fa` (`oa_role_id`, `dept_id`)
) CHARACTER SET utf8mb4 COMMENT='角色和部门的关联表';
CREATE TABLE IF NOT EXISTS `oa_user_jobs` (
    `OA_users_id` INT NOT NULL,
    `job_id` INT NOT NULL,
    FOREIGN KEY (`OA_users_id`) REFERENCES `OA_users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`job_id`) REFERENCES `oa_job` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_oa_user_job_OA_user_1f8359` (`OA_users_id`, `job_id`)
) CHARACTER SET utf8mb4 COMMENT='用户和岗位的关联表';
CREATE TABLE IF NOT EXISTS `oa_user_roles` (
    `OA_users_id` INT NOT NULL,
    `roles_id` INT NOT NULL,
    FOREIGN KEY (`OA_users_id`) REFERENCES `OA_users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`roles_id`) REFERENCES `oa_role` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_oa_user_rol_OA_user_769ed2` (`OA_users_id`, `roles_id`)
) CHARACTER SET utf8mb4 COMMENT='用户和角色的关联表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
