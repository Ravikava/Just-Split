"""empty message

Revision ID: 89df2bfae73a
Revises: 216efda772f9
Create Date: 2023-09-04 22:11:44.236965

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '89df2bfae73a'
down_revision = '216efda772f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('user_name', sa.String(length=50), nullable=True),
    sa.Column('profile_image', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone_number', sa.String(length=10), nullable=True),
    sa.Column('dob', sa.String(length=12), nullable=True),
    sa.Column('friends', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('Group', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('current_currency', sa.String(length=50), nullable=True),
    sa.Column('all_currency_used', postgresql.ARRAY(sa.String(length=50)), nullable=True),
    sa.Column('device_ids', postgresql.ARRAY(sa.String(length=256)), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('current_currency'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('friend_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('friendship_status', sa.Boolean(), nullable=True),
    sa.Column('request_status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_name', sa.String(length=50), nullable=False),
    sa.Column('group_image', sa.String(length=256), nullable=True),
    sa.Column('group_description', sa.String(length=256), nullable=True),
    sa.Column('group_members', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('left_group_member', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('group_balance', sa.Float(), nullable=True),
    sa.Column('group_status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expense_tag', sa.String(length=30), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=True),
    sa.Column('expense_currency', sa.String(length=50), nullable=True),
    sa.Column('expense_description', sa.String(length=256), nullable=True),
    sa.Column('expense_image', sa.String(length=256), nullable=True),
    sa.Column('expense_category', sa.String(length=50), nullable=True),
    sa.Column('expense_comment', sa.String(length=256), nullable=True),
    sa.Column('payer', postgresql.ARRAY(postgresql.JSONB(astext_type=sa.Text())), nullable=True),
    sa.Column('payee', postgresql.ARRAY(postgresql.JSONB(astext_type=sa.Text())), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['expense_currency'], ['user.current_currency'], ),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expense_snapshot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expense_id', sa.Integer(), nullable=True),
    sa.Column('expense_snapshots', postgresql.ARRAY(postgresql.JSONB(astext_type=sa.Text())), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['expense_id'], ['expense.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense_snapshot')
    op.drop_table('expense')
    op.drop_table('group')
    op.drop_table('friend_request')
    op.drop_table('user')
    # ### end Alembic commands ###
