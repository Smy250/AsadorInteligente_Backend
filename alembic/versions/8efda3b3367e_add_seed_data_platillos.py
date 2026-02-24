"""add_seed_data_platillos

Revision ID: 8efda3b3367e
Revises: 855b468c5a7d
Create Date: 2026-02-23 23:30:26.410600

"""
from decimal import Decimal
import uuid
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '8efda3b3367e'
down_revision: Union[str, Sequence[str], None] = '855b468c5a7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    platillos_table = sa.table('platillos',
        sa.column('id', postgresql.UUID(as_uuid=True)),
        sa.column('nombre', sa.String),
        sa.column('precio', sa.DECIMAL),
        sa.column('created_at',sa.TIMESTAMP),
        sa.column('update_at',sa.TIMESTAMP)
    )

    # Insertamos las semillas
    info_platillos = [
        {'id': uuid.uuid4(),'nombre': 'Bife de Chorizo 400g', 'precio': Decimal(3500)},
        {'id': uuid.uuid4(),'nombre': 'Asado de Tira 500g', 'precio': Decimal(2800)},
        {'id': uuid.uuid4(),'nombre': 'Entraña 350g', 'precio': Decimal(4200)},
        {'id':uuid.uuid4(),'nombre': 'Vacío 450g', 'precio': Decimal(3200)},
        {'id':uuid.uuid4(),'nombre': 'Costillas 600g', 'precio' : Decimal(2500)},
        {'id':uuid.uuid4(),'nombre': 'Matambre 400g', 'precio' : Decimal(3800)},
        {'id':uuid.uuid4(),'nombre': 'Papas Fritas', 'precio' : Decimal(1200)},
        {'id':uuid.uuid4(),'nombre': 'Ensalada Mixta', 'precio' : Decimal(1500)},
        {'id':uuid.uuid4(),'nombre': 'Provoleta', 'precio' : Decimal(1800)},
        {'id':uuid.uuid4(),'nombre': 'Chorizo Parrillero', 'precio' : Decimal(2000)},
        {'id':uuid.uuid4(),'nombre': 'Morcilla', 'precio' : Decimal(1600)}
    ]
    
    op.bulk_insert(platillos_table, info_platillos)


def downgrade() -> None:
    op.execute("DELETE FROM platillos")
    op.drop_table('platillos')
