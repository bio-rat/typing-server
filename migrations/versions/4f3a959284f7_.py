"""empty message

Revision ID: 4f3a959284f7
Revises: d6895e5c16d3
Create Date: 2019-05-06 18:07:24.423139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f3a959284f7'
down_revision = 'd6895e5c16d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('excerpt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('text')
    )
    op.add_column('score', sa.Column('excerpt_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'score', 'excerpt', ['excerpt_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'score', type_='foreignkey')
    op.drop_column('score', 'excerpt_id')
    op.drop_table('excerpt')
    # ### end Alembic commands ###
