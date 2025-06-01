
# 📚 Datos de Reglas de MTG y Embeddings

Este directorio contiene el texto completo de las reglas de *Magic: The Gathering* y los archivos de índice semántico utilizados por el endpoint `/ask_rule` del backend de Aethermind.

---

## 📁 Estructura

```
data/
├── rules\_raw/
│   └── MagicCompRules.txt      # Texto completo de las reglas oficiales
├── embeddings/
│   ├── faiss.index             # Índice semántico FAISS generado desde los chunks
│   └── chunks.pkl              # Lista serializada de fragmentos de reglas

```

---

## 📝 Archivo de reglas: `MagicCompRules.txt`

Puedes descargar el archivo oficial de reglas desde la página de Wizards of the Coast:

🔗 https://magic.wizards.com/en/rules

Colócalo en el siguiente directorio:

```

data/rules\_raw/MagicCompRules.txt

````

Asegúrate de que el archivo sea texto plano, esté limpio y sin modificaciones.

---

## ⚙️ Cómo construir el índice semántico

Una vez tengas el archivo en su lugar, ejecuta el script de construcción de índice desde la raíz del backend:

```bash
source venv/bin/activate
python build_index.py
````

Esto hará lo siguiente:

* Dividirá el texto de reglas en fragmentos (chunks)
* Generará embeddings semánticos usando un modelo de `sentence-transformers`
* Creará un índice FAISS para búsqueda semántica rápida
* Guardará los resultados en `data/embeddings/`

---

## ❗ Notas importantes

* Si actualizas el archivo de reglas, debes volver a ejecutar `build_index.py` para regenerar el índice.
* Por defecto se utiliza el modelo `all-MiniLM-L6-v2` de sentence-transformers.
* Este índice es utilizado por el backend para responder preguntas en el endpoint `/ask_rule`.

