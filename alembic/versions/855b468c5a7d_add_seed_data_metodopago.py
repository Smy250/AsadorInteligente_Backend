"""add_seed_data_metodopago

Revision ID: 855b468c5a7d
Revises: 088ebda35568
Create Date: 2026-02-21 18:15:42.534547

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '855b468c5a7d'
down_revision: Union[str, Sequence[str], None] = '088ebda35568'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = '088ebda35568'


def upgrade() -> None:
    metodosPago_table = sa.table('metodos_pago',
        sa.column('id', sa.Integer),
        sa.column('nombre', sa.String)
    )

    # Insertamos las semillas
    info_metodo_pago = [
        {'id':1,'nombre': 'Transferencia'},
        {'id':2,'nombre': 'Tarjeta'},
        {'id':3,'nombre': 'Efectivo'},
    ]
    
    op.bulk_insert(metodosPago_table, info_metodo_pago)


def downgrade() -> None:
    op.execute('DELETE FROM metodo_pago')
    op.drop_table('metodo_pago')
