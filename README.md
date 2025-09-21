# Project Raven Squad – Reverse Engineering

join our discord [Project-RavenSquad](https://discord.gg/TN8BgX4xy5)

## Overview
**Raven Squad: Operation Hidden Dagger** is a tactical first-person shooter and real-time strategy hybrid released in 2009 for Windows and Xbox 360. Players control an elite mercenary team navigating hostile environments with a mix of squad-based tactics and direct combat. Each squad member has unique abilities, and players can seamlessly switch between first-person action and top-down tactical command, offering a dynamic strategic gameplay experience.

This repository is dedicated to **reverse engineering and analyzing Raven Squad**.  
It focuses on understanding the game’s file formats, extracting game assets, and documenting the internal systems.  
Included are:
- Python tools for extracting and analyzing `.slot` files.  
- Decompressed textures (as `.dds`) and configuration data (plain text).  
- Documentation of file formats, internal structures, and mission data.  
- Organized folder structure for storing extracted assets and logs.  

The goal is to provide a structured framework for research, modding, and educational purposes.

---

## Project Goals
The goal of this project is to provide a structured toolkit for researching and understanding Raven Squad’s game files, including:
- Extracting assets from `.slot` files.
- Understanding file structure and compression.
- Creating a reference for modding or educational purposes.
- Developing scripts and tools to assist further analysis or game modification.

---

## Important Notes
- This repository does **not** include any copyrighted game files.
- Users must own a legal copy of Raven Squad to use the extraction tools.
- This project is intended for research, educational, and modding purposes only.

---

## Attribution
- Python scripts were originally generated with OpenAI’s ChatGPT to extract data from zlib-compressed containers.

---

## Notes on `.slot` Files
1. Many game data are in `.slot` files such as:
   - Textures (e.g., mission assets, main menu backgrounds)  
   - Configuration data (human-readable text format)  
   - Some data not yet identified, currently saved as `.bin`  
2. The project is just starting, and there is no confirmed information about the game engine yet.

---

## Example Extracted Config

Here is a sample of configuration data extracted from a `.slot` file:

```plaintext
[: cHelicopterBase]
{
    _RefID = 1
    StringID = "uh60_rs_spline"
    BaseId_ = "DEIMOSS-1236089170-451301101"
    ParentName = ""
    EditorHierarchyPath = "Vehicles"
    ModelName = "gfx/objects/vehicles/uh60/uh_60.drs"
    ModelMaterialLOD = 10, 12
    Name = "#iHOTSPOT_NAME_ENEMY_HELICOPTER#"
    Scale = 1, 1, 1
    Team = 0
    Collide = 1
    CastShadow = 1
    ReceiveShadow = 1
    DetectionDuration = 100
    LastSeenEffectName = "gw_unit_hide"
    TPS_Offset = 0, 0, 5
    TPS_Distance = 10
}
```
Observations:
- Each block starts with [: cClassName], defining an entity type.
- Inside { ... } are key/value pairs (numbers, strings, or comma-separated lists).
- ModelName points to game assets like .drs (3D models).
- Likely represents objects/actors in missions, with properties for AI, collisions, and rendering.
- This shows how objects, models, and gameplay properties are defined inside the game files.

More examples will be added as additional .slot content is documented.
