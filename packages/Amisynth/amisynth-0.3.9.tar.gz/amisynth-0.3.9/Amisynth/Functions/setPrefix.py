
import xfox
import discord
import Amisynth.utils as utils

@xfox.addfunc(xfox.funcs)
async def setPrefix(prefix, guild_id:int=None, *args, **kwargs):
    context = utils.ContextAmisynth()
    selft = utils.bot_inst
    if prefix is None:

        raise ValueError(f"Especifica el prefix, `$setPrefix[?;..]` vacio.")
    
    if guild_id is None:
        guild_id=context.guild_id
    selft.set_prefijo_servidor(guild_id, prefix)
    return "" 