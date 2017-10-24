"""initilization

Revision ID: 2e6091162b4b
Revises: 
Create Date: 2014-12-07 16:36:14.966285

"""

# revision identifiers, used by Alembic.
revision = '2e6091162b4b'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'participant',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('timestamp', sa.TIMESTAMP),
            sa.Column('first_name', sa.String(100), nullable=False),
            sa.Column('last_name', sa.String(100), nullable=False),
            sa.Column('age', sa.Integer, nullable=False)
            sa.Column('major', sa.Text),
            sa.Column('college_name', sa.Text),
            sa.Column('academic_year', sa.Integer),
            sa.Column('photo', sa.Text),
            sa.Column('score', sa.Integer),
            sa.Column('eliminated', sa.Boolean)
            sa.Column('first_round_answers', sa.Text),
            sa.Column('first_round_elimination_vote', sa.String(100)),
            sa.Column('second_round_answers', sa.Text),
            sa.Column('second_round_elimination_vote', sa.String(100))
    )

    op.create_table(
            'player',
            sa.Column('name', sa.Text),
            sa.Column('photo_url', sa.String),
            sa.Column('rank', sa.Integer),
            sa.Column('score', sa.Integer),
            sa.Column('eliminated', sa.Boolean)
    )

def downgrade():
    op.drop_table('participant')
    op.drop_table('player')

