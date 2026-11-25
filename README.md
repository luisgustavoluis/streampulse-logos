# StreamPulse · logos de canales

StreamPulse lee `logos.json` de este repositorio y da a cada canal de tus listas su logo **sin que tengas que
cargarlo a mano**. Funciona con cualquier lista: el emparejamiento se hace por el nombre del canal (y por
`tvg-id` cuando lo hay), siempre **exacto**: «ESPN» nunca toma el logo de «ESPN 2».

## De dónde salen los logos

1. **Los tuyos**, en `logos/<país>/`. Mandan sobre los demás.
2. [tv-logo/tv-logos](https://github.com/tv-logo/tv-logos), fijado a un commit (`sources.json`), así sus URLs no
   cambian nunca. Son PNG con transparencia.

Países incluidos: `spain`, `argentina`, `mexico`, `chile`, `united-states`, `world-latin-america`, `international`.

## Agregar un logo que falta (desde la web de GitHub, sin instalar nada)

1. Entrá en la carpeta del país, por ejemplo `logos/mexico/`, y pulsá **Add file › Upload files**.
2. Subí un **PNG con transparencia** llamado como el canal, en minúsculas, con guiones y el sufijo del país:
   `canal-catorce-mx.png`, `espn-2-ar.png`, `teledeporte-es.png`.
   Sufijos: `es`, `ar`, `mx`, `cl`, `us`, `lam` (Latinoamérica), `int` (internacional).
3. **Commit**. En un minuto la acción *Regenerar logos.json* actualiza el índice solo.

StreamPulse lo descarga al arrancar: la próxima vez que abras la app, el canal ya tiene su logo.

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
