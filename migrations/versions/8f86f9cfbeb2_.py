"""Add 'completed' column

Revision ID: 8f86f9cfbeb2
Revises: 88247819406e
Create Date: 2020-07-02 05:02:46.042511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f86f9cfbeb2'
down_revision = '88247819406e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###\
    
    #have to allow null values when creating column because the existing data
    #will have null values after update, but then we set all nulls to false
    #and can then update the column to impose NOT NULL from then on
    op.execute('UPDATE todos SET completed=False WHERE completed IS NULL')
    op.alter_column('todos', 'completed', nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
