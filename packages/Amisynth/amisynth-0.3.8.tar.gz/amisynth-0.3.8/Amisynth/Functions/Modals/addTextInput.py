import xfox
import Amisynth.utils as utils
from discord.ui import TextInput, TextInputStyle

@xfox.addfunc(xfox.funcs)
async def addTextInput(
    input_id: str,
    style: str,
    label: str,
    min_length: int = None,
    max_length: int = None,
    required: str = "yes",  # Acepta 'yes' o 'no'
    value: str = None,
    placeholder: str = None,
    *args, **kwargs
):
    # Validaciones de parámetros
    print(f"[DEBUG ADDTEXTINPUT] Verificando parámetros: label={label}, style={style}, min_length={min_length}, max_length={max_length}, required={required}, value={value}, placeholder={placeholder}")
    
    if len(label) > 45:
        print("[DEBUG ADDTEXTINPUT] Error: El label tiene más de 45 caracteres.")
        return "El label no puede tener más de 45 caracteres."
    
    # Validar estilo: 'short' -> singleline, 'paragraph' -> multiline
    if style not in ["short", "paragraph"]:
        print(f"[DEBUG ADDTEXTINPUT] Error: El estilo '{style}' no es válido.")
        return "El estilo debe ser 'short' (singleline) o 'paragraph' (multiline)."
    
    # Convertir el estilo a su valor correspondiente
    style_enum = TextInputStyle.singleline if style == "short" else TextInputStyle.multiline
    print(f"[DEBUG ADDTEXTINPUT] Estilo convertido a: {style_enum}")
    
    # Validaciones de longitudes
    if min_length is not None:
        if min_length < 0 or min_length > 4000:
            print(f"[DEBUG ADDTEXTINPUT] Error: Longitud mínima {min_length} fuera de rango.")
            return "La longitud mínima debe estar entre 0 y 4000."
        print(f"[DEBUG ADDTEXTINPUT] Longitud mínima válida: {min_length}")
    
    if max_length is not None:
        if max_length < 0 or max_length > 4000 or (min_length is not None and max_length < min_length):
            print(f"[DEBUG ADDTEXTINPUT] Error: Longitud máxima {max_length} fuera de rango o menor que la mínima.")
            return "La longitud máxima debe estar entre 0 y 4000, y no puede ser menor que la longitud mínima."
        print(f"[DEBUG ADDTEXTINPUT] Longitud máxima válida: {max_length}")
    
    # Validar si es requerido
    if required not in ["yes", "no"]:
        print(f"[DEBUG ADDTEXTINPUT] Error: El parámetro 'Required?' tiene un valor inválido '{required}'.")
        return "El parámetro 'Required?' debe ser 'yes' o 'no'."

    required_bool = True if required == "yes" else False
    print(f"[DEBUG ADDTEXTINPUT] 'Required?' convertido a booleano: {required_bool}")
    
    # Crear el TextInput
    input_box = TextInput(
        custom_id=input_id,
        style=style_enum,
        label=label,
        min_length=min_length,
        max_length=max_length,
        required=required_bool,
        default=value,
        placeholder=placeholder
    )
    
    print(f"[DEBUG ADDTEXTINPUT] Input Box creado: {input_box}")

    # Agregar al modal
    modal = utils.modals
    print(f"[DEBUG ADDTEXTINPUT] Modal antes de agregar el input: {modal}")
    modal.add_item(input_box)
    print(f"[DEBUG ADDTEXTINPUT] Modal después de agregar el input: {modal}")
    
    return f"Input agregado correctamente."
