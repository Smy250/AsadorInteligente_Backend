"""add_seed_data_metodopago

Revision ID: 855b468c5a7d
Revises: 088ebda35568
Create Date: 2026-02-21 18:15:42.534547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from Models.metodo_pago import MetodoPago


# revision identifiers, used by Alembic.
revision: str = '855b468c5a7d'
down_revision: Union[str, Sequence[str], None] = '088ebda35568'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    metodosPago_table = sa.table('metodo_pago',
        sa.column('id', postgresql.UUID(as_uuid=True)),
        sa.column('nombre', sa.String)
    )

    # Insertamos las semillas
    info1 = [
        {'nombre': 'Transferencia'},
        {'nombre': 'Tarjeta'},
        {'nombre': 'Efectivo'},
    ]
    
    seed = [MetodoPago(**item).model_dump() for item in info1]
    op.bulk_insert(metodosPago_table, seed)


def downgrade() -> None:
    """Downgrade schema."""
    pass
