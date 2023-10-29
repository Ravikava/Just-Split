"""empty message

Revision ID: 216efda772f9
Revises: a07564d23556
Create Date: 2023-09-04 22:10:54.415737

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '216efda772f9'
down_revision = 'a07564d23556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('friend_request')
    op.drop_table('expense_snapshot')
    op.drop_table('expense')
    op.drop_table('group')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('user_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('profile_image', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('phone_number', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('dob', sa.VARCHAR(length=12), autoincrement=False, nullable=True),
    sa.Column('friends', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.Column('Group', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.Column('current_currency', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('all_currency_used', postgresql.ARRAY(sa.VARCHAR(length=50)), autoincrement=False, nullable=True),
    sa.Column('device_ids', postgresql.ARRAY(sa.VARCHAR(length=256)), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('current_currency', name='user_current_currency_key'),
    sa.UniqueConstraint('email', name='user_email_key'),
    sa.UniqueConstraint('phone_number', name='user_phone_number_key'),
    sa.UniqueConstraint('user_name', name='user_user_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('expense',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('expense_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('expense_tag', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('total_amount', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('expense_currency', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('expense_description', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('expense_image', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('expense_category', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('expense_comment', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('payer', postgresql.ARRAY(postgresql.JSONB(astext_type=sa.Text())), autoincrement=False, nullable=True),
    sa.Column('payee', postgresql.ARRAY(postgresql.JSONB(astext_type=sa.Text())), autoincrement=False, nullable=True),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['expense_currency'], ['user.current_currency'], name='expense_expense_currency_fkey'),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name='expense_group_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='expense_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('expense_snapshot',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('expense_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('expense_snapshots', postgresql.ARRAY(postgresql.JSONB(astext_type=sa.Text())), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['expense_id'], ['expense.id'], name='expense_snapshot_expense_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='expense_snapshot_pkey')
    )
    op.create_table('friend_request',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sender_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('receiver_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('friendship_status', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('request_status', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], name='friend_request_receiver_id_fkey'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], name='friend_request_sender_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='friend_request_pkey')
    )
    op.create_table('group',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('group_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('group_image', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('group_description', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('group_members', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.Column('left_group_member', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True),
    sa.Column('group_balance', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('group_status', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='group_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='group_pkey')
    )
    # ### end Alembic commands ###