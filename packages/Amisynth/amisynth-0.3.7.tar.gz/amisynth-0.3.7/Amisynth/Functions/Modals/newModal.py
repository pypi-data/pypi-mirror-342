import xfox
import Amisynth.utils as utils
import discord

@xfox.addfunc(xfox.funcs)
async def newModal(id, nombre, *args, **kwargs):
    # Usamos los componentes que tienes en utils.modals (que asumo son discord.ui.TextInput)
    print(f"[DEBUG NEWMODAL] Parámetros recibidos: id={id}, nombre={nombre}, args={args}, kwargs={kwargs}")
    
    n = utils.modals
    print(f"[DEBUG NEWMODAL] Lista de modales: {n}")
    
    # Creamos el modal usando la lista de componentes
    view = discord.ui.Modal(title=nombre, custom_id=id)
    print(f"[DEBUG NEWMODAL] Modal creado: {view}")

    for i in n:
        view.add_item(i)
        print(f"[DEBUG NEWMODAL] Componente agregado al modal: {i}")

    # Definir lo que ocurre cuando el modal se envíe
    async def on_submit(interaction: discord.Interaction):
        # Extraer los valores de los componentes
        values = {}
        print(f"[DEBUG NEWMODAL] Enviando valores del modal: {values}")
        for child in view.children:
            values[child.custom_id] = child.value or "No especificado"
            print(f"[DEBUG NEWMODAL] Valor de {child.custom_id}: {child.value}")
        
        # Crear el mensaje con los resultados
        response_message = "\n".join([f"{key}: {value}" for key, value in values.items()])
        print(f"[DEBUG NEWMODAL] Mensaje a enviar: {response_message}")

        # Enviar el mensaje como respuesta
        await interaction.response.send_message(response_message, ephemeral=True)
        print("[DEBUG NEWMODAL] Mensaje enviado como respuesta.")

    # Asignar la función on_submit al modal
    view.on_submit = on_submit
    print(f"[DEBUG NEWMODAL] Función on_submit asignada al modal.")

    # Actualizar los modales en utils (si es necesario para mantener el estado)
    utils.modals = view
    print(f"[DEBUG NEWMODAL] Modal actualizado en utils.modals.")

    # Retornar vacío, ya que el modal se maneja internamente
    return ""
