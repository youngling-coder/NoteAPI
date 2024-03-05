"""add foreign key to tasks table

Revision ID: 6078b33c173c
Revises: 016d5afb936c
Create Date: 2024-02-20 15:59:33.726740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6078b33c173c'
down_revision: Union[str, None] = '016d5afb936c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("tasks_users_fk", source_table="tasks", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("tasks_users_fk", table_name="tasks")
    op.drop_column("owner_id")
