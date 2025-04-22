import xfox
import discord
import Amisynth.utils as utils

@xfox.addfunc(xfox.funcs)
async def ThreadMembersCount(id: str = None, *args, **kwargs):
    """
    Devuelve el número de miembros de un hilo (Thread).
    Si no se proporciona un ID, devuelve el número de miembros del servidor.
    """
    context = utils.ContextAmisynth()  # Asegúrate de que sea async
    obj_bot = utils.bot_inst

    # Si no se proporciona un ID, obtener el número de miembros del servidor
    if id is None:
        try: 
            count = context.member_count
        except AttributeError:
            return None
    else:
        # Verificar si el ID proporcionado es un canal válido
        obj_thread = await obj_bot.fetch_channel(id)

        if isinstance(obj_thread, discord.Thread):
            fetched_members = await obj_thread.fetch_members()
            count = len(fetched_members.members if hasattr(fetched_members, "members") else fetched_members)
        else:
            return 0  # Podrías lanzar una excepción aquí si prefieres

    return count
