import xfox
import discord
import Amisynth.utils as utils

@xfox.addfunc(xfox.funcs)
async def ThreadID(name: str = None, *args, **kwargs):
    context = utils.ContextAmisynth()  # ← si es async
    obj_bot = utils.bot_inst

    # Si no se proporciona un nombre, usamos el hilo actual
    if name is None:
        return context.thread_id  # Asumiendo que context.thread_name es el nombre del hilo actual
    else:
        # Buscar entre los hilos activos del canal
        channel = context.channel
        threads = await channel.active_threads()
        for thread in threads:
            if thread.name == name:
                return thread.id
        return None  # No se encontró hilo con ese nombre
