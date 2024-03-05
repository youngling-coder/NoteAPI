"""create tasks users table

Revision ID: 016d5afb936c
Revises: 5bbd66b6e4fe
Create Date: 2024-02-20 15:54:11.324344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '016d5afb936c'
down_revision: Union[str, None] = '5bbd66b6e4fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", type_=sa.Integer, primary_key=True),
                        sa.Column("full_name", type_=sa.String, nullable=True),
                        sa.Column("username", type_=sa.String, nullable=False),
                        sa.Column("password", type_=sa.String, nullable=False),
                        sa.Column("timestamp", type_=sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False))


def downgrade() -> None:
    op.drop_table("users")
