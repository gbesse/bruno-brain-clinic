# Bruno Brain Clinic

[Français](README.md) · [English](README.en.md)

Un verificador **local y de solo lectura** para exportaciones Markdown de memoria de agentes, incluido [Bruno Brain](https://get-bruno.com/fr/tech). Señala páginas sin fuente, conocimientos caducados, ciertos patrones de secretos y valores contradictorios que comparten explícitamente un fact_key. El informe no contiene valores de hechos ni secretos detectados.

El directorio skills/brain-clinic contiene una habilidad reutilizable para ejecutar esta revisión local.

## Probar

    python3 -m pip install -r requirements.txt
    python3 brain_clinic.py RUTA_EXPORTACION --lang es
    python3 -m unittest discover -s tests -v

Los metadatos son YAML entre dos líneas --- al principio del archivo Markdown. Esta versión comprende sources o source, stale_after en formato YYYY-MM-DD, y los campos opcionales fact_key y fact_value para comparar hechos. El programa lee todos los archivos .md del directorio y genera JSON. Códigos de salida: 0 sin hallazgos, 2 revisión necesaria, 1 entrada no válida. Los mensajes están disponibles en francés, inglés y español.

Bruno anuncia la exportación de su cerebro en Markdown u OKF. Este repositorio trabaja con archivos Markdown exportados; no se conecta a Bruno ni valida toda la especificación OKF. Solo detecta contradicciones identificadas explícitamente por fact_key, no discrepancias semánticas. Revise los hallazgos antes de corregirlos.

Licencia MIT.
