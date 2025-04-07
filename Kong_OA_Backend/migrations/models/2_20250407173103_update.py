from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `oa_leave` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除' DEFAULT 0,
    `reason` VARCHAR(150) NOT NULL COMMENT '请假原因',
    `time` VARCHAR(128) NOT NULL COMMENT '请假开始时间',
    `days` VARCHAR(128) NOT NULL COMMENT '请假天数',
    `type` INT NOT NULL COMMENT '请假类型:1病假，2事假，3年假' DEFAULT 1,
    `approver` VARCHAR(128) COMMENT '审批人',
    `status` INT COMMENT '请假状态:0已提交待审批，1审批通过，2审批驳回' DEFAULT 0,
    `owner_id` INT COMMENT '请假人',
    CONSTRAINT `fk_oa_leave_OA_users_22f4a0ab` FOREIGN KEY (`owner_id`) REFERENCES `OA_users` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `oa_leave`;"""
