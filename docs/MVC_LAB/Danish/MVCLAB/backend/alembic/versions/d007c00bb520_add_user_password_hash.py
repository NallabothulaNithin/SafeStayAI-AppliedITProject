"""add user password hash

Revision ID: d007c00bb520
Revises: 839a5f8a6414
Create Date: 2026-06-25 17:36:43.936695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from passlib.context import CryptContext
from sqlalchemy import text
from app.auth.hashing import hash_password

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


# revision identifiers, used by Alembic.
revision: str = 'd007c00bb520'
down_revision: Union[str, Sequence[str], None] = '839a5f8a6414'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=200), nullable=True)
    )

    op.create_unique_constraint(
        "uq_users_name",
        "users",
        ["name"]
    )

    default_hash = hash_password("password1234")

    op.execute(
        sa.text(
            "UPDATE users SET password_hash = :h"
        ).bindparams(h=default_hash)
    )

    op.alter_column(
        "users",
        "password_hash",
        nullable=False
    )

def downgrade() -> None:
   op.drop_constraint(
        "uq_users_name",
        "users",
        type_="unique"
    )
   
   op.drop_column(
        "users",
        "password_hash"
   )
