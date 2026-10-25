# 🏹 Happy Dussehra (Vijayadashami) Cinematic Animation

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame-CE](https://img.shields.io/badge/Engine-Pygame--CE%20%7C%20Turtle-orange.svg?logo=pygame&logoColor=white)](https://pyga.me/)
[![NumPy Audio DSP](https://img.shields.io/badge/Audio-Procedural%20NumPy%20DSP-013243.svg?logo=numpy&logoColor=white)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Resolution](https://img.shields.io/badge/Display-High--DPI%2060%20FPS-gold.svg)](#)

> **"यतो धर्मस्ततो जयः"** — *Where there is Dharma, there is Victory.*

An authentic, standalone, high-fidelity Python cinematic experience celebrating **Dussehra (Vijayadashami)** — the cosmic triumph of Lord Rama over the ten-headed demon king Ravana and the traditional burning of the Ravana effigy (*Ravana Dahan*).

---

![Happy Dussehra Climax Greeting](screenshots/07_happy_dussehra_greeting.png)

---

## 🌟 Highlights

- **Dual Rendering Engines**: 
  - **High-Performance 60 FPS Pygame Engine** (default) with bloom glow, particle physics, screen shake, and smooth High-DPI scaling.
  - **Zero-Dependency Vector Turtle Engine** (`--turtle`) using standard library Python for universal compatibility.
- **Pure Procedural Audio Synthesis (NumPy DSP)**: Generates all sound effects in real time — conch shell (*Shankha*), bowstring tension, fiery arrow launch, sub-bass Brahmastra impact, rolling effigy firecrackers (*Ladi*), temple bells (*Ghanta*), and meditative *Tambura* drone — **no external audio assets required**!
- **Hand-Crafted 2D Vector Characters**:
  - **Lord Rama**: Athletic Kshatriya archer silhouette, Megha-shyam (raincloud-blue) skin, muscular contouring, golden Pitambara dhoti with saffron borders, sacred *Yajnopavita* thread, *Kirita-mukut* crown with iridescent peacock feather (*Mayura Pankha*), serene lotus eyes, and the golden *Kodanda* bow with dynamic string deflection.
  - **King Ravana (Dashanana)**: Ten individually crowned heads arranged in a majestic crescent arch, fierce warrior expressions, antique embossed gold breastplate featuring a 12-beam solar disc and ruby, and dual articulated arms wielding the celestial *Chandrahas* sword and spiked *Gada* (mace).
- **Four-Stage Staged Effigy Demolition**:
  1. Blinding impact shockwave, navel armor breach, and molten fissures.
  2. Spreading fire across the effigy accompanied by cracking firecracker bursts.
  3. Sequential head detonation: all 10 heads detach and tumble with independent 2D kinematics (gravity, velocity, rotational spin) and explode on ground impact.
  4. Structural collapse of the wooden bamboo frame into a roaring celebratory bonfire.
- **Grand Festive Finale**: Multi-tier aerial fireworks barrages, ground Anaar spark fountains, illuminated floating sky lanterns (*Kandils*), celestial flower shower (*Pushpa Vrishti*), and radiant 3D beveled golden greeting banner.

---

## 📸 Cinematic Gallery

| 1. Deep Midnight Sanctum & Temple | 2. Lord Rama Drawing the Kodanda Bow |
| :---: | :---: |
| ![Intro](screenshots/01_night_sanctum_intro.png) | ![Rama Aim](screenshots/02_lord_rama_drawing_bow.png) |
| *Grand Dravidian/Nagara temple shikharas, flickering diyas & moonlit terrace.* | *Dynamic bowstring tension, muscle contouring & radiant Prabhamandala aura.* |

| 3. Brahmastra Arrow in Ballistic Flight | 4. Ravana Effigy Ablaze & Crackers Detonating |
| :---: | :---: |
| ![Brahmastra](screenshots/03_brahmastra_flight.png) | ![Burning Effigy](screenshots/04_ravana_effigy_burning.png) |
| *Parabolic trajectory with helical energy rings & trailing exhaust sparks.* | *Molten fissures, cracker pops & detached heads tumbling with gravity.* |

| 5. Bamboo Frame Collapse & Sky Lanterns | 6. Festive Aerial Fireworks Climax |
| :---: | :---: |
| ![Bonfire](screenshots/05_bonfire_and_sky_lanterns.png) | ![Fireworks](screenshots/06_festive_fireworks_climax.png) |
| *Permanent bonfire bed, floating glowing Kandils & smoke dissipation.* | *Multi-spectral shell bursts, sparkling Anaar fountains & festive embers.* |

---

## 🎮 Interactive Controls

| Key | Action | Description |
| :---: | :---: | :--- |
| `[SPACE]` | **Replay Animation** | Resets the entire sequence from INTRO, clearing all particles and audio for a fresh experience. |
| `[F]` | **Toggle Fullscreen** | Switches smoothly between native High-DPI Fullscreen and a 16:10 windowed mode. |
| `[S]` | **Cinematic Slow-Mo** | Toggles 0.35x slow-motion playback to observe projectile dynamics, head detachment, and particle details. |
| `[P]` | **Pause / Resume** | Freezes simulation time with an elegant golden pause overlay. |
| `[M]` | **Mute / Unmute** | Toggles the procedural sound engine and ambient sacred drone. |
| `[ESC]` | **Exit** | Gracefully cleans up mixer channels and closes the application. |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Windows, macOS, or Linux

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/addagatlasricharan/dussehra-animation.git
   cd dussehra-animation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Or manually install: `pip install pygame-ce numpy pillow`)*

### Execution

- **Run High-Fidelity Cinematic Engine (Recommended)**:
  ```bash
  python happy_dasara.py
  ```
  *or with full script name:*
  ```bash
  python "Happy Dussehra Animation.py"
  ```

- **Run Lightweight Turtle Fallback Engine**:
  ```bash
  python happy_dasara.py --turtle
  ```

- **Generate Documentation Screenshots Headlessly**:
  ```bash
  python capture_screenshots.py
  ```

---

## 🔬 Technical Architecture & Math

### 1. Procedural DSP Audio Engine (`ProceduralAudioEngine`)
All sound waves are computed directly as NumPy arrays (44.1 kHz, 16-bit signed stereo):
- **Bow Draw**: Linear chirp frequency sweep $f(t) \in [70\text{Hz}, 240\text{Hz}]$ modulated by stochastic tension noise.
- **Brahmastra Launch**: Instantaneous transient attack with decaying odd/even harmonics ($560\text{Hz}, 840\text{Hz}$) + turbulence noise.
- **Brahmastra Impact**: Descending exponential sub-bass sweep ($130\text{Hz} \to 25\text{Hz}$) combined with low-frequency rumble ($42\text{Hz}$) and a randomized crackle tail.
- **Victory Conch (*Shankha*)**: Non-linear additive harmonic series ($f_0 \approx 220\text{Hz}$) with acoustic breath noise:
  $$S(t) = \left(\sum_{k=1}^5 A_k \sin(k \cdot \phi(t))\right) \cdot E_{\text{breath}}(t)$$
- **Temple Bell (*Ghanta*)**: Bell acoustics with non-harmonic chime partials and exponential envelope decay:
  $$B(t) = \sum_{i} A_i \sin(2\pi f_i t) e^{-d_i t}$$
- **Sacred Tambura Bed**: Continuous Sa-Pa-Sa drone ($130.81\text{Hz}, 196.00\text{Hz}, 261.63\text{Hz}$) with micro-phase oscillation and seamless loop cross-fading.

### 2. Projectile Dynamics & Tangent Derivative
The Brahmastra traverses a parametric arc:
$$X(t) = X_{\text{start}} (1 - \tau) + X_{\text{target}} \tau$$
$$Y(t) = Y_{\text{start}} (1 - \tau) + Y_{\text{target}} \tau - h \sin(\pi \tau)$$
The arrow's visual orientation is locked to the analytical tangent angle:
$$\theta(t) = \operatorname{atan2}\left(\frac{dY}{dt}, \frac{dX}{dt}\right) = \operatorname{atan2}\left( (Y_{\text{target}} - Y_{\text{start}}) - \pi h \cos(\pi \tau), X_{\text{target}} - X_{\text{start}} \right)$$

### 3. Effigy Head Detachment Kinematics
Severed heads are simulated as independent rigid bodies with gravitational acceleration:
$$v_y(t + \Delta t) = v_y(t) + g \cdot \Delta t \quad (g = 380\text{ px/s}^2)$$
$$\theta_{\text{head}}(t + \Delta t) = \theta_{\text{head}}(t) + \omega \cdot \Delta t$$
Upon crossing the ground rampart ($Y \ge 540$), they detonate in a burst of colored firecracker sparks.

---

## 📁 Repository Structure

```
dussehra-animation/
├── Happy Dussehra Animation.py  # Primary cinematic dual-engine source code
├── happy_dasara.py              # Convenient CLI launcher script
├── capture_screenshots.py       # Headless automated screenshot generator
├── requirements.txt             # Python package dependencies
├── .gitignore                   # Git ignore file
├── LICENSE                      # MIT Open Source License
├── README.md                    # Project presentation & documentation
└── screenshots/                 # High-resolution animation snapshots
    ├── 01_night_sanctum_intro.png
    ├── 02_lord_rama_drawing_bow.png
    ├── 03_brahmastra_flight.png
    ├── 04_ravana_effigy_burning.png
    ├── 05_bonfire_and_sky_lanterns.png
    ├── 06_festive_fireworks_climax.png
    └── 07_happy_dussehra_greeting.png
```

---

## 📜 Cultural Context & Lore

**Vijayadashami** (also known as *Dussehra*) marks the victory of **Lord Rama** over the demon king **Ravana** of Lanka, signifying the eternal triumph of righteousness (*Dharma*) over wickedness (*Adharma*), light over darkness, and truth over deceit. In cities and villages across India, towering effigies of Ravana filled with festive firecrackers are ceremonially shot by an actor playing Lord Rama with a flaming arrow, culminating in a celebration with fireworks, sweets, and the exchange of auspicious Shami leaves.

---

## 📄 License

This project is open-source and released under the [MIT License](LICENSE).  
Developed with devotion and artistic craftsmanship by **Sri Charan Addagatla**.

**May the divine blessings of Lord Rama bring courage, wisdom, and victory into your life! Happy Dussehra!**
