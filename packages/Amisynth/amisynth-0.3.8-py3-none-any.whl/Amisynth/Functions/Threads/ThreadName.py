import xfox
import discord
import Amisynth.utils as utils

@xfox.addfunc(xfox.funcs)
async def ThreadName(id: int = None, *args, **kwargs):
    context = utils.ContextAmisynth()  # ← si es una clase asíncrona (ajústalo si no lo es)

    obj_bot = utils.bot_inst

    if id is None:
        try:
            name = context.thread_name
        except AttributeError:
            return None
    else:
        thread = await obj_bot.fetch_channel(id)  # ← faltaba el await
        name = thread.name

    return name
