import xfox
import discord
import Amisynth.utils as utils
@xfox.addfunc(xfox.funcs)
async def botID(*args, **kwargs):
    from Amisynth.utils import bot_inst
    return bot_inst.user.id