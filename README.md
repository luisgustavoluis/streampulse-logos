# StreamPulse · logos de canales

StreamPulse lee `logos.json` de este repositorio y da a cada canal de tus listas su logo **sin que tengas que
cargarlo a mano**. Funciona con cualquier lista: el emparejamiento se hace por el nombre del canal, siempre
**exacto**: «ESPN» nunca toma el logo de «ESPN 2».

## De dónde salen los logos

1. **Los tuyos**, en `logos/<país>/`. Mandan sobre los demás.
2. [tv-logo/tv-logos](https://github.com/tv-logo/tv-logos), fijado a un commit (`sources.json`), así sus URLs no
   cambian nunca. Son PNG con transparencia. Los tuyos se sirven por commit: si reemplazás uno, la app baja el nuevo.

Países incluidos: `spain`, `argentina`, `mexico`, `chile`, `united-states`, `world-latin-america`, `international`.

## Agregar un logo que falta (desde el navegador, sin instalar nada)

Abrí el enlace de subida del país (con tu sesión de GitHub iniciada) y arrastrá el PNG:

| País | Subir aquí |
|---|---|
| España | https://github.com/luisgustavoluis/streampulse-logos/upload/main/logos/spain |
| Argentina | https://github.com/luisgustavoluis/streampulse-logos/upload/main/logos/argentina |
| México | https://github.com/luisgustavoluis/streampulse-logos/upload/main/logos/mexico |
| Latinoamérica | https://github.com/luisgustavoluis/streampulse-logos/upload/main/logos/world-latin-america |
| EE. UU. | https://github.com/luisgustavoluis/streampulse-logos/upload/main/logos/united-states |
| Chile | https://github.com/luisgustavoluis/streampulse-logos/upload/main/logos/chile |
| Internacional | https://github.com/luisgustavoluis/streampulse-logos/upload/main/logos/international |

1. El PNG, **con transparencia**, se llama como el canal, en minúsculas, con guiones y el sufijo del país:
   `canal-catorce-mx.png`, `espn-2-ar.png`, `teledeporte-es.png`.
   Sufijos: `es`, `ar`, `mx`, `cl`, `us`, `lam` (Latinoamérica), `int` (internacional).
2. Abajo, **Commit changes**. En un minuto la acción *Regenerar logos.json* actualiza el índice sola.
3. Abrí StreamPulse dos veces (la primera baja el índice nuevo; GitHub puede tardar hasta 5 minutos en servirlo).

(En la carpeta del país, el mismo menú está arriba a la derecha como **Add file › Upload files**; en pantallas
estrechas queda dentro del botón **…**. La app móvil de GitHub no permite subir archivos: usá el navegador.)

En la guía, StreamPulse pinta en blanco los logos de un solo color (negros, azul oscuro, rojos…) para que se vean
sobre el fondo oscuro; los que tienen detalle blanco propio (DAZN, Telecinco, TV3) conservan sus colores.

**Si un logo de tv-logos está mal**, subí el tuyo con el **mismo nombre de archivo** en la misma carpeta: el tuyo
lo reemplaza.

## El canal se llama distinto en tu lista

El nombre del archivo es un nombre; si tu lista usa otro, agregá alias en `aliases.json`:

```json
"spain/tve-1-es.png": ["La 1", "TVE 1", "TVE La 1"]
```

No hace falta escribir las variantes de calidad o prefijos: la app ya ignora mayúsculas, acentos, `HD`, `SD`,
`FHD`, `UHD`, `4K`, `RAW`, `VIP`, `ᴴᴰ`, `(Ciudad)`, `delay…` y prefijos como `ES:`, `MX|`, `VIP:`.
Los **números sí cuentan**: «ESPN», «ESPN 2» y «ESPN 3» son canales distintos.

## Qué logo gana

1. El logo que pongas a mano en las opciones del canal en StreamPulse.
2. El de este repositorio.
3. El que trae la lista.
4. Las iniciales.

Si un nombre coincide con canales de varios países, se elige el del país de la lista (`ES|`, `LA| ARGENTINA`…), y
si no se puede saber, **no se pone ninguno**: mejor sin logo que con uno equivocado.

## Regenerar a mano

```sh
GITHUB_TOKEN=$(gh auth token) python3 tools/build_index.py
```
