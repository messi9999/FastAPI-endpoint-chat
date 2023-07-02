"""Create user table

Revision ID: 238e9cab3bc2
Revises: 
Create Date: 2023-07-01 21:44:26.747626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "238e9cab3bc2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "account",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime),
    )


def downgrade() -> None:
    pass
