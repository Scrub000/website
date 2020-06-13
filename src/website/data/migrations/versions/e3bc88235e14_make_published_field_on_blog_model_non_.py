"""Make published field on Blog model non-nullable

Revision ID: e3bc88235e14
Revises: d0df9fadc5b3
Create Date: 2020-01-26 18:41:49.753399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3bc88235e14'
down_revision = 'd0df9fadc5b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogs', schema=None) as batch_op:
        batch_op.alter_column('published',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogs', schema=None) as batch_op:
        batch_op.alter_column('published',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###
