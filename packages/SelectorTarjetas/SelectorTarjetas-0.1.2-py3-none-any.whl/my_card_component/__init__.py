import os
import streamlit.components.v1 as components

# Cambiar a True después de `npm run build` en frontend
_RELEASE = True

if not _RELEASE:
    # En desarrollo: servidor React en localhost:3001
    _component = components.declare_component(
        "my_card_component", url="http://localhost:3000"
    )
else:
    # En producción: usar carpeta build estática
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component = components.declare_component(
        "my_card_component", path=build_dir
    )


def card_component(cards, height=400, default="", key=None):
    """
    cards: lista de dicts con campos {
      id, name, description, value, image_url
    }
    height: altura del iframe para renderizar el componente
    default: valor seleccionado por defecto
    key: clave única de Streamlit
    """
    # Pasamos todos los argumentos al componente
    selected = _component(
        cards=cards,
        height=height,
        default=default,
        key=key,
    )
    return selected