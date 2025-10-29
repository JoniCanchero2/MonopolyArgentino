#para usar json
import json
#desde objetos.py trae casilla y tablero
from objetos import Casilla, Tablero


class FabricaCasillas:
    #metodo estatico para funciones sin instanciar dentro de clases 
    @staticmethod
    def crear_casilla_desde_json(datos):
        # Crear la casilla base
        casilla = Casilla(
            id_propiedad=datos['id'],
            nombre=datos['nombre'],
            casilla_especial=datos['casilla_especial']
        )
        
        # configurar propiedades según el tipo
        if not datos['casilla_especial']:
            # es una propiedad normal
            casilla.color = datos.get('color')
            casilla.valor_propiedad = datos.get('valor_propiedad', 0)
            casilla.valor_alquiler = datos.get('valor_alquiler', 0)
        else:
            # es una casilla especial
            if 'monto' in datos:
                casilla.monto = datos['monto']
            # acá hay que completar con más detalles
            if 'valor_propiedad' in datos:
                casilla.valor_propiedad = datos.get('valor_propiedad', 0) 
            # cada tipo de casilla especial
        
        return casilla
    

# funcion que unicamente muesta los datos creados
def cargar_tablero_completo():
    with open('base.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    tablero = Tablero()
    
    print("=== DETALLES DE CADA CASILLA CREADA ===")
    print("=" * 60)
    
    for casilla_data in datos['casillas']:
        casilla_obj = FabricaCasillas.crear_casilla_desde_json(casilla_data)
        tablero.agregar_casilla(casilla_obj)
        
        # Mostrar TODOS los datos de cada casilla
        print(f"\n📍 CASILLA {casilla_obj.id_propiedad}: {casilla_obj.nombre}")
        print(f"   ┌ Tipo: {'ESPECIAL' if casilla_obj.casilla_especial else 'NORMAL'}")
        
        if not casilla_obj.casilla_especial:
            print(f"   ├ Color: {casilla_obj.color}")
            print(f"   ├ Valor propiedad: ${casilla_obj.valor_propiedad}")
            print(f"   └ Valor alquiler: ${casilla_obj.valor_alquiler}")
        else:
            #hasattr revisa si el atributo pedido existe
            if hasattr(casilla_obj, 'monto') and casilla_obj.monto > 0:
                print(f"   └ Monto impuesto: ${casilla_obj.monto}")
            elif hasattr(casilla_obj, 'valor_propiedad') and casilla_obj.valor_propiedad > 0:
                print(f"   └ Valor transporte: ${casilla_obj.valor_propiedad}")
            else:
                print(f"   └ Tipo especial: {casilla_obj.nombre}")
        
        # Mostrar todos los atributos del objeto
        print(f"   📊 Atributos del objeto: {vars(casilla_obj)}")
    
    print("=" * 60)
    return tablero



# llamar la función y mostrar resultados
tablero = cargar_tablero_completo()
print(f"\n🎯 RESUMEN: {len(tablero.casillas)} casillas cargadas exitosamente")
