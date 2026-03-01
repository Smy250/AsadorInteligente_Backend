"""add_seed_data_platillos

Revision ID: 8efda3b3367e
Revises: 855b468c5a7d
Create Date: 2026-02-23 23:30:26.410600

"""
from datetime import datetime, timezone
from decimal import Decimal
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '8efda3b3367e'
down_revision: Union[str, Sequence[str], None] = '855b468c5a7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = '088ebda35568'


def upgrade() -> None:
    platillos_table = sa.table('platillos',
        sa.column('id', postgresql.UUID(as_uuid=True)),
        sa.column('nombre', sa.String),
        sa.column('precio', sa.DECIMAL),
        sa.column('created_at',sa.TIMESTAMP),
        sa.column('update_at',sa.TIMESTAMP)
    )
    
    now = datetime.now(timezone.utc)

    # Insertamos las semillas
    info_platillos = [
        {'id': uuid.uuid4(),'nombre': 'Bife de Chorizo 400g', 'precio': Decimal(3500), 
            "created_at":now, "update_at":now},
        
        {'id': uuid.uuid4(),'nombre': 'Asado de Tira 500g', 'precio': Decimal(2800), 
            "created_at":now, "update_at":now},
        
        {'id': uuid.uuid4(),'nombre': 'Entraña 350g', 'precio': Decimal(4200), 
            "created_at":now, "update_at":now},
        
        {'id':uuid.uuid4(),'nombre': 'Vacío 450g', 'precio': Decimal(3200), 
            "created_at":now, "update_at":now},
        
        {'id':uuid.uuid4(),'nombre': 'Costillas 600g', 'precio' : Decimal(2500), 
            "created_at":now, "update_at":now},
        
        {'id':uuid.uuid4(),'nombre': 'Matambre 400g', 'precio' : Decimal(3800), 
            "created_at":now, "update_at":now},
        
        {'id':uuid.uuid4(),'nombre': 'Papas Fritas', 'precio' : Decimal(1200), 
            "created_at":now, "update_at":now},
        
        {'id':uuid.uuid4(),'nombre': 'Ensalada Mixta', 'precio' : Decimal(1500), 
            "created_at":now, "update_at":now},
        
        {'id':uuid.uuid4(),'nombre': 'Provoleta', 'precio' : Decimal(1800), 
            "created_at":now, "update_at":now},
        
        {'id':uuid.uuid4(),'nombre': 'Chorizo Parrillero', 'precio' : Decimal(2000), 
            "created_at":now, "update_at":now},
        
        {'id':uuid.uuid4(),'nombre': 'Morcilla', 'precio' : Decimal(1600), 
            "created_at":now, "update_at":now}
    ]
    
    tipoPlatillo_table = sa.table('tipo_platillos',
        sa.column('id', postgresql.UUID(as_uuid=True)),
        sa.column('categoria', sa.String)
    )
    
    info_tipoPlatillo = [
        {'id':uuid.uuid4(),"categoria":"Comida"},
        {'id':uuid.uuid4(),"categoria":"Bebida"} 
    ]
    
    op.bulk_insert(platillos_table, info_platillos)
    op.bulk_insert(tipoPlatillo_table,info_tipoPlatillo)


def downgrade() -> None:
    op.execute("DELETE FROM platillos")
    op.drop_table('platillos')
    op.execute("DELETE FROM tipo_platillo")
    op.drop_table('tipo_platillo')
