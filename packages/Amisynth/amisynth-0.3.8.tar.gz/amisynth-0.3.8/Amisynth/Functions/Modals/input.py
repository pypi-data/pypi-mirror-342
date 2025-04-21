import xfox
import Amisynth.utils as utils


@xfox.addfunc(xfox.funcs)
async def input(custom, *args, **kwargs):
    # Asegúrate de que kwargs contiene la interacción correcta
    interaction = kwargs.get('interaction')  # Asumiendo que se pasa 'interaction' en kwargs
    
    if interaction is None:
        raise ValueError("Interacción no encontrada.")

    # Acceder a los componentes (TextInput)
    inputs = interaction.data["components"][0]["components"]
    
    # Buscar el TextInput con custom_id específico
    for input_component in inputs:
        if input_component["custom_id"] == custom:  # Aquí se busca por custom_id
            return input_component["value"]
        
    print("[DEBUG INPUT] No se encontró el TextInput con el custom_id proporcionado")
    return ""
