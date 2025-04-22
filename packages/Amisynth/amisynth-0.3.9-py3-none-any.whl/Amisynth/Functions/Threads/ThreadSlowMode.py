import xfox
import discord
import Amisynth.utils as utils

@xfox.addfunc(xfox.funcs)
async def ThreadSlowMode(*args, **kwargs):
    """
    Devuelve el número de miembros de un hilo (Thread).
    Si no se proporciona un ID, devuelve el número de miembros del servidor.
    """
    context = utils.ContextAmisynth()  # Asegúrate de que sea async

    return context.slowmode_delay
