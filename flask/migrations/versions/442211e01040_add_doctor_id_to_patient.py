from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# Revision identifiers, used by Alembic.
revision = '442211e01040'
down_revision = 'c0acb5d78ab3'
branch_labels = None
depends_on = None

def upgrade():
    # 获取数据库连接
    conn = op.get_bind()

    # 查询表的列信息
    result = conn.execute(text('PRAGMA table_info(patients)'))
    columns = [row[1] for row in result]  # row[1] 是列名

    # 如果 doctor_id 列不存在，则添加它
    if 'doctor_id' not in columns:
        op.add_column('patients', sa.Column('doctor_id', sa.Integer(), nullable=True))

    # 如果 old_column_name 列存在，则删除它
    if 'old_column_name' in columns:
        op.drop_column('patients', 'old_column_name')

def downgrade():
    # 获取数据库连接
    conn = op.get_bind()

    # 查询表的列信息
    result = conn.execute(text('PRAGMA table_info(patients)'))
    columns = [row[1] for row in result]  # row[1] 是列名

    # 恢复 old_column_name 列
    if 'old_column_name' not in columns:
        op.add_column('patients', sa.Column('old_column_name', sa.Integer(), nullable=True))

    # 删除 doctor_id 列
    if 'doctor_id' in columns:
        op.drop_column('patients', 'doctor_id')
