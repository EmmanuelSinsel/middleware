from fastapi import APIRouter, FastAPI, Depends, Response
from database import DatabaseMatriz, DatabaseMochis, DatabaseMazatlan
from sqlalchemy import MetaData
import datetime

from sqlalchemy import select, Table


def get_conn(sucursal):
    eng = None
    conn = None
    metadata = None
    pack = []
    if sucursal == "todo":
        #  MATRIZ
        eng_mt = DatabaseMatriz().engine
        conn_mt = DatabaseMatriz().connection()
        metadata_mt = MetaData()
        metadata_mt.reflect(bind=eng_mt)
        pack.append([eng_mt, conn_mt, metadata_mt, "matriz"])
        #  MOCHIS
        eng_mo = DatabaseMochis().engine
        conn_mo = DatabaseMochis().connection()
        metadata_mo = MetaData()
        metadata_mo.reflect(bind=eng_mo)
        pack.append([eng_mo, conn_mo, metadata_mo, "mochis"])
        #  MAZATLAN
        eng_ma = DatabaseMazatlan().engine
        conn_ma = DatabaseMazatlan().connection()
        metadata_ma = MetaData()
        metadata_ma.reflect(bind=eng_ma)
        pack.append([eng_ma, conn_ma, metadata_ma, "mazatlan"])
        return pack
    else:
        if sucursal == "matriz":
            eng = DatabaseMatriz().engine
            conn = DatabaseMatriz().connection()
            metadata = MetaData()
            metadata.reflect(bind=eng)
        if sucursal == "mochis":
            eng = DatabaseMochis().engine
            conn = DatabaseMochis().connection()
            metadata = MetaData()
            metadata.reflect(bind=eng)
        if sucursal == "mazatlan":
            eng = DatabaseMazatlan().engine
            conn = DatabaseMazatlan().connection()
            metadata = MetaData()
            metadata.reflect(bind=eng)
    return [[eng, conn, metadata, sucursal]]


# DTOS

# API
app = FastAPI()
router = APIRouter(
    prefix="/Asterisk",
    tags=["Asterisk"]
)

@router.get("/buscar")
def buscar(sucursal: str = "matriz",
           date_from: str = None,
           date_to: str = None,
           ext_from: str = None,
           ext_to: str = None,
           status: str = None):
    conn_pack = get_conn(sucursal=sucursal)
    data = []
    for eng, conn, metadata, suc in conn_pack:
        cdr = Table("cdr", metadata, autoload_with=eng)
        stmt = select(cdr.c.calldate, cdr.c.src, cdr.c.dst, cdr.c.duration, cdr.c.disposition)
        if date_from:
            date = datetime.datetime.strptime(date_from, "%Y-%m-%d")
            stmt = stmt.filter(cdr.c.calldate >= date)
        if date_to:
            date = datetime.datetime.strptime(date_to, "%Y-%m-%d")
            stmt = stmt.filter(cdr.c.calldate < date)
        if ext_from:
            stmt = stmt.filter(cdr.c.src == ext_from)
        if ext_to:
            stmt = stmt.filter(cdr.c.dst == ext_to)
        if status:
            stmt = stmt.filter(cdr.c.disposition == status)
        row = conn.execute(stmt).all()
        suc_data = []
        for i in row:
            suc_data.append({
                "fecha": i[0],
                "origen": i[1],
                "destino": i[2],
                "duracion": i[3],
                "estatus": i[4]
            })
        data.append({suc:suc_data})
    return data


app.include_router(router)
