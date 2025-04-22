import xfox
import discord
import Amisynth.utils as utils

@xfox.addfunc(xfox.funcs)
async def ThreadMembers(id: str = None, *args, **kwargs):
    """
    Devuelve una lista de nombres de usuario (usernames) de los miembros de un hilo (Thread).
    Si no se proporciona un ID, devuelve los miembros desde el contexto.
    """
    context = utils.ContextAmisynth()
    obj_bot = utils.bot_inst

    # Si no se proporciona un ID, obtener los miembros del contexto
    if id is None:
        members = context.members_name
    else:
        obj_thread = await obj_bot.fetch_channel(id)


        fetched_members = await obj_thread.fetch_members()
        members = fetched_members.members if hasattr(fetched_members, "members") else fetched_members
    # Convertir a lista de nombres de usuario
    usernames = [member.name for member in members]
    return usernames
