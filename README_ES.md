<h1 align="center">Dork Factory</h1>
<p align="center">
  🇺🇸 <a href="README.md"><b>English</b></a> |
  🇪🇸 <a href="README_ES.md">Español</a>
</p>
<p align="center">
  <img width="577" height="432" alt="image-removebg-preview (40)" src="https://github.com/user-attachments/assets/ecb08480-e1aa-436d-a6a8-7af892b38e6f" />
</p>
<h3 align="center">
Dork Factory es una herramienta interactiva de línea de comandos, multiplataforma, diseñada para generar dorks de alta calidad para Google y Yandex orientados a Reconocimiento Pasivo y Descubrimiento.
</h3>

Se enfoca exclusivamente en la **fabricación de consultas para motores de búsqueda**, ayudando a investigadores de seguridad a descubrir información indexada públicamente **sin interactuar activamente con los objetivos**.

> Sin escaneo. Sin fuzzing. Sin crawling.
> Solo recon limpio, estructurado y listo para buscadores.

---

## ✨ Características Clave

* CLI interactiva (no requiere flags)
* Generación de dorks para Google y Yandex
* Selección de categorías de recon
* Perfiles predefinidos (Bug Bounty, OSINT, CTF, etc.)
* Filtros avanzados y exclusiones
* Salida limpia y colorizada
* Resultados exportables
* Totalmente pasivo y ético
* Compatible con Windows · Linux · macOS

---

## 🖥️ Modo Interactivo (Por Defecto)

Ejecutar la herramienta sin argumentos inicia la **interfaz interactiva**:

```bash
python dorkfactory.py
```

Este modo permite usar todas las funciones **sin memorizar flags**, mediante un flujo guiado por menús.

### Interfaz Principal

<img width="630" height="822" alt="dfmainn" src="https://github.com/user-attachments/assets/ea220395-863a-4c9d-8f6f-94ea1ae8791c" />

---

## 🎯 Configuración del Objetivo

Definí uno o varios objetivos, incluyendo comodines y subdominios.

<img width="625" height="160" alt="dftarget0" src="https://github.com/user-attachments/assets/f6822388-b959-424a-a36d-1ed073bff274" />

<img width="627" height="229" alt="dftarget1" src="https://github.com/user-attachments/assets/0742a9e1-95e7-49a4-9823-753cf1bc3152" />

Soportado:

* `example.com`
* `*.example.com`
* Múltiples objetivos
* Exclusiones

---

## 🔍 Selección del Motor de Búsqueda

Elegí para qué motor(es) generar los dorks:

* Google
* Yandex
* Ambos

<img width="627" height="195" alt="dfengine0" src="https://github.com/user-attachments/assets/2e244f97-a6d6-4a2b-a58b-725f872c1003" />

---

## 🧩 Categorías de Reconocimiento

Seleccioná qué categorías incluir en el proceso de generación.

<img width="623" height="351" alt="dfcategory0" src="https://github.com/user-attachments/assets/3011f121-eeca-4f70-85b7-238e142bee30" />

<img width="626" height="346" alt="dfcategory1" src="https://github.com/user-attachments/assets/2ceb5bfa-6e1c-48af-8de7-93605ca2c6ce" />

Ejemplos:

* Paneles y Autenticación
* Archivos Sensibles y Backups
* Errores y Debug
* APIs y Endpoints
* OSINT y Metadatos

---

## 📦 Perfiles Predefinidos

Los perfiles configuran automáticamente motores y categorías para casos de uso comunes.

Perfiles disponibles:

* `bugbounty`
* `osint-company`
* `ctf`
* `webapp-basic`
* `cloud-recon`

<img width="625" height="246" alt="dfprofiles0" src="https://github.com/user-attachments/assets/d4b77704-1048-45aa-9de3-1d6e90cae563" />

---

## ⚙️ Opciones Avanzadas

Ajustá el proceso de generación con configuraciones opcionales.

<img width="629" height="239" alt="dfadvops" src="https://github.com/user-attachments/assets/0aa370c7-a299-49e1-8453-7b5318e55462" />

Opciones incluidas:

* Reducción de ruido
* Consultas estrictas
* Activar / desactivar banner
* Control de salida con colores

---

## 🧠 Generación de Dorks

Una vez configurado, Dork Factory genera dorks optimizados y categorizados, junto con **URLs de búsqueda listas para usar**.

<img width="845" height="730" alt="dfgenerated" src="https://github.com/user-attachments/assets/2ee9ab2d-b542-4928-bddf-3f3d68b15331" />

Cada dork es:

* Agrupado por categoría
* Adaptado al motor de búsqueda
* Sin duplicados
* Etiquetado para mayor claridad

---

## 📤 Exportación de Resultados

Los dorks generados pueden exportarse para uso posterior.

<img width="357" height="115" alt="dfsaveoutput" src="https://github.com/user-attachments/assets/4aaa56a4-e4ca-4079-92b4-21ab760237dc" />

Formatos soportados:

* `.txt`
* `.md`
* `.json`

---

## ⌨️ Uso con Flags (Opcional)

Para usuarios avanzados o automatización, Dork Factory también soporta flags.

```bash
python dorkfactory.py --target example.com --profile bugbounty --engine both --no-banner
```

### Flags Comunes

```text
-h, --help              Mostrar ayuda
-i, --interactive       Forzar modo interactivo
-nb, --no-banner        Desactivar banner
--target                Definir objetivo(s)
--engine                google | yandex | both
--category              Seleccionar categorías
--profile               Usar un perfil
--exclude               Exclusiones
--export                Exportar resultados
--silent                Salida mínima
--no-color              Desactivar colores
```

---

## 🛡️ Ética y Seguridad

Dork Factory está diseñado bajo principios de **reconocimiento pasivo**:

* ❌ No envía requests a los objetivos
* ❌ No hace crawling ni scraping
* ❌ No explota vulnerabilidades
* ❌ No realiza fuzzing ni scanning
* ✅ Solo consultas públicas a motores de búsqueda

Usalo de forma responsable y únicamente sobre objetivos que estés autorizado a investigar.

---

## 🧰 Detalles Técnicos

* **Lenguaje**: Python 3
* **Interfaz**: CLI interactiva (estilo TUI)
* **Plataformas**: Windows, Linux, macOS
* **Salida**: Colorizada, categorizada, exportable
* **Comentarios**: Mínimos, solo donde la lógica lo requiere
* **Idioma**: Inglés completo

---

## ⭐ Contribuir

Las pull requests son bienvenidas si:

* Mejoran la lógica de generación de dorks, la calidad de las consultas o la compatibilidad con motores de búsqueda (Google / Yandex)
* Mejoran el flujo interactivo, la claridad de la experiencia o los formatos de exportación sin sobrecomplicar la interfaz
* Mantienen la filosofía completamente pasiva de la herramienta (sin scraping, sin crawling, sin interacción activa con los targets)

---

## 🏁 Notas Finales

**Dork Factory** convierte los motores de búsqueda en herramientas de recon estructurado, aportando claridad, velocidad y organización a flujos de descubrimiento pasivo.

> *Fabricando consultas de búsqueda para Reconocimiento y Descubrimiento.*

---

Hecho con <3 por **URDev**.
