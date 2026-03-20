"""create prediction log table

Revision ID: 0001_create_prediction_log
Revises: None
Create Date: 2026-03-20 00:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = '0001_create_prediction_log'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'prediction_log',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('feature1', sa.Float(), nullable=False),
        sa.Column('feature2', sa.Float(), nullable=False),
        sa.Column('feature3', sa.Float(), nullable=False),
        sa.Column('prediction', sa.Float(), nullable=False),
        sa.Column('model_version', sa.String(length=50), nullable=False),
        sa.Column('duration_ms', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('prediction_log')
