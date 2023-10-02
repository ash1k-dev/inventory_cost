"""create base tables(user, steamid and game)

Revision ID: 3fce28c00e69
Revises: 
Create Date: 2023-09-30 22:27:37.104393

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3fce28c00e69"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("user_name", sa.String(), nullable=True),
        sa.Column("telegram_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_id"),
    )
    op.create_table(
        "steamids",
        sa.Column("steam_id", sa.Integer(), nullable=True),
        sa.Column("steam_name", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "games",
        sa.Column("game_name", sa.String(), nullable=True),
        sa.Column("game_id", sa.Integer(), nullable=True),
        sa.Column("game_cost", sa.Integer(), nullable=True),
        sa.Column("steam_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["steam_id"],
            ["steamids.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("games")
    op.drop_table("steamids")
    op.drop_table("users")
    # ### end Alembic commands ###
