"""create tasks table

Revision ID: 5bbd66b6e4fe
Revises:
Create Date: 2024-02-20 14:56:15.664368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bbd66b6e4fe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("tasks", sa.Column("id", type_=sa.Integer, primary_key=True),
                            sa.Column("title", type_=sa.String, nullable=False),
                            sa.Column("detail", type_=sa.String, nullable=False),
                            sa.Column("priority", type_=sa.String, nullable=False, server_default="medium"),
                            sa.Column("timestamp", type_=sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
    )

def downgrade() -> None:
    op.drop_table("tasks")
