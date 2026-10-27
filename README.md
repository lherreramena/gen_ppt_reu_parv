# gen_ppt_reu_parv
Genrador de Reuniones de Apoderados de Parvulos

## Modificar una presentación

`pptx_agent.py` recibe una presentación `.pptx` como plantilla, un archivo UTF-8
con las instrucciones de cambio y la ruta para guardar una nueva presentación.
El agente solo puede reemplazar texto en formas existentes; no cambia el diseño,
las imágenes ni otras partes del archivo. Si una instrucción requiere crear una
forma, cambiar el formato o alterar el número de párrafos, no se aplicará.

Configura `OPENAI_API_KEY` y ejecuta:

```sh
python pptx_agent.py --template plantilla.pptx --changes cambios.txt --output nueva.pptx
```

Opcionalmente, configura `OPENAI_MODEL` (por defecto `gpt-4o-mini`) y
`OPENAI_BASE_URL` (por defecto `https://api.openai.com/v1`) para elegir el modelo
y el servicio compatible con la API de Chat Completions.

Las modificaciones se validan contra el texto original y se aplican solamente
a las formas identificadas por diapositiva e ID. Para ejecutar las pruebas:

```sh
python -m unittest discover -s tests
```
