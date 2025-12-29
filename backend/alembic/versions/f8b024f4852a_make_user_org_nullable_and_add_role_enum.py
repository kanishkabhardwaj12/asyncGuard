"""make user org nullable and add role enum

Revision ID: f8b024f4852a
Revises: 02910d21b969
Create Date: 2025-12-20 19:58:11.703017
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f8b024f4852a"
down_revision = "02910d21b969"
branch_labels = None
depends_on = None


# Define ENUM explicitly (PostgreSQL-level type)
userrole_enum = postgresql.ENUM(
    "viewer",
    "auditor",
    "admin",
    name="userrole",
)


def upgrade():
    # 1. Create ENUM type
    userrole_enum.create(op.get_bind(), checkfirst=True)

    # 2. Alter role column to ENUM
    op.alter_column(
        "users",
        "role",
        existing_type=sa.VARCHAR(length=50),
        type_=userrole_enum,
        nullable=False,
        postgresql_using="role::userrole",
    )


    # 3. Make org_id nullable
    op.alter_column(
        "users",
        "org_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )

    # 4. Drop old FK and recreate with ON DELETE SET NULL
    op.drop_constraint(
        "users_org_id_fkey",
        "users",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "users_org_id_fkey",
        "users",
        "organizations",
        ["org_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade():
    # 1. Drop FK
    op.drop_constraint(
        "users_org_id_fkey",
        "users",
        type_="foreignkey",
    )

    # 2. Recreate FK without ON DELETE SET NULL
    op.create_foreign_key(
        "users_org_id_fkey",
        "users",
        "organizations",
        ["org_id"],
        ["id"],
    )

    # 3. Make org_id NOT NULL again
    op.alter_column(
        "users",
        "org_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    # 4. Convert role back to VARCHAR
    op.alter_column(
        "users",
        "role",
        existing_type=userrole_enum,
        type_=sa.VARCHAR(length=50),
        nullable=False,
    )

    # 5. Drop ENUM type
    userrole_enum.drop(op.get_bind(), checkfirst=True)
