# 🥣 Cerealicious Profile & Design System Preferences

This document records the aesthetic preferences, design tokens, technical specifications, and iterative roadmap established for **cerealicious**. It serves as our shared design log so we can iterate on the profile together.

---

## 🎨 1. Aesthetic & Brand Foundations

* **Core Aesthetic:** **Anti-Gravity / Zero-G Cereal Bar**
  * Simple, breathable, and uncluttered layout with generous vertical whitespace.
  * Floating cards, subtle rounded borders, and clean monospace accents.
  * Balanced contrast: looks natural in both GitHub Dark Mode (`#0D1117`) and Light Mode (`#FFFFFF`).
* **Tone & Persona:**
  * **Role:** Student developer & IT systems support specialist.
  * **Vibe:** Playful, approachable, and technically capable. Doesn't take themselves too seriously (e.g., measuring "patience with printers" and "DNS troubleshooting" in the Nutrition Facts).
  * **Focus Areas:**
    1. IT Support & Systems Administration (PowerShell, Active Directory, network debugging).
    2. Student Hubs & Campus Portals (accessible, clean web pages for peers).
    3. Freelance Web Development & Personal Runbooks.
* **Primary IDE:** **Visual Studio** / **VS Code**.

---

## 🌈 2. Color Palette & Design Tokens

Inspired by classic breakfast cereals (Froot Loops & Lucky Charms marshmallows) suspended against a clean slate chassis:

| Flavor Token | Hex Code | Role / Usage |
| :--- | :--- | :--- |
| **Berry Crunch (Pink)** | `#FF6B8B` | Primary highlights, accent buttons, curiosity badge |
| **Golden Puff / Honey (Yellow)** | `#FFB84D` | Zero-G status indicators, underglow accents, warm tags |
| **Crisp Lime (Green)** | `#6BCB77` | Code quality badges, successful ping indicators |
| **Blueberry Sky (Blue)** | `#4D96FF` | Network badges, IT support, LinkedIn buttons |
| **Grape Violet (Purple)** | `#9B5DE5` | Discord, Astro, creative flair |
| **Citrus Tangerine (Orange)** | `#FF9100` | Warning tags, HTML5, energetic accents |
| **Milk Cream (Marshmallow)** | `#F0F6FC` | High-contrast legends, keycap labels, light text |
| **Deep Chassis Slate** | `#161B22` | Card backgrounds, keyboard chassis body |
| **Outer Space Slate** | `#0D1117` | Transparent canvas background, GitHub dark match |
| **Subtle Border** | `#30363D` | Crisp card borders, table dividers |

---

## ⌨️ 3. Animated Header Specs

The repository includes **two complementary implementations** of the animated header:

### A. Python-Rendered Animated GIF (`assets/header.gif`)
* **Generator Script:** `scripts/generate_animated_header.py`
* **Resolution:** $840 \times 300\text{ px}$, 25 FPS, 83 frames.
* **Physics Engine:** Simulates 3D mechanical keycap displacement ($-5\text{px}$) with actuated LED underglow. Spawns 3–5 zero-gravity cereal loops and marshmallow puffs on every letter press. Particles burst upward with initial velocity $v_y \in [-4.5, -9.5]$ and float in micro-gravity ($g = 0.16$).
* **Why GIF?** 100% universal compatibility across GitHub Desktop, GitHub Mobile app, and light/dark theme switches without SVG script blocking.

### B. Pure Vector Animated SVG (`assets/header.svg`)
* **Resolution:** Scalable vector viewBox `0 0 840 300`.
* **Engine:** Pure CSS `@keyframes` (`zeroGBob`, `pressKey`, `popBurst1-3`).
* **Why SVG?** Infinite crisp resolution, lightweight footprint (~15 KB), zero pixelation on Retina/4K displays.

---

## 🛠️ 4. How to Iterate & Customize

### 1. Regenerating the Animated Header (Python)
To modify typing speed, letter sequence, or add more cereal particles:
```powershell
# In Visual Studio Terminal / PowerShell:
py scripts/generate_animated_header.py
```
Key configurable variables in `scripts/generate_animated_header.py`:
* `TEXT = "cerealicious"`: Change the typed string.
* `KEY_INTERVAL = 4`: Keystroke spacing (lower = faster typing).
* `POST_TYPE_HOLD = 35`: Pause before the animation loops.
* `CEREAL_COLORS`: Add or replace color hex codes.

### 2. Updating Nutrition Facts (`README.md`)
The Nutrition Facts panel is defined in the `## 🥣 Nutrition Facts` block using a monospace ASCII/Unicode box:
* Edit the `% Daily Val*` column to adjust fun skills (e.g., *Cable Management*, *Printer Whisperer*).
* Edit the *Fortified Vitamins* list to highlight new certifications (CompTIA, Azure, Cisco).

### 3. Adding New Ingredients / Badges
All shields follow a unified flat-square aesthetic:
```markdown
<img src="https://img.shields.io/badge/Tech_Name-HEXCOLOR?style=flat-square&logo=logoname&logoColor=white" alt="Tech" />
```

---

## 📋 5. Future Iteration Checklist
- [ ] Connect real URLs to the project cards in `README.md`.
- [ ] Add real email address / social handles to `🥛 Pour Yourself a Bowl`.
- [ ] Add a GitHub Stats card with custom cereal palette themes (optional).
- [ ] Embed personal study hub web links as they launch.

