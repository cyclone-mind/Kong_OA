from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `oa_menu` MODIFY COLUMN `cache` BOOL COMMENT '缓存' DEFAULT 0;
        ALTER TABLE `oa_menu` MODIFY COLUMN `i_frame` BOOL COMMENT '是否外链' DEFAULT 0;
        ALTER TABLE `oa_menu` MODIFY COLUMN `hidden` BOOL COMMENT '是否隐藏' DEFAULT 0;
        ALTER TABLE `oa_menu` MODIFY COLUMN `is_menu` BOOL COMMENT '是否是菜单' DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `oa_menu` MODIFY COLUMN `cache` BOOLNOT NULL COMMENT '缓存' DEFAULT 0;
        ALTER TABLE `oa_menu` MODIFY COLUMN `i_frame` BOOLNOT NULL COMMENT '是否外链' DEFAULT 0;
        ALTER TABLE `oa_menu` MODIFY COLUMN `hidden` BOOLNOT NULL COMMENT '是否隐藏' DEFAULT 0;
        ALTER TABLE `oa_menu` MODIFY COLUMN `is_menu` BOOLNOT NULL COMMENT '是否是菜单' DEFAULT 0;"""
