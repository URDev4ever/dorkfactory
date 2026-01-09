<h1 align="center">dorkfactory</h1>
<p align="center">
  <img width="577" height="432" alt="image-removebg-preview (40)" src="https://github.com/user-attachments/assets/ecb08480-e1aa-436d-a6a8-7af892b38e6f" />
</p>
<h3 align="center">Dork Factory is a cross-platform, interactive command-line tool designed to generate high-quality Google and Yandex dorks for Passive Recon &amp; Discovery.</h3>

It focuses exclusively on **search engine query manufacturing**, helping security researchers uncover publicly indexed information **without actively interacting with targets**.

> No scanning. No fuzzing. No crawling.
> Just clean, structured, search-engine–ready recon.

---

## ✨ Key Features

* Interactive CLI (no flags required)
* Google & Yandex dork generation
* Recon category selection
* Preset profiles (Bug Bounty, OSINT, CTF, etc.)
* Advanced filtering & exclusions
* Clean, colorized output
* Exportable results
* Fully passive & ethical
* Windows · Linux · macOS compatible

---

## 🖥️ Interactive Mode (Default)

Running the tool without arguments launches the **interactive interface**:

```bash
python dorkfactory.py
```

This mode allows full usage **without memorizing flags**, using a menu-driven workflow.

### Main Interface

<img width="630" height="822" alt="dfmainn" src="https://github.com/user-attachments/assets/ea220395-863a-4c9d-8f6f-94ea1ae8791c" />

---

## 🎯 Target Configuration

Define one or multiple targets, including wildcards and subdomains.

<img width="625" height="160" alt="dftarget0" src="https://github.com/user-attachments/assets/f6822388-b959-424a-a36d-1ed073bff274" />

<img width="627" height="229" alt="dftarget1" src="https://github.com/user-attachments/assets/0742a9e1-95e7-49a4-9823-753cf1bc3152" />

Supported:

* `example.com`
* `*.example.com`
* Multiple targets
* Exclusions

---

## 🔍 Search Engine Selection

Choose which search engine(s) to generate dorks for:

* Google
* Yandex
* Both

<img width="627" height="195" alt="dfengine0" src="https://github.com/user-attachments/assets/2e244f97-a6d6-4a2b-a58b-725f872c1003" />


---

## 🧩 Recon Categories

Select which recon categories to include in the generation process.

<img width="623" height="351" alt="dfcategory0" src="https://github.com/user-attachments/assets/3011f121-eeca-4f70-85b7-238e142bee30" />

<img width="626" height="346" alt="dfcategory1" src="https://github.com/user-attachments/assets/2ceb5bfa-6e1c-48af-8de7-93605ca2c6ce" />


Examples:

* Panels & Authentication
* Sensitive Files & Backups
* Errors & Debug
* APIs & Endpoints
* OSINT & Metadata

---

## 📦 Preset Profiles

Profiles automatically configure engines and categories for common use cases.

Available profiles include:

* `bugbounty`
* `osint-company`
* `ctf`
* `webapp-basic`
* `cloud-recon`

<img width="625" height="246" alt="dfprofiles0" src="https://github.com/user-attachments/assets/d4b77704-1048-45aa-9de3-1d6e90cae563" />


---

## ⚙️ Advanced Options

Fine-tune the generation process with optional advanced settings.

<img width="629" height="239" alt="dfadvops" src="https://github.com/user-attachments/assets/0aa370c7-a299-49e1-8453-7b5318e55462" />


Options include:

* Noise reduction
* Strict queries
* Banner toggle
* Color output control

---

## 🧠 Dork Generation

Once configured, Dork Factory generates categorized, optimized dorks and provides **ready-to-use search URLs**.

<img width="845" height="730" alt="dfgenerated" src="https://github.com/user-attachments/assets/2ee9ab2d-b542-4928-bddf-3f3d68b15331" />


Each dork is:

* Grouped by category
* Engine-aware
* Deduplicated
* Labeled for clarity

---

## 📤 Exporting Results

Generated dorks can be exported for later use.

<img width="357" height="115" alt="dfsaveoutput" src="https://github.com/user-attachments/assets/4aaa56a4-e4ca-4079-92b4-21ab760237dc" />


Supported formats:

* `.txt`
* `.md`
* `.json`

---

## ⌨️ Flag-Based Usage (Optional)

For advanced users or scripting purposes, Dork Factory also supports flags.

```bash
python dorkfactory.py --target example.com --profile bugbounty --engine both --no-banner
```

### Common Flags

```text
-h, --help              Show help
-i, --interactive       Force interactive mode
-nb, --no-banner        Disable banner
--target                Define target(s)
--engine                google | yandex | both
--category              Select categories
--profile               Use a preset
--exclude               Exclusions
--export                Export results
--silent                Minimal output
--no-color              Disable colors
```

---

## 🛡️ Ethics & Safety

Dork Factory is designed with **passive reconnaissance principles** in mind:

* ❌ No requests sent to targets
* ❌ No crawling or scraping
* ❌ No exploitation
* ❌ No fuzzing or scanning
* ✅ Public search engine queries only

Use responsibly and only on targets you are authorized to research.

---

## 🧰 Technical Details

* **Language**: Python 3
* **Interface**: Interactive CLI (TUI-style)
* **Platforms**: Windows, Linux, macOS
* **Output**: Colorized, categorized, exportable
* **Comments**: Minimal, only where logic matters
* **Language**: Full English

---

## 🏁 Final Notes

**Dork Factory** turns search engines into structured recon tools, providing clarity, speed, and organization to passive discovery workflows.

> *Manufacturing search queries for Recon & Discovery.*

---

Made with <3 by URDev.
