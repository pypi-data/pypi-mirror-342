import xfox
import discord
import Amisynth.utils as utils
@xfox.addfunc(xfox.funcs)
async def username(id: str = None, *args, **kwargs):
    context = utils.ContextAmisynth()
    if id is None:
        username  = context.username
    else:
        username = context.get_username_by_id(int(id))

    return username
