"""
================================================================================
HAPPY DASARA / VIJAYADASHAMI - CINEMATIC ANIMATION & EPIC SIMULATION
================================================================================
A high-fidelity, standalone, dual-engine Python application celebrating
Vijayadashami (Dussehra) - The Cosmic Victory of Dharma over Adharma
(Lord Rama vanquishing King Ravana and the ceremonial burning of the effigy).

--------------------------------------------------------------------------------
ARCHITECTURE OVERVIEW:
--------------------------------------------------------------------------------
1. Coordinate System & Resolution:
   - Internal Virtual Canvas: 1280 x 800 (16:10 aspect ratio).
   - High-DPI Scaling: Automatically enables per-monitor DPI awareness on Windows
     and smoothly scales the virtual canvas to target display resolutions (e.g. 2880x1800).
   - Character Anchors: Both Lord Rama and Ravana are grounded flush upon a temple
     terrace rampart at baseline Y = 556.

2. Procedural Sound Synthesizer (NumPy DSP):
   - Completely standalone digital audio synthesis using NumPy vector arrays and
     Pygame mixer channels (44.1 kHz, 16-bit stereo).
   - Requires zero external WAV/MP3 files for core sound effects!
   - Synthesizes: Bowstring tension creak (FM linear chirp), celestial arrow launch
     (transient twang + aerodynamic resonance), Brahmastra impact (descending sub-bass
     exponential sweep 130Hz -> 25Hz + rumble), fireworks whistle & bursts, rolling
     effigy crackers (Ladi), sacred conch shell (Shankha), temple bells (Ghanta),
     and a meditative Tambura drone bed (Sa-Pa-Sa harmonics).

3. Advanced Physics & Particle Systems:
   - Dynamic particle system managing fire embers, smoke plumes, sparks, and debris.
   - Sky lanterns (Kandils) with thermal buoyancy and sinusoidal horizontal draft.
   - Pushpa Vrishti (celestial flower petal rain) with 3D angular rotation and aerodynamic flutter.
   - Multi-stage ballistic fireworks rockets with exploding secondary sparkle bursts.
   - Anaar (flowerpot firecracker) cone fountains with randomized upward velocities.

4. 2D Vector Graphic Masterpieces:
   - Lord Rama: Authentic Kshatriya archer anatomy with Megha-shyam raincloud skin,
     sculpted muscle contouring, Paduka sandals, pleated golden Pitambara dhoti with
     flowing sash, sacred Yajnopavita thread, Navaratna jewelry, Kirita-mukut crown
     with iridescent peacock feather (Mayura Pankha), serene lotus eyes, Vaishnava tilak,
     and the celestial recurve Kodanda bow with dynamic string deflection.
   - King Ravana: Ten distinct heads (Dashanana) arranged in a symmetrical royal crescent,
     individual tiered golden crowns, fierce warrior brows, ruby-inlaid golden breastplate
     featuring a 12-beam solar medallion, royal crimson dhoti with gold brocade, dual
     articulated arms wielding the legendary Chandrahas scimitar and spiked Gada.

5. Four-Stage Realistic Effigy Demolition Sequence:
   - Stage 1: Solar plexus impact flash, radial shockwave, and core navel fire fissure.
   - Stage 2: Fire spreading across the torso accompanied by rapid firecracker pops.
   - Stage 3: Sequential head detonations - heads detach and tumble with independent
     gravitational acceleration, horizontal velocity, and rotational tumbling, bursting
     upon ground impact.
   - Stage 4: Structural bamboo framework collapse into a roaring celebratory bonfire.

6. Dual Engine Implementation:
   - Engine 1 (Default): High-performance 60 FPS Pygame Engine with hardware-accelerated
     alpha blending, bloom filters, and screen shake.
   - Engine 2 (Fallback): Vector Turtle / Tkinter Engine using Python standard library
     for systems without Pygame installed.

--------------------------------------------------------------------------------
REQUIREMENTS & INSTALLATION:
--------------------------------------------------------------------------------
  pip install pygame-ce numpy pillow
  (or: pip install pygame numpy pillow)

--------------------------------------------------------------------------------
EXECUTION:
--------------------------------------------------------------------------------
  python "Happy Dussehra Animation.py"           # Runs default Pygame cinematic engine
  python "Happy Dussehra Animation.py" --turtle  # Runs lightweight Turtle/Tkinter engine
  python happy_dasara.py                         # Convenient alias launcher script

--------------------------------------------------------------------------------
INTERACTIVE CONTROLS:
--------------------------------------------------------------------------------
  [SPACE]     Replay full animation sequence (from INTRO to GREETING)
  [F]         Toggle Fullscreen / Windowed mode
  [S]         Toggle Slow-Motion mode (0.35x speed for cinematic detail)
  [P]         Pause / Resume animation
  [M]         Mute / Unmute audio effects & ambient drone
  [ESC]       Exit application
================================================================================
"""

import sys
import math
import random

# ==============================================================================
# SECTION 1: GLOBAL CONFIGURATION & CONSTANTS
# ==============================================================================
WIDTH = 1280
HEIGHT = 800
DEFAULT_WINDOW_WIDTH = 2880
DEFAULT_WINDOW_HEIGHT = 1800
FPS = 60
WINDOW_TITLE = "Vijayadashami: Lord Rama Defeats Ravana - Happy Dussehra!"

# Color Palette: Traditional Indian Epic Palette
COLOR_SKY_TOP = (6, 10, 26)         # Deepest Indian midnight indigo
COLOR_SKY_MID = (16, 28, 62)        # Royal navy blue
COLOR_SKY_HORIZON = (46, 22, 42)    # Dusky earthen horizon
COLOR_GOLD_DARK = (150, 100, 15)
COLOR_GOLD = (255, 215, 0)
COLOR_GOLD_LIGHT = (255, 245, 185)
COLOR_ORANGE = (255, 120, 0)
COLOR_CRIMSON = (185, 18, 35)
COLOR_CRIMSON_DARK = (115, 10, 20)
COLOR_RAMA_BLUE = (62, 125, 205)    # Megha-shyam (celestial rain-cloud blue)
COLOR_RAMA_SHADOW = (38, 80, 145)
COLOR_RAMA_LIGHT = (100, 170, 245)
COLOR_RAVANA_SKIN = (45, 135, 85)
COLOR_RAVANA_SKIN_SHADOW = (25, 85, 52)
COLOR_RAVANA_SKIN_LIGHT = (70, 168, 110)
COLOR_TEMPLE_DARK = (16, 14, 28)
COLOR_TEMPLE_MID = (26, 22, 42)
COLOR_GROUND = (28, 18, 24)

# ==============================================================================
# SECTION 2: PROCEDURAL AUDIO SYNTHESIZER (NUMPY + PYGAME MIXER)
# Generates realistic sound effects without requiring any external audio files.
# ==============================================================================
class ProceduralAudioEngine:
    def __init__(self):
        self.enabled = False
        self.muted = False
        self.sounds = {}
        self._script_dir = ''
        try:
            import pygame
            import numpy as np
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.set_num_channels(48)
            self.np = np
            self.pygame = pygame
            self.sample_rate = 44100
            self._script_dir = sys.path[0] if sys.path and sys.path[0] else '.'
            self._synthesize_all()
            self._load_external_sounds()
            self.enabled = True
        except Exception as e:
            print(f"[AUDIO WARNING] Audio engine init failed: {e}")
            self.enabled = False

    def _make_sound(self, mono_wave):
        np = self.np
        w = np.clip(mono_wave * 32767, -32767, 32767).astype(np.int16)
        stereo = np.column_stack((w, w))
        return self.pygame.sndarray.make_sound(stereo)

    def _synthesize_all(self):
        np = self.np
        sr = self.sample_rate

        # 1. Bow Draw: tension creak and rising low-frequency harmonic
        t_draw = np.linspace(0, 1.3, int(sr * 1.3), False)
        freq_draw = np.linspace(70, 240, len(t_draw))
        creak = np.sin(2 * np.pi * freq_draw * t_draw) * 0.18
        creak += (np.random.uniform(-0.06, 0.06, len(t_draw)) * np.linspace(0.1, 0.35, len(t_draw)))
        creak *= (1.0 - np.exp(-4 * t_draw)) * np.linspace(0.3, 0.85, len(t_draw))
        self.sounds['bow_draw'] = self._make_sound(creak * 0.45)

        # 2. Celestial Arrow Launch: sharp twang + ethereal resonant whoosh
        t_rel = np.linspace(0, 0.75, int(sr * 0.75), False)
        twang = (np.sin(2 * np.pi * 280 * t_rel) + 0.6 * np.sin(2 * np.pi * 560 * t_rel) + 0.3 * np.sin(2 * np.pi * 840 * t_rel)) * np.exp(-10 * t_rel)
        whoosh_noise = np.random.uniform(-0.25, 0.25, len(t_rel)) * (np.sin(np.pi * t_rel / 0.75)**1.5)
        energy_hum = np.sin(2 * np.pi * np.linspace(420, 680, len(t_rel)) * t_rel) * np.exp(-4.5 * t_rel) * 0.25
        rel_wave = twang * 0.65 + whoosh_noise * 0.45 + energy_hum
        self.sounds['arrow_launch'] = self._make_sound(rel_wave * 0.7)

        # 3. Epic Brahmastra Impact: heavy sub-bass boom + shockwave rumble + sizzling burst
        t_exp = np.linspace(0, 2.0, int(sr * 2.0), False)
        sub_bass = np.sin(2 * np.pi * np.linspace(130, 25, len(t_exp)) * t_exp) * np.exp(-2.8 * t_exp)
        rumble = np.sin(2 * np.pi * 42 * t_exp) * np.exp(-1.5 * t_exp) * 0.5
        noise_burst = np.random.uniform(-0.6, 0.6, len(t_exp)) * np.exp(-6.0 * t_exp)
        crackle_tail = np.random.uniform(-0.2, 0.2, len(t_exp)) * np.exp(-2.2 * t_exp) * (np.random.random(len(t_exp)) > 0.85)
        exp_wave = sub_bass * 0.85 + rumble * 0.4 + noise_burst * 0.55 + crackle_tail * 0.4
        self.sounds['impact'] = self._make_sound(exp_wave * 0.8)

        # 4. Firework Rocket Launch Whistle (Ascending pitch)
        t_whistle = np.linspace(0, 0.8, int(sr * 0.8), False)
        freq_whistle = np.linspace(500, 2200, len(t_whistle)) + 30 * np.sin(2 * np.pi * 35 * t_whistle)
        whistle_wave = np.sin(2 * np.pi * freq_whistle * t_whistle) * (1.0 - np.exp(-6 * t_whistle)) * np.exp(-1.2 * t_whistle)
        whistle_noise = np.random.uniform(-0.15, 0.15, len(t_whistle)) * np.exp(-1.5 * t_whistle)
        self.sounds['rocket_whistle'] = self._make_sound((whistle_wave * 0.5 + whistle_noise * 0.3) * 0.4)

        # 5. Varied Aerial Firework Booms
        for i, f_start in enumerate([110, 85, 70]):
            t_fw = np.linspace(0, 2.2, int(sr * 2.2), False)
            fw_bass = np.sin(2 * np.pi * np.linspace(f_start, 30, len(t_fw)) * t_fw) * np.exp(-2.2 * t_fw)
            fw_reverb = np.sin(2 * np.pi * 45 * t_fw) * np.exp(-1.2 * t_fw) * 0.35
            fw_crack = np.random.uniform(-0.4, 0.4, len(t_fw)) * np.exp(-3.5 * t_fw)
            fw_glitter = np.random.uniform(-0.25, 0.25, len(t_fw)) * np.exp(-1.8 * t_fw) * (np.random.random(len(t_fw)) > 0.88)
            fw_total = (fw_bass * 0.75 + fw_reverb + fw_crack * 0.5 + fw_glitter * 0.45) * 0.65
            self.sounds[f'firework_{i+1}'] = self._make_sound(fw_total)

        # 6. Effigy Firecracker Cluster (Rolling Ladi Crackers)
        t_ladi = np.linspace(0, 0.4, int(sr * 0.4), False)
        ladi_wave = np.zeros_like(t_ladi)
        for pop_t in [0.0, 0.06, 0.12, 0.17, 0.24, 0.31]:
            idx = int(pop_t * sr)
            dur = int(0.05 * sr)
            if idx + dur < len(ladi_wave):
                p_slice = np.linspace(0, 0.05, dur, False)
                pop_w = np.random.uniform(-0.8, 0.8, dur) * np.exp(-45 * p_slice)
                ladi_wave[idx:idx+dur] += pop_w * np.random.uniform(0.6, 1.0)
        self.sounds['cracker_pop'] = self._make_sound(ladi_wave * 0.45)

        # 7. Sacred Shankha (Victory Conch Shell Horn)
        t_shankha = np.linspace(0, 3.2, int(sr * 3.2), False)
        pitch_env = 220.0 + 12.0 * np.sin(np.pi * np.clip(t_shankha / 3.0, 0, 1)) - 8.0 * np.exp(-8 * t_shankha)
        amp_env = np.clip(t_shankha / 0.5, 0, 1.0) * np.exp(-0.4 * np.maximum(0, t_shankha - 1.2))
        phase = 2 * np.pi * np.cumsum(pitch_env) / sr
        shankha_wave = (
            0.65 * np.sin(phase) +
            0.40 * np.sin(2 * phase) +
            0.28 * np.sin(3 * phase) +
            0.15 * np.sin(4 * phase) +
            0.08 * np.sin(5 * phase)
        ) * amp_env
        breath_air = np.random.uniform(-0.06, 0.06, len(t_shankha)) * amp_env
        self.sounds['shankha'] = self._make_sound((shankha_wave + breath_air) * 0.6)

        # 8. Sacred Temple Bell (Ghanta) with long shimmering chime decay
        t_bell = np.linspace(0, 3.5, int(sr * 3.5), False)
        bell_harmonics = [(440.0, 1.0, 1.4), (884.0, 0.6, 2.0), (1328.0, 0.4, 2.8), (1772.0, 0.25, 3.5), (2216.0, 0.15, 4.2)]
        bell_wave = np.zeros_like(t_bell)
        for freq, amp, decay in bell_harmonics:
            strike = np.sin(2 * np.pi * freq * t_bell) * np.exp(-decay * t_bell)
            strike += 0.25 * np.sin(2 * np.pi * (freq + 1.8) * t_bell) * np.exp(-decay * t_bell)
            bell_wave += strike * amp
        bell_wave *= (1.0 - np.exp(-50 * t_bell))
        self.sounds['victory_bell'] = self._make_sound(bell_wave * 0.55)

        # 9. Meditative Sacred Tambura Drone (Seamless Loop Bed)
        t_drone = np.linspace(0, 6.0, int(sr * 6.0), False)
        sa_1 = 130.81
        pa = 196.00
        sa_2 = 261.63
        drone_wave = (
            0.35 * np.sin(2 * np.pi * sa_1 * t_drone + 0.2 * np.sin(2 * np.pi * 0.5 * t_drone)) +
            0.28 * np.sin(2 * np.pi * pa * t_drone) +
            0.22 * np.sin(2 * np.pi * sa_2 * t_drone) +
            0.12 * np.sin(2 * np.pi * (sa_2 * 2) * t_drone) +
            0.08 * np.sin(2 * np.pi * (pa * 2) * t_drone)
        )
        fade_len = int(sr * 0.25)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        drone_wave[:fade_len] *= fade_in
        drone_wave[-fade_len:] *= fade_out
        self.sounds['ambient_drone'] = self._make_sound(drone_wave * 0.26)

    def _load_external_sounds(self):
        """Load imported MP3 firecracker/fireworks sound files from the script directory or sounds/."""
        import os
        pg = self.pygame
        sound_map = {
            'ext_firework_1': 'dragon-studio-fireworks-07-419025.mp3',
            'ext_firework_2': 'dragon-studio-fireworks-13-419033.mp3',
            'ext_firework_big': 'freesound_community-fireworks-29629.mp3',
        }
        for key, filename in sound_map.items():
            filepath = os.path.join(self._script_dir, filename)
            if not os.path.isfile(filepath):
                alt = os.path.join(self._script_dir, 'sounds', filename)
                if os.path.isfile(alt):
                    filepath = alt
            if os.path.isfile(filepath):
                try:
                    snd = pg.mixer.Sound(filepath)
                    snd.set_volume(0.65)
                    self.sounds[key] = snd
                except Exception as e:
                    print(f"[AUDIO] Could not load {filename}: {e}")
            else:
                print(f"[AUDIO] External sound not found: {filepath}")

    def stop_all_effects(self):
        """Stop all sound effects (leaving ambient drone if active)."""
        if not self.enabled:
            return
        for name, snd in self.sounds.items():
            if name != 'ambient_drone':
                try:
                    snd.stop()
                except Exception:
                    pass

    def start_ambient(self):
        if not self.enabled or self.muted:
            return
        snd = self.sounds.get('ambient_drone')
        if snd:
            try:
                snd.play(loops=-1)
            except Exception:
                pass

    def stop_ambient(self):
        if not self.enabled:
            return
        snd = self.sounds.get('ambient_drone')
        if snd:
            try:
                snd.stop()
            except Exception:
                pass

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            self.stop_ambient()
        else:
            self.start_ambient()
        return self.muted

    def play(self, sound_name):
        if not self.enabled or self.muted:
            return
        if sound_name == 'firework':
            sound_name = random.choice(['firework_1', 'firework_2', 'firework_3'])
        elif sound_name == 'ext_firework':
            # Pick a random external firecracker sound for variety
            sound_name = random.choice(['ext_firework_1', 'ext_firework_2'])
        snd = self.sounds.get(sound_name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass

    def play_at_volume(self, sound_name, volume=0.5):
        """Play a sound at a specific volume (0.0 to 1.0) without altering the original."""
        if not self.enabled or self.muted:
            return
        if sound_name == 'ext_firework':
            sound_name = random.choice(['ext_firework_1', 'ext_firework_2'])
        snd = self.sounds.get(sound_name)
        if snd:
            try:
                ch = snd.play()
                if ch:
                    ch.set_volume(volume)
            except Exception:
                pass


# ==============================================================================
# SECTION 3: PARTICLE SYSTEMS (FIRE, SMOKE, SPARKS, FIREWORKS, DEBRIS)
# ==============================================================================
class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'color', 'size', 'life', 'max_life', 'ptype')
    def __init__(self, x, y, vx, vy, color, size, life, ptype='generic'):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.ptype = ptype


class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.fireworks = []
        self.sparkles = []
        self.lanterns = []
        self.sky_flashes = []
        self.petals = []
        self._init_sky_lanterns()

    def _init_sky_lanterns(self):
        for _ in range(20):
            self.lanterns.append({
                'x': random.uniform(60, WIDTH - 60),
                'y': random.uniform(HEIGHT - 220, HEIGHT + 260),
                'speed': random.uniform(14, 32),
                'sway_phase': random.uniform(0, math.pi * 2),
                'size': random.uniform(7, 14),
                'alpha': random.uniform(160, 240)
            })

    def update_lanterns(self, dt):
        for lan in self.lanterns:
            lan['y'] -= lan['speed'] * dt
            lan['sway_phase'] += dt * 1.4
            if lan['y'] < -50:
                lan['y'] = HEIGHT + random.uniform(20, 140)
                lan['x'] = random.uniform(60, WIDTH - 60)

    def add_fire_particle(self, x, y, intensity=1.0):
        vx = random.uniform(-18, 18) * intensity
        vy = random.uniform(-90, -35) * intensity
        size = random.uniform(6, 18) * intensity
        life = random.uniform(0.35, 0.75)
        palette = [
            (255, 255, 210), (255, 220, 50), (255, 140, 10), (220, 45, 10), (140, 15, 10)
        ]
        color = random.choice(palette)
        self.particles.append(Particle(x, y, vx, vy, color, size, life, 'fire'))

    def add_smoke_particle(self, x, y, intensity=1.0):
        vx = random.uniform(-25, 25)
        vy = random.uniform(-60, -25)
        size = random.uniform(12, 28) * intensity
        life = random.uniform(1.0, 2.2)
        gray = random.randint(35, 80)
        color = (gray, gray, gray + 5)
        self.particles.append(Particle(x, y, vx, vy, color, size, life, 'smoke'))

    def add_spark_particle(self, x, y, speed_range=(80, 300)):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(*speed_range)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed - 40
        size = random.uniform(2, 5)
        life = random.uniform(0.4, 1.2)
        color = random.choice([(255, 255, 200), (255, 215, 0), (255, 160, 20), (255, 90, 10)])
        self.particles.append(Particle(x, y, vx, vy, color, size, life, 'spark'))

    def add_debris(self, x, y):
        vx = random.uniform(-140, 140)
        vy = random.uniform(-220, -40)
        size = random.uniform(6, 14)
        life = random.uniform(1.2, 2.5)
        color = random.choice([(160, 70, 20), (120, 30, 10), (80, 50, 20), (220, 140, 30)])
        self.particles.append(Particle(x, y, vx, vy, color, size, life, 'debris'))

    def trigger_cracker_burst(self, x, y):
        colors = [
            (255, 50, 50), (50, 255, 100), (255, 215, 0),
            (255, 255, 255), (255, 130, 20), (180, 70, 255)
        ]
        burst_color = random.choice(colors)
        for _ in range(25):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 220)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(x, y, vx, vy, burst_color, random.uniform(2, 5), random.uniform(0.25, 0.65), 'spark'))

    def add_flower_petal(self, x=None):
        if x is None:
            x = random.uniform(40, WIDTH - 40)
        y = random.uniform(-25, -5)
        # Mix of delicate fluttering petals and miniature whole flower blossoms
        is_blossom = random.random() < 0.30
        color = random.choice([
            (235, 60, 95),    # Rose pink
            (255, 130, 20),   # Saffron marigold
            (255, 215, 0),    # Golden yellow
            (255, 245, 210),  # Jasmine cream
            (240, 85, 115)    # Deep rose
        ])
        self.petals.append({
            'x': x,
            'y': y,
            'vx': random.uniform(-14, 14),
            'vy': random.uniform(36, 72),
            'color': color,
            'size': random.uniform(7, 12) if is_blossom else random.uniform(5, 9),
            'angle': random.uniform(0, 360),
            'va': random.uniform(-65, 65),
            'sway_phase': random.uniform(0, math.pi * 2),
            'sway_speed': random.uniform(1.2, 2.6),
            'sway_amp': random.uniform(22, 50),
            'life': random.uniform(11.0, 16.0),
            'max_life': 16.0,
            'is_blossom': is_blossom
        })

    def update_petals(self, dt):
        alive_petals = []
        for p in self.petals:
            p['life'] -= dt
            if p['life'] <= 0 or p['y'] > HEIGHT + 20:
                continue
            p['sway_phase'] += p['sway_speed'] * dt
            p['angle'] = (p['angle'] + p['va'] * dt) % 360
            sway_offset = math.sin(p['sway_phase']) * p['sway_amp']
            p['x'] += (p['vx'] + sway_offset * 0.4) * dt
            p['y'] += p['vy'] * dt
            alive_petals.append(p)
        self.petals = alive_petals

    def draw_petals(self, surface, pg_module=None):
        if pg_module is None:
            import pygame as pg
        else:
            pg = pg_module
        for p in self.petals:
            ratio = min(1.0, p['life'] / p['max_life'])
            alpha = int(min(240, 255 * ratio))
            sz = int(p['size'])
            col = p['color']
            if p.get('is_blossom', False):
                # Render a miniature 6-petaled falling flower blossom
                b_surf = pg.Surface((sz * 2 + 6, sz * 2 + 6), pg.SRCALPHA)
                for bi in range(6):
                    bang = (bi / 6.0) * math.pi * 2
                    bx = sz + 3 + math.cos(bang) * (sz * 0.52)
                    by = sz + 3 + math.sin(bang) * (sz * 0.52)
                    pg.draw.circle(b_surf, (col[0], col[1], col[2], alpha), (int(bx), int(by)), max(2, sz // 3))
                pg.draw.circle(b_surf, (255, 240, 160, min(255, alpha + 20)), (sz + 3, sz + 3), max(2, sz // 4))
                rot_p = pg.transform.rotate(b_surf, p['angle'])
                surface.blit(rot_p, (int(p['x'] - rot_p.get_width() // 2), int(p['y'] - rot_p.get_height() // 2)))
            else:
                p_surf = pg.Surface((sz * 2 + 6, sz * 2 + 6), pg.SRCALPHA)
                pg.draw.ellipse(p_surf, (col[0], col[1], col[2], alpha), (2, 2, sz * 2, sz + 2))
                pg.draw.ellipse(p_surf, (255, 255, 255, min(140, alpha)), (3, 3, max(2, sz), max(2, sz // 2)))
                rot_p = pg.transform.rotate(p_surf, p['angle'])
                surface.blit(rot_p, (int(p['x'] - rot_p.get_width() // 2), int(p['y'] - rot_p.get_height() // 2)))

    def launch_firework(self, x, y, target_y):
        colors = [
            (255, 215, 0), (255, 60, 60), (60, 255, 140),
            (255, 160, 20), (190, 80, 255), (240, 255, 255),
            (30, 220, 180), (255, 45, 140)
        ]
        chosen_color = random.choice(colors)
        fw_type = random.choice(['chrysanthemum', 'willow', 'double_ring', 'peony', 'palm_crackle', 'kamuro_brocade', 'crossette'])
        self.fireworks.append({
            'x': x,
            'y': y,
            'target_y': target_y,
            'vy': -random.uniform(460, 600),
            'color': chosen_color,
            'type': fw_type,
            'exploded': False
        })

    def trigger_anaar_spark(self, x, y):
        for _ in range(8):
            angle = random.uniform(-math.pi * 0.72, -math.pi * 0.28)
            speed = random.uniform(180, 460)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice([(255, 255, 230), (255, 220, 0), (255, 160, 20), (255, 245, 180), (255, 100, 20)])
            self.particles.append(Particle(x, y, vx, vy, color, random.uniform(2, 4.8), random.uniform(0.35, 0.9), 'spark'))

    def update(self, dt):
        gravity = 340
        alive = []
        for p in self.particles:
            p.life -= dt
            if p.life <= 0:
                continue

            if p.ptype == 'fire':
                p.vy -= 120 * dt
                p.x += p.vx * dt
                p.y += p.vy * dt
                p.size = max(1.0, p.size * (1.0 - 0.7 * dt))
            elif p.ptype == 'smoke':
                p.vy -= 40 * dt
                p.x += p.vx * dt
                p.y += p.vy * dt
                p.size += 15 * dt
            elif p.ptype == 'willow':
                p.vy += 180 * dt
                p.vx *= 0.95
                p.vy *= 0.96
                p.x += p.vx * dt
                p.y += p.vy * dt
            elif p.ptype in ('spark', 'debris', 'peony'):
                p.vy += gravity * dt
                p.vx *= 0.94
                p.vy *= 0.94
                p.x += p.vx * dt
                p.y += p.vy * dt
                if p.y > HEIGHT - 90:
                    p.y = HEIGHT - 90
                    p.vy = -p.vy * 0.35
                    p.vx *= 0.6
            alive.append(p)
        self.particles = alive

        # Update Sky Flashes
        flashes_alive = []
        for fl in self.sky_flashes:
            fl['alpha'] -= fl['decay'] * dt
            if fl['alpha'] > 0:
                flashes_alive.append(fl)
        self.sky_flashes = flashes_alive

        # Update Fireworks Rockets — track newly exploded ones
        fw_alive = []
        self._newly_exploded = []  # for sound sync
        for fw in self.fireworks:
            if not fw['exploded']:
                fw['y'] += fw['vy'] * dt
                fw['vy'] += 160 * dt
                # Soaring rocket glowing trail
                self.particles.append(Particle(fw['x'], fw['y'], random.uniform(-6, 6), random.uniform(15, 65), (255, 215, 100), 2.5, 0.35, 'spark'))
                if fw['y'] <= fw['target_y'] or fw['vy'] >= -30:
                    fw['exploded'] = True
                    self._explode_firework(fw)
                    self._newly_exploded.append(fw)
                else:
                    fw_alive.append(fw)
        self.fireworks = fw_alive
        self.update_lanterns(dt)
        self.update_petals(dt)

    def _explode_firework(self, fw):
        x, y = fw['x'], fw['y']
        color = fw['color']
        fw_type = fw['type']

        # Add ambient sky flash
        self.sky_flashes.append({
            'x': x, 'y': y, 'color': color, 'radius': random.randint(220, 280),
            'alpha': 55.0, 'decay': 130.0
        })

        if fw_type == 'chrysanthemum':
            count = 100
            for i in range(count):
                angle = (i / count) * math.pi * 2 + random.uniform(-0.06, 0.06)
                speed = random.uniform(80, 270)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                life = random.uniform(0.9, 1.8)
                self.particles.append(Particle(x, y, vx, vy, color, random.uniform(3, 5), life, 'spark'))
        elif fw_type == 'willow':
            count = 125
            for _ in range(count):
                angle = random.uniform(-math.pi * 0.95, -math.pi * 0.05)
                speed = random.uniform(50, 250)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                life = random.uniform(1.6, 2.7)
                self.particles.append(Particle(x, y, vx, vy, (255, 225, 75), random.uniform(2.5, 4.5), life, 'willow'))
        elif fw_type == 'double_ring':
            # Outer Ring
            count_out = 65
            speed_out = random.uniform(170, 200)
            for i in range(count_out):
                angle = (i / count_out) * math.pi * 2
                self.particles.append(Particle(x, y, math.cos(angle) * speed_out, math.sin(angle) * speed_out, color, 3.5, 1.5, 'spark'))
            # Inner Contrasting Ring
            inner_col = (255, 60, 60) if color != (255, 60, 60) else (255, 215, 0)
            count_in = 45
            speed_in = random.uniform(90, 115)
            for i in range(count_in):
                angle = (i / count_in) * math.pi * 2
                self.particles.append(Particle(x, y, math.cos(angle) * speed_in, math.sin(angle) * speed_in, inner_col, 3.0, 1.3, 'spark'))
        elif fw_type == 'peony':
            count = 100
            for i in range(count):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(70, 240)
                p_col = color if i % 2 == 0 else (245, 255, 255)
                self.particles.append(Particle(x, y, math.cos(angle) * speed, math.sin(angle) * speed, p_col, random.uniform(3, 5), random.uniform(1.1, 1.9), 'peony'))
        elif fw_type == 'palm_crackle':
            arms = 12
            for a in range(arms):
                base_angle = (a / arms) * math.pi * 2
                for s in range(7):
                    spd = 50 + s * 28
                    vx = math.cos(base_angle) * spd + random.uniform(-10, 10)
                    vy = math.sin(base_angle) * spd + random.uniform(-10, 10)
                    self.particles.append(Particle(x, y, vx, vy, (255, 200, 60), 3.5, random.uniform(1.0, 1.6), 'spark'))
        elif fw_type == 'kamuro_brocade':
            # Majestic weeping-gold waterfall brocade with twinkling tails
            count = 140
            for _ in range(count):
                angle = random.uniform(-math.pi * 0.98, -math.pi * 0.02)
                speed = random.uniform(40, 260)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                life = random.uniform(2.2, 3.4)
                gold_shade = random.choice([(255, 235, 120), (255, 215, 0), (255, 185, 30)])
                self.particles.append(Particle(x, y, vx, vy, gold_shade, random.uniform(3, 4.5), life, 'willow'))
        elif fw_type == 'crossette':
            # Radial comets with splitting cross stars
            arms = 10
            for a in range(arms):
                base_ang = (a / arms) * math.pi * 2 + random.uniform(-0.1, 0.1)
                spd = random.uniform(140, 220)
                vx = math.cos(base_ang) * spd
                vy = math.sin(base_ang) * spd
                self.particles.append(Particle(x, y, vx, vy, color, 4.0, random.uniform(1.2, 1.8), 'spark'))
                for sub_i in range(3):
                    ang_off = (sub_i - 1) * 0.25
                    self.particles.append(Particle(
                        x, y,
                        math.cos(base_ang + ang_off) * (spd * 0.6),
                        math.sin(base_ang + ang_off) * (spd * 0.6),
                        (255, 255, 240), 2.5, random.uniform(0.7, 1.2), 'spark'
                    ))


# ==============================================================================
# PEACOCK FEATHER HELPER
# ==============================================================================
def draw_peacock_feather(surf, x, y, scale=1.0, angle=-18, pg_module=None):
    """Draws an authentic, detailed peacock feather (Mayur-pankha)."""
    if pg_module is None:
        import pygame
    else:
        pygame = pg_module
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def rot(dx, dy):
        return (x + (dx * cos_a - dy * sin_a) * scale,
                y + (dx * sin_a + dy * cos_a) * scale)

    stem_start = rot(0, 18)
    stem_end = rot(0, -42)
    pygame.draw.line(surf, (225, 205, 140), stem_start, stem_end, max(1, int(2 * scale)))

    for i in range(-6, 7):
        t_y = -16 + i * 4
        span = (1.0 - (abs(i) / 7.0)**2) * 20
        pygame.draw.line(surf, (35, 135, 65), rot(0, t_y), rot(-span, t_y), 1)
        pygame.draw.line(surf, (35, 135, 65), rot(0, t_y), rot(span, t_y), 1)

    eye_surf = pygame.Surface((int(38 * scale), int(48 * scale)), pygame.SRCALPHA)
    pygame.draw.ellipse(eye_surf, (15, 165, 135), (0, 0, int(38 * scale), int(48 * scale)))
    pygame.draw.ellipse(eye_surf, (15, 55, 185), (int(4 * scale), int(6 * scale), int(30 * scale), int(36 * scale)))
    pygame.draw.ellipse(eye_surf, (245, 195, 25), (int(8 * scale), int(14 * scale), int(22 * scale), int(24 * scale)))
    pygame.draw.circle(eye_surf, (10, 20, 70), (int(19 * scale), int(26 * scale)), int(8 * scale))
    pygame.draw.circle(eye_surf, (255, 255, 255), (int(21 * scale), int(24 * scale)), max(1, int(2 * scale)))

    rot_eye = pygame.transform.rotate(eye_surf, -angle)
    surf.blit(rot_eye, (x - rot_eye.get_width() // 2, y - int(30 * scale) - rot_eye.get_height() // 2))


# ==============================================================================
# SECTION 4: HIGH-FIDELITY PYGAME CINEMATIC ENGINE
# ==============================================================================
class DasaraCinematicEngine:
    def __init__(self):
        import pygame
        self.pygame = pygame
        # Enable Per-Monitor High-DPI awareness on Windows so 2880x1800 displays at native resolution
        if sys.platform == 'win32':
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass

        # Target native resolution: 2880x1800 (16:10 aspect ratio), default to FULLSCREEN
        self.target_w = DEFAULT_WINDOW_WIDTH
        self.target_h = DEFAULT_WINDOW_HEIGHT
        self.fullscreen = True
        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
        try:
            self.screen = pygame.display.set_mode((self.target_w, self.target_h), flags)
        except Exception:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.audio = ProceduralAudioEngine()
        self.psystem = ParticleSystem()
        self._scaled_surface = None

        # Pre-render static background gradient
        self.sky_surface = pygame.Surface((WIDTH, HEIGHT))
        self._build_sky_gradient()

        # Pre-allocated reusable surfaces (avoid per-frame allocation)
        self._render_surface = pygame.Surface((WIDTH, HEIGHT))
        self._cloud_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self._flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self._pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Particle Surface Cache — keyed by (color_tuple, radius, ptype_tag) -> Surface
        self._particle_cache = {}
        self._particle_cache_max = 512  # max cached entries

        # Twinkling stars coordinates (use isolated RNG to avoid polluting global seed)
        star_rng = random.Random(108)
        self.stars = []
        for _ in range(160):
            sx = star_rng.randint(0, WIDTH)
            sy = star_rng.randint(0, int(HEIGHT * 0.65))
            sr = star_rng.choice([1, 1, 1, 2, 2, 3])
            phase = star_rng.uniform(0, math.pi * 2)
            self.stars.append((sx, sy, sr, phase))

        # Typography
        pygame.font.init()
        self.font_title = self._find_font(['georgia', 'timesnewroman', 'palatino', 'serif'], 74, bold=True)
        self.font_subtitle = self._find_font(['georgia', 'timesnewroman', 'arial', 'sans-serif'], 26, bold=False)
        self.font_ui = self._find_font(['arial', 'calibri', 'sans-serif'], 16, bold=False)

        # State Variables
        self.state_time = 0.0
        self.total_time = 0.0
        self.state = 'INTRO'  # INTRO -> RAMA_AIM -> ARROW_CHARGE -> ARROW_FLY -> DESTRUCTION -> CLIMAX -> GREETING
        self.screen_shake = 0.0
        self.white_flash = 0.0
        self.slow_mo = False
        self.paused = False
        self.fullscreen = True

        # Character Base Coordinates (Grounded flush on terrace rampart at y=556)
        self.rama_bx = 220
        self.rama_by = 556
        self.ravana_rx = 980
        self.ravana_ry = 556

        # Arrow Flight Dynamics (from Rama's bow grip / arrow tip to Ravana's solar plexus)
        self.arrow_start = (398, 386)
        self.arrow_target = (980, 328)
        self.arrow_pos = list(self.arrow_start)
        self.arrow_active = False
        self.arrow_angle = 0.0

        # Effigy Destruction Stages & Detached Falling Heads Physics
        self.effigy_damage = 0.0
        self.effigy_collapse_y = 0.0
        self.effigy_heads_collapsed = [False] * 10
        self.falling_heads = []
        self.cracker_timer = 0.0
        self.firework_timer = 0.0
        self.destruction_timer = 0.0
        self._debris_accumulator = 0.0  # replaces frame-rate dependent modulo check
        self._post_demolition_stage = 0
        self._post_demolition_timer = 0.0

    def _find_font(self, font_names, size, bold=False):
        for name in font_names:
            try:
                f = self.pygame.font.SysFont(name, size, bold=bold)
                if f:
                    return f
            except Exception:
                continue
        return self.pygame.font.Font(None, size)

    def _build_sky_gradient(self):
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            if ratio < 0.6:
                t = ratio / 0.6
                r = int(COLOR_SKY_TOP[0] * (1 - t) + COLOR_SKY_MID[0] * t)
                g = int(COLOR_SKY_TOP[1] * (1 - t) + COLOR_SKY_MID[1] * t)
                b = int(COLOR_SKY_TOP[2] * (1 - t) + COLOR_SKY_MID[2] * t)
            else:
                t = (ratio - 0.6) / 0.4
                r = int(COLOR_SKY_MID[0] * (1 - t) + COLOR_SKY_HORIZON[0] * t)
                g = int(COLOR_SKY_MID[1] * (1 - t) + COLOR_SKY_HORIZON[1] * t)
                b = int(COLOR_SKY_MID[2] * (1 - t) + COLOR_SKY_HORIZON[2] * t)
            self.pygame.draw.line(self.sky_surface, (r, g, b), (0, y), (WIDTH, y))

    # --------------------------------------------------------------------------
    # FUNCTION 1: BACKGROUND & ANCIENT CITYSCAPE ARCHITECTURE
    # --------------------------------------------------------------------------
    def draw_background(self, surface):
        pg = self.pygame
        t = self.total_time
        surface.blit(self.sky_surface, (0, 0))

        # 1. Soft Moonlit Night Clouds Drifting Across Horizon (reuse pre-allocated surface)
        cloud_surf = self._cloud_surface
        cloud_surf.fill((0, 0, 0, 0))
        for c_idx in range(6):
            cx = int((180 + c_idx * 210 + t * 4) % (WIDTH + 200) - 100)
            cy = 135 + (c_idx % 3) * 35
            for c_blob in range(5):
                bx = cx + (c_blob - 2) * 45
                by = cy + int(math.sin(c_blob * 1.2 + t * 0.4) * 12)
                rad = 52 + (c_blob % 3) * 18
                pg.draw.circle(cloud_surf, (24, 30, 62, 28), (bx, by), rad)
                pg.draw.circle(cloud_surf, (42, 50, 88, 16), (bx, by - 6), rad - 8)
        surface.blit(cloud_surf, (0, 0))

        # 2. Twinkling Night Stars
        for sx, sy, sr, phase in self.stars:
            twinkle = (math.sin(t * 3.5 + phase) + 1.0) * 0.5
            alpha = int(120 + 135 * twinkle)
            c = (alpha, alpha, min(255, alpha + 30))
            pg.draw.circle(surface, c, (sx, sy), sr)

        # 3. Glowing Full Moon with Multi-Layered Lunar Halos
        mx, my = 1055, 115
        for radius, alpha in [(125, 10), (95, 18), (75, 30), (58, 55), (46, 85)]:
            halo = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
            pg.draw.circle(halo, (255, 245, 205, alpha), (radius, radius), radius)
            surface.blit(halo, (mx - radius, my - radius))
        pg.draw.circle(surface, (255, 252, 238), (mx, my), 40)
        pg.draw.circle(surface, (242, 238, 220), (mx - 12, my - 8), 10)
        pg.draw.circle(surface, (236, 232, 212), (mx + 10, my + 14), 13)
        pg.draw.circle(surface, (240, 235, 215), (mx + 16, my - 10), 8)
        pg.draw.circle(surface, (235, 230, 210), (mx - 4, my + 18), 7)

        # 4. Deep Distant Palace Skyline (Ayodhya / Ancient Fort Towers & Spire Chhatris)
        deep_col = (12, 10, 22)
        spires = [
            (40, 60, 200), (130, 80, 180), (280, 70, 190),
            (390, 95, 210), (520, 65, 170), (740, 85, 190),
            (850, 90, 210), (980, 75, 180), (1150, 110, 200), (1240, 60, 190)
        ]
        for x, w, h in spires:
            steps = 5
            for s in range(steps):
                sw = int(w * (1.0 - (s / steps) * 0.55))
                sh = int(h / steps)
                sy = 560 - (s + 1) * sh
                sx = x - sw // 2
                pg.draw.rect(surface, deep_col, (sx, sy, sw, sh + 1))
            dome_y = 560 - h - 10
            pg.draw.ellipse(surface, deep_col, (x - w // 4, dome_y, w // 2, 16))
            pg.draw.polygon(surface, (140, 105, 30), [(x, dome_y - 12), (x - 3, dome_y), (x + 3, dome_y)])
            glow_w = pg.Surface((12, 16), pg.SRCALPHA)
            pg.draw.ellipse(glow_w, (220, 150, 40, 85), (0, 0, 12, 16))
            surface.blit(glow_w, (x - 6, 560 - int(h * 0.4)))

        # 5. Grand Midground Nagara Temples with Illuminated Jharokha Portals
        self._draw_grand_temple(surface, 110, 560, scale=0.76, color=(18, 14, 28))
        self._draw_grand_temple(surface, 340, 560, scale=0.90, color=(18, 14, 28))
        self._draw_grand_temple(surface, 540, 560, scale=0.82, color=(26, 20, 38))
        self._draw_grand_temple(surface, 700, 560, scale=1.15, color=(26, 20, 38))
        self._draw_grand_temple(surface, 920, 560, scale=0.80, color=(18, 14, 28))
        self._draw_grand_temple(surface, 1160, 560, scale=0.95, color=(18, 14, 28))

        # 6. Hanging Marigold Garlands (Torans) with Pulsating Golden Fairy Lights
        toran_points = [(0, 150), (210, 205), (430, 165), (650, 210), (870, 170), (1090, 205), (WIDTH, 155)]
        for i in range(len(toran_points) - 1):
            p1 = toran_points[i]
            p2 = toran_points[i+1]
            pg.draw.line(surface, (110, 80, 35), p1, p2, 2)
            for step in range(1, 7):
                ratio = step / 7.0
                gx = int(p1[0] * (1 - ratio) + p2[0] * ratio)
                gy = int(p1[1] * (1 - ratio) + p2[1] * ratio) + int(math.sin(ratio * math.pi) * 16)
                flower_color = (255, 140, 0) if step % 2 == 0 else (255, 215, 0)
                pg.draw.circle(surface, flower_color, (gx, gy), 4)
                pg.draw.circle(surface, (180, 50, 10), (gx, gy), 2)

                bulb_y = gy + 9
                pg.draw.line(surface, (60, 60, 60), (gx, gy), (gx, bulb_y), 1)
                pulse = (math.sin(t * 5 + i * 2 + step) + 1.0) * 0.5
                bulb_glow = pg.Surface((18, 18), pg.SRCALPHA)
                pg.draw.circle(bulb_glow, (255, int(200 + 45 * pulse), 70, int(80 + 50 * pulse)), (9, 9), 8)
                surface.blit(bulb_glow, (gx - 9, bulb_y - 9))
                pg.draw.circle(surface, (255, 255, 220), (gx, bulb_y), 3)

        # 7. Grand Ornate Carved Stone Ramparts / Royal Terrace (Matching Reference)
        terrace_top_y = 556
        pg.draw.rect(surface, (22, 14, 20), (0, terrace_top_y, WIDTH, HEIGHT - terrace_top_y))
        pg.draw.rect(surface, (150, 95, 25), (0, terrace_top_y, WIDTH, 8))
        pg.draw.rect(surface, (220, 160, 45), (0, terrace_top_y + 1, WIDTH, 2))
        pg.draw.rect(surface, (80, 45, 15), (0, terrace_top_y + 7, WIDTH, 2))

        # Intricate Frieze Band with Carved Lotus Motifs and Stone Jali Cutouts
        frieze_y = terrace_top_y + 8
        frieze_h = 28
        pg.draw.rect(surface, (70, 38, 26), (0, frieze_y, WIDTH, frieze_h))
        pg.draw.line(surface, (170, 110, 35), (0, frieze_y), (WIDTH, frieze_y), 2)
        pg.draw.line(surface, (170, 110, 35), (0, frieze_y + frieze_h), (WIDTH, frieze_y + frieze_h), 2)

        for fx in range(35, WIDTH, 70):
            pg.draw.polygon(surface, (200, 140, 50), [
                (fx, frieze_y + 6), (fx - 10, frieze_y + 18), (fx + 10, frieze_y + 18)
            ])
            pg.draw.polygon(surface, (160, 100, 30), [
                (fx, frieze_y + 6), (fx - 10, frieze_y + 18), (fx + 10, frieze_y + 18)
            ], 1)
            pg.draw.circle(surface, (240, 190, 70), (fx, frieze_y + 18), 3)
            pg.draw.polygon(surface, (180, 120, 40), [
                (fx - 10, frieze_y + 18), (fx - 16, frieze_y + 12), (fx - 8, frieze_y + 12)
            ])
            pg.draw.polygon(surface, (180, 120, 40), [
                (fx + 10, frieze_y + 18), (fx + 16, frieze_y + 12), (fx + 8, frieze_y + 12)
            ])
            for dot_i in range(1, 4):
                pg.draw.circle(surface, (180, 125, 45), (fx + dot_i * 17, frieze_y + 14), 2)

        pg.draw.rect(surface, (38, 24, 28), (0, frieze_y + frieze_h, WIDTH, HEIGHT - (frieze_y + frieze_h)))
        # Carved stone masonry courses for palace fortress plinth
        frieze_bot = frieze_y + frieze_h
        for row_i, by in enumerate(range(frieze_bot, HEIGHT, 32)):
            pg.draw.line(surface, (55, 34, 40), (0, by), (WIDTH, by), 2)
            pg.draw.line(surface, (22, 14, 18), (0, by + 1), (WIDTH, by + 1), 1)
            offset = 40 if row_i % 2 == 1 else 0
            for jx in range(offset, WIDTH, 90):
                pg.draw.line(surface, (22, 14, 18), (jx, by), (jx, min(HEIGHT, by + 32)), 2)

        # 8. Royal Flaming Mashaals on Elevated Stone Pedestals (Left & Right)
        self._draw_mashaal(surface, 56, terrace_top_y, t)
        self._draw_mashaal(surface, WIDTH - 56, terrace_top_y, t)

        # 9. Terracotta Diyas along Parapet
        diya_positions = [160, 260, 360, 480, 600, 720, 840, 960, 1080, 1180]
        for dx in diya_positions:
            self._draw_diya(surface, dx, terrace_top_y, t)

        # 10. Terracotta Flowerpot (Anaar) Firecracker Pots on Terrace (grounds fountain sparks)
        for ax in (135, WIDTH - 135):
            self._draw_anaar_pot(surface, ax, terrace_top_y, t)

    def _draw_grand_temple(self, surface, x, base_y, scale=1.0, color=(24, 20, 36)):
        pg = self.pygame
        w = int(145 * scale)
        h = int(270 * scale)
        steps = 8
        for i in range(steps):
            ratio = i / float(steps)
            sw = int(w * (1.0 - ratio * 0.62))
            sh = int(h / steps)
            sy = base_y - (i + 1) * sh
            sx = x - sw // 2
            pg.draw.rect(surface, color, (sx, sy, sw, sh + 1))
            pg.draw.line(surface, (color[0] + 10, color[1] + 10, color[2] + 14), (sx, sy + sh), (sx + sw, sy + sh), 2)

        amalaka_y = base_y - h - int(14 * scale)
        amalaka_w = int(48 * scale)
        pg.draw.ellipse(surface, color, (x - amalaka_w // 2, amalaka_y, amalaka_w, int(18 * scale)))
        pg.draw.ellipse(surface, (color[0] + 12, color[1] + 12, color[2] + 16), (x - amalaka_w // 2 + 4, amalaka_y + 2, amalaka_w - 8, int(14 * scale)), 2)

        kal_y = amalaka_y - int(10 * scale)
        pg.draw.polygon(surface, COLOR_GOLD, [
            (x, kal_y - int(22 * scale)),
            (x - int(7 * scale), kal_y),
            (x + int(7 * scale), kal_y)
        ])
        pg.draw.circle(surface, COLOR_GOLD_LIGHT, (x, kal_y - int(22 * scale)), max(2, int(3 * scale)))

        flag_wave = math.sin(self.total_time * 6 + x) * 6
        flag_pts = [
            (x, kal_y - int(22 * scale)),
            (x + int(32 * scale), kal_y - int(30 * scale) + int(flag_wave)),
            (x + int(20 * scale), kal_y - int(18 * scale) + int(flag_wave * 0.5)),
            (x, kal_y - int(12 * scale))
        ]
        pg.draw.polygon(surface, (255, 110, 15), flag_pts)
        pg.draw.lines(surface, (255, 180, 40), False, flag_pts, 1)

        arch_w = int(68 * scale)
        arch_h = int(82 * scale)
        arch_x = x - arch_w // 2
        arch_y = base_y - arch_h

        pil_w = max(4, int(10 * scale))
        pg.draw.rect(surface, (color[0] + 6, color[1] + 6, color[2] + 10), (arch_x, arch_y, pil_w, arch_h))
        pg.draw.rect(surface, (color[0] + 6, color[1] + 6, color[2] + 10), (arch_x + arch_w - pil_w, arch_y, pil_w, arch_h))

        arch_pts = [
            (arch_x, arch_y + 20),
            (arch_x + arch_w // 4, arch_y + 6),
            (x, arch_y),
            (arch_x + arch_w * 3 // 4, arch_y + 6),
            (arch_x + arch_w, arch_y + 20),
            (arch_x + arch_w, base_y),
            (arch_x, base_y)
        ]
        pg.draw.polygon(surface, color, arch_pts)

        glow_surf = pg.Surface((int(44 * scale), int(56 * scale)), pg.SRCALPHA)
        pg.draw.ellipse(glow_surf, (255, 175, 45, 120), (0, 0, int(44 * scale), int(56 * scale)))
        pg.draw.ellipse(glow_surf, (255, 235, 120, 180), (int(8 * scale), int(10 * scale), int(28 * scale), int(36 * scale)))
        surface.blit(glow_surf, (x - int(22 * scale), base_y - int(58 * scale)))

        up_w, up_h = int(28 * scale), int(38 * scale)
        up_y = base_y - int(h * 0.52)
        pg.draw.rect(surface, (color[0] - 6, color[1] - 6, color[2] - 6), (x - up_w // 2, up_y, up_w, up_h), border_radius=int(6 * scale))
        up_glow = pg.Surface((up_w, up_h), pg.SRCALPHA)
        pg.draw.ellipse(up_glow, (255, 180, 50, 130), (2, 2, up_w - 4, up_h - 4))
        surface.blit(up_glow, (x - up_w // 2, up_y))
        for jx in range(x - up_w // 2 + 5, x + up_w // 2 - 2, 6):
            pg.draw.line(surface, color, (jx, up_y), (jx, up_y + up_h), 1)

    def _draw_mashaal(self, surface, x, base_y, t):
        pg = self.pygame
        pg.draw.rect(surface, (80, 48, 20), (x - 22, base_y - 8, 44, 8), border_radius=2)
        pg.draw.rect(surface, (150, 100, 35), (x - 22, base_y - 8, 44, 8), 2, border_radius=2)
        pg.draw.rect(surface, (65, 38, 15), (x - 16, base_y - 18, 32, 10))

        col_h = 75
        col_top = base_y - 18 - col_h
        pg.draw.rect(surface, (95, 60, 25), (x - 8, col_top, 16, col_h))
        pg.draw.line(surface, (155, 110, 45), (x - 4, col_top), (x - 4, base_y - 18), 2)
        pg.draw.line(surface, (60, 35, 15), (x + 4, col_top), (x + 4, base_y - 18), 2)

        for ring_y in [col_top + 20, col_top + 45]:
            pg.draw.rect(surface, (175, 125, 45), (x - 11, ring_y, 22, 6), border_radius=2)
            pg.draw.circle(surface, (210, 20, 40), (x, ring_y + 3), 2)

        bowl_top = col_top - 18
        bowl_pts = [
            (x - 28, bowl_top), (x + 28, bowl_top),
            (x + 14, col_top), (x - 14, col_top)
        ]
        pg.draw.polygon(surface, (160, 105, 35), bowl_pts)
        pg.draw.polygon(surface, (90, 50, 18), bowl_pts, 2)
        pg.draw.rect(surface, (220, 165, 55), (x - 30, bowl_top - 4, 60, 6), border_radius=2)
        pg.draw.circle(surface, (210, 20, 40), (x - 15, bowl_top - 1), 3)
        pg.draw.circle(surface, (210, 20, 40), (x, bowl_top - 1), 3)
        pg.draw.circle(surface, (210, 20, 40), (x + 15, bowl_top - 1), 3)

        glow_pulse = (math.sin(t * 12 + x) + 1.0) * 0.5
        glow_r = int(75 + 15 * glow_pulse)
        glow_surf = pg.Surface((glow_r * 2, glow_r * 2), pg.SRCALPHA)
        pg.draw.circle(glow_surf, (255, 150, 20, int(50 + 20 * glow_pulse)), (glow_r, glow_r), glow_r)
        pg.draw.circle(glow_surf, (255, 210, 50, int(90 + 30 * glow_pulse)), (glow_r, glow_r), int(glow_r * 0.55))
        surface.blit(glow_surf, (x - glow_r, bowl_top - glow_r - 15))

        flick_x = math.sin(t * 16 + x) * 4
        flick_y = math.cos(t * 20 + x) * 5
        flame_pts = [
            (x - 20, bowl_top - 2),
            (x - 22, bowl_top - 22),
            (x - 12 + flick_x * 0.5, bowl_top - 48 + flick_y),
            (x - 2 + flick_x, bowl_top - 62 + flick_y * 1.5),
            (x + 8 + flick_x * 0.7, bowl_top - 42 + flick_y),
            (x + 18, bowl_top - 52),
            (x + 20, bowl_top - 22),
            (x + 18, bowl_top - 2)
        ]
        pg.draw.polygon(surface, (255, 100, 10), flame_pts)

        mid_flame = [
            (x - 14, bowl_top - 2),
            (x - 14, bowl_top - 20),
            (x - 6 + flick_x * 0.5, bowl_top - 42 + flick_y),
            (x + 2 + flick_x * 0.8, bowl_top - 50 + flick_y),
            (x + 10, bowl_top - 36),
            (x + 12, bowl_top - 2)
        ]
        pg.draw.polygon(surface, (255, 185, 25), mid_flame)

        inner_flame = [
            (x - 8, bowl_top - 2),
            (x - 6, bowl_top - 18),
            (x + flick_x * 0.4, bowl_top - 32 + flick_y * 0.8),
            (x + 6, bowl_top - 18),
            (x + 6, bowl_top - 2)
        ]
        pg.draw.polygon(surface, (255, 255, 220), inner_flame)

    def _draw_diya(self, surface, x, y, t):
        pg = self.pygame
        pg.draw.ellipse(surface, (140, 50, 20), (x - 14, y - 6, 28, 12))
        pg.draw.ellipse(surface, (95, 30, 10), (x - 12, y - 5, 24, 7))
        flicker_y = math.sin(t * 18 + x) * 2.5
        flicker_x = math.cos(t * 14 + x) * 1.5
        flame_pts = [
            (x - 5, y - 3),
            (x + 5, y - 3),
            (x + 3 + flicker_x, y - 12 + flicker_y),
            (x + flicker_x, y - 20 + flicker_y),
            (x - 3 + flicker_x, y - 12 + flicker_y)
        ]
        halo = pg.Surface((44, 44), pg.SRCALPHA)
        pg.draw.circle(halo, (255, 180, 30, 45), (22, 22), 20)
        surface.blit(halo, (x - 22, y - 25))
        pg.draw.polygon(surface, (255, 120, 10), flame_pts)
        inner_flame = [
            (x - 2.5, y - 3),
            (x + 2.5, y - 3),
            (x + 1.5 + flicker_x * 0.5, y - 9 + flicker_y),
            (x + flicker_x * 0.5, y - 15 + flicker_y),
            (x - 1.5 + flicker_x * 0.5, y - 9 + flicker_y)
        ]
        pg.draw.polygon(surface, (255, 235, 140), inner_flame)

    def _draw_anaar_pot(self, surface, x, y, t):
        """Draws a traditional conical terracotta Anaar (flowerpot firecracker) on terrace stone."""
        pg = self.pygame
        pot_w = 26
        pot_h = 30
        pts = [
            (x - pot_w // 2, y),
            (x + pot_w // 2, y),
            (x + 5, y - pot_h),
            (x - 5, y - pot_h)
        ]
        pg.draw.polygon(surface, (175, 75, 35), pts)
        pg.draw.polygon(surface, (110, 40, 15), pts, 2)
        band_y1 = y - int(pot_h * 0.38)
        band_y2 = y - int(pot_h * 0.65)
        pg.draw.polygon(surface, (255, 215, 0), [
            (x - 10, band_y1), (x + 10, band_y1),
            (x + 7, band_y2), (x - 7, band_y2)
        ])
        pg.draw.polygon(surface, (180, 120, 20), [
            (x - 10, band_y1), (x + 10, band_y1),
            (x + 7, band_y2), (x - 7, band_y2)
        ], 1)
        pg.draw.rect(surface, (80, 70, 60), (x - 3, y - pot_h - 4, 6, 5))
        if self.state in ('CLIMAX', 'GREETING'):
            pulse = (math.sin(t * 25 + x) + 1.0) * 0.5
            pg.draw.circle(surface, (255, 240, 180), (x, y - pot_h - 2), int(3 + pulse * 2))
            pg.draw.circle(surface, (255, 120, 30), (x, y - pot_h - 2), int(6 + pulse * 3), 1)

    # --------------------------------------------------------------------------
    # FUNCTION 2: LORD RAMA ADVANCED PROCEDURAL VECTOR ILLUSTRATION
    # --------------------------------------------------------------------------
    def draw_rama(self, surface, draw_progress=0.0):
        """
        Dignified, athletic illustration of Lord Rama with Megha-shyam blue skin,
        anatomical muscle contouring, expressive lotus eye with catchlight, Vaishnava
        tilak, balanced Kirita-mukut with peacock feather, clean yellow Pitambara silk
        dhoti with saffron borders & flowing sash, and celestial Kodanda bow.
        """
        pg = self.pygame
        bx, by = self.rama_bx, self.rama_by
        t = self.total_time
        breath = math.sin(t * 2.5) * 1.5

        # 1. Divine Radiant Aura (Pulsing Prabhamandala) — Enhanced with lotus mandala rings
        aura_cx, aura_cy = bx + 25, by - 250 + breath
        aura_pulse = (math.sin(t * 2.8) + 1.0) * 0.5
        for rad, alpha in [(145, 8 + int(6 * aura_pulse)), (120, 16 + int(8 * aura_pulse)),
                           (95, 28 + int(12 * aura_pulse)), (72, 50 + int(20 * aura_pulse)),
                           (50, 80 + int(25 * aura_pulse))]:
            a_surf = self._get_cached_glow((255, 225, 95), rad, alpha)
            surface.blit(a_surf, (aura_cx - rad, aura_cy - rad))
        # Spinning divine ray wheel
        for ray_i in range(24):
            ray_ang = (ray_i / 24.0) * math.pi * 2 + t * 0.35
            ray_len = 72 + 18 * math.sin(t * 4.5 + ray_i * 0.8)
            p1 = (aura_cx + math.cos(ray_ang) * 55, aura_cy + math.sin(ray_ang) * 55)
            p2 = (aura_cx + math.cos(ray_ang) * ray_len, aura_cy + math.sin(ray_ang) * ray_len)
            ray_alpha = int(100 + 55 * math.sin(t * 3 + ray_i))
            pg.draw.line(surface, (255, 240, 160, min(255, ray_alpha)), p1, p2, 2)
        # Sacred lotus-petal mandala ring (slowly rotating)
        mandala_r = 105
        for petal_i in range(12):
            p_ang = (petal_i / 12.0) * math.pi * 2 + t * 0.15
            px = aura_cx + math.cos(p_ang) * mandala_r
            py = aura_cy + math.sin(p_ang) * mandala_r
            petal_alpha = int(40 + 30 * math.sin(t * 2 + petal_i * 0.5))
            pg.draw.circle(surface, (255, 215, 80, min(255, petal_alpha)), (int(px), int(py)), 6)

        # 2. Golden Quiver (Tarkash) on Back - Clean embossed leather & gold
        quiver_pts = [
            (bx - 30, by - 145 + breath),
            (bx - 55, by - 240 + breath),
            (bx - 32, by - 246 + breath),
            (bx - 10, by - 150 + breath)
        ]
        pg.draw.polygon(surface, (185, 125, 25), quiver_pts)
        pg.draw.polygon(surface, (125, 80, 15), quiver_pts, 2)
        pg.draw.line(surface, COLOR_GOLD, (bx - 55, by - 240 + breath), (bx - 32, by - 246 + breath), 5)
        pg.draw.circle(surface, COLOR_CRIMSON, (bx - 44, int(by - 243 + breath)), 3)
        pg.draw.line(surface, COLOR_GOLD_LIGHT, (bx - 42, by - 195 + breath), (bx - 20, by - 200 + breath), 3)

        for arr_i, arr_off in enumerate([-7, 0, 7]):
            arr_tail = (bx - 44 + arr_off, by - 244 + breath)
            arr_tip = (bx - 56 + arr_off * 1.2, by - 280 + arr_i * 3 + breath)
            pg.draw.line(surface, (230, 190, 80), arr_tail, arr_tip, 3)
            pg.draw.polygon(surface, (20, 150, 120), [
                arr_tip,
                (arr_tip[0] - 5, arr_tip[1] + 13),
                (arr_tip[0] + 5, arr_tip[1] + 13)
            ])
            pg.draw.circle(surface, COLOR_GOLD, arr_tip, 2)

        # 3. Feet & Paduka Sandals - Balanced Heroic Archer Stance
        pg.draw.polygon(surface, (150, 100, 30), [(bx - 56, by), (bx - 22, by), (bx - 25, by - 9), (bx - 54, by - 9)])
        pg.draw.circle(surface, COLOR_GOLD, (bx - 38, by - 8), 3)
        pg.draw.polygon(surface, COLOR_RAMA_BLUE, [(bx - 50, by - 8), (bx - 26, by - 8), (bx - 30, by - 18), (bx - 46, by - 18)])
        pg.draw.circle(surface, COLOR_GOLD, (bx - 38, by - 17), 3)

        pg.draw.polygon(surface, (150, 100, 30), [(bx + 28, by), (bx + 68, by), (bx + 64, by - 9), (bx + 32, by - 9)])
        pg.draw.circle(surface, COLOR_GOLD, (bx + 50, by - 8), 3)
        pg.draw.polygon(surface, COLOR_RAMA_BLUE, [(bx + 32, by - 8), (bx + 62, by - 8), (bx + 58, by - 18), (bx + 36, by - 18)])
        pg.draw.circle(surface, COLOR_GOLD, (bx + 48, by - 17), 3)

        # 4. Clean Yellow Pitambara Dhoti with Saffron Borders & Natural Drape Folds
        dhoti_base_pts = [
            (bx - 32, by - 120), (bx + 38, by - 120),
            (bx + 68, by - 65), (bx + 62, by - 18),
            (bx + 34, by - 12), (bx + 6, by - 62),
            (bx - 16, by - 12), (bx - 54, by - 18),
            (bx - 50, by - 65)
        ]
        pg.draw.polygon(surface, (250, 195, 25), dhoti_base_pts)
        pg.draw.polygon(surface, (220, 160, 20), [
            (bx - 32, by - 120), (bx - 4, by - 120),
            (bx - 16, by - 12), (bx - 54, by - 18), (bx - 50, by - 65)
        ])

        pleat_lines = [
            ((-24, by - 115), (-42, by - 20)),
            ((-12, by - 115), (-24, by - 15)),
            ((0, by - 115), (-8, by - 55)),
            ((12, by - 115), (16, by - 14)),
            ((26, by - 115), (46, by - 20))
        ]
        for p_top, p_bot in pleat_lines:
            pg.draw.line(surface, (185, 130, 15), (bx + p_top[0], p_top[1]), (bx + p_bot[0], p_bot[1]), 2)
            pg.draw.line(surface, (255, 235, 120), (bx + p_top[0] + 1, p_top[1]), (bx + p_bot[0] + 1, p_bot[1]), 1)

        hem_left = [(bx - 54, by - 18), (bx - 16, by - 12)]
        hem_right = [(bx + 6, by - 12), (bx + 62, by - 18)]
        pg.draw.line(surface, COLOR_CRIMSON, hem_left[0], hem_left[1], 6)
        pg.draw.line(surface, COLOR_CRIMSON, hem_right[0], hem_right[1], 6)
        pg.draw.line(surface, COLOR_GOLD, hem_left[0], hem_left[1], 2)
        pg.draw.line(surface, COLOR_GOLD, hem_right[0], hem_right[1], 2)

        belt_rect = (bx - 32, by - 126, 72, 13)
        pg.draw.rect(surface, COLOR_GOLD, belt_rect, border_radius=4)
        pg.draw.rect(surface, COLOR_GOLD_DARK, belt_rect, 2, border_radius=4)
        pg.draw.circle(surface, COLOR_CRIMSON, (bx + 4, by - 120), 5)
        pg.draw.circle(surface, COLOR_GOLD_LIGHT, (bx + 4, by - 120), 2)
        pg.draw.arc(surface, (255, 255, 245), (bx - 24, by - 122, 26, 16), 0, math.pi, 2)
        pg.draw.arc(surface, (255, 255, 245), (bx + 6, by - 122, 26, 16), 0, math.pi, 2)

        # Front Sash (Patka)
        sash_pts = [(bx - 6, by - 118), (bx + 14, by - 118), (bx + 10, by - 52), (bx - 3, by - 52)]
        pg.draw.polygon(surface, (215, 25, 42), sash_pts)
        pg.draw.lines(surface, COLOR_GOLD, False, [(bx - 6, by - 118), (bx - 3, by - 52)], 2)
        pg.draw.lines(surface, COLOR_GOLD, False, [(bx + 14, by - 118), (bx + 10, by - 52)], 2)
        pg.draw.polygon(surface, COLOR_GOLD, [(bx - 4, by - 52), (bx + 11, by - 52), (bx + 3, by - 44)])

        # Flowing side sash flutter
        side_wave = math.sin(t * 3.5) * 4
        side_sash = [
            (bx - 28, by - 120),
            (bx - 48 + int(side_wave), by - 95),
            (bx - 42 + int(side_wave), by - 70),
            (bx - 32, by - 115)
        ]
        pg.draw.polygon(surface, (215, 25, 42), side_sash)
        pg.draw.line(surface, COLOR_GOLD, (bx - 48 + int(side_wave), by - 95), (bx - 42 + int(side_wave), by - 70), 2)

        # 5. Athletic Torso
        torso_y = by - 192 + breath
        torso_pts = [
            (bx - 28, by - 124), (bx + 34, by - 124),
            (bx + 56, torso_y), (bx - 36, torso_y)
        ]
        pg.draw.polygon(surface, COLOR_RAMA_BLUE, torso_pts)
        pg.draw.polygon(surface, COLOR_RAMA_SHADOW, [
            (bx - 28, by - 124), (bx - 4, by - 124),
            (bx - 10, torso_y), (bx - 36, torso_y)
        ])
        pg.draw.polygon(surface, COLOR_RAMA_LIGHT, [
            (bx + 18, by - 124), (bx + 34, by - 124),
            (bx + 56, torso_y), (bx + 38, torso_y)
        ])

        pec_y = torso_y + 20
        pg.draw.ellipse(surface, COLOR_RAMA_SHADOW, (bx - 20, pec_y, 26, 18))
        pg.draw.ellipse(surface, COLOR_RAMA_BLUE, (bx - 18, pec_y + 1, 22, 15))
        pg.draw.ellipse(surface, COLOR_RAMA_LIGHT, (bx + 8, pec_y, 28, 18))
        pg.draw.ellipse(surface, COLOR_RAMA_BLUE, (bx + 10, pec_y + 1, 24, 15))

        pg.draw.line(surface, (255, 252, 230), (bx - 20, torso_y), (bx + 30, by - 124), 2)
        pg.draw.line(surface, COLOR_GOLD_LIGHT, (bx - 18, torso_y), (bx + 32, by - 124), 1)

        pg.draw.arc(surface, (255, 255, 255), (bx - 10, torso_y - 4, 40, 26), 0.2, math.pi * 0.9, 3)
        pg.draw.circle(surface, (20, 175, 95), (bx + 10, int(torso_y + 18)), 4)
        pg.draw.circle(surface, COLOR_GOLD, (bx + 10, int(torso_y + 18)), 4, 1)

        # 6. Head, Face Profile, Lotus Eye & Balanced Mukut
        neck_y = torso_y - 22
        pg.draw.polygon(surface, COLOR_RAMA_BLUE, [
            (bx + 4, torso_y), (bx + 26, torso_y),
            (bx + 22, neck_y), (bx + 8, neck_y)
        ])
        pg.draw.line(surface, COLOR_RAMA_SHADOW, (bx + 6, torso_y), (bx + 9, neck_y), 2)

        hair_pts = [
            (bx - 4, neck_y - 24), (bx - 20, neck_y - 12),
            (bx - 24, neck_y + 14), (bx - 14, neck_y + 28),
            (bx + 2, neck_y + 8)
        ]
        pg.draw.polygon(surface, (16, 20, 32), hair_pts)
        pg.draw.lines(surface, (30, 45, 75), False, hair_pts, 2)

        face_y = neck_y - 34
        pg.draw.ellipse(surface, COLOR_RAMA_BLUE, (bx + 2, face_y, 34, 38))
        profile_pts = [
            (bx + 20, face_y + 4),
            (bx + 28, face_y + 13),
            (bx + 33, face_y + 18),
            (bx + 28, face_y + 21),
            (bx + 30, face_y + 24),
            (bx + 27, face_y + 26),
            (bx + 29, face_y + 28),
            (bx + 26, face_y + 33),
            (bx + 16, face_y + 34),
            (bx + 8, face_y + 27)
        ]
        pg.draw.polygon(surface, COLOR_RAMA_BLUE, profile_pts)
        pg.draw.lines(surface, COLOR_RAMA_SHADOW, False, profile_pts, 1)

        is_victory = self.state in ('CLIMAX', 'GREETING')
        if is_victory:
            # Compassionate divine victory smile
            pg.draw.arc(surface, (200, 60, 70), (bx + 21, face_y + 21, 11, 7), math.pi, math.pi * 2, 2)
        else:
            pg.draw.line(surface, (190, 70, 75), (bx + 25, face_y + 25), (bx + 29, face_y + 24), 2)

        pg.draw.polygon(surface, (255, 255, 255), [
            (bx + 18, face_y + 16), (bx + 26, face_y + 15),
            (bx + 28, face_y + 17), (bx + 21, face_y + 19)
        ])
        pg.draw.circle(surface, (20, 25, 45), (bx + 23, face_y + 16), 2)
        pg.draw.circle(surface, (255, 255, 255), (bx + 24, face_y + 15), 1)
        pg.draw.line(surface, (12, 16, 25), (bx + 17, face_y + 13), (bx + 27, face_y + 12), 2)

        pg.draw.line(surface, (255, 255, 255), (bx + 22, face_y + 5), (bx + 24, face_y + 14), 2)
        pg.draw.line(surface, COLOR_CRIMSON, (bx + 23, face_y + 6), (bx + 23, face_y + 13), 1)

        pg.draw.circle(surface, COLOR_GOLD, (bx + 10, face_y + 27), 3)
        pg.draw.circle(surface, COLOR_CRIMSON, (bx + 10, face_y + 30), 2)

        crown_base_y = face_y + 5
        pg.draw.polygon(surface, COLOR_GOLD, [
            (bx + 2, crown_base_y), (bx + 32, crown_base_y),
            (bx + 30, crown_base_y - 12), (bx + 4, crown_base_y - 12)
        ])
        pg.draw.polygon(surface, COLOR_GOLD_DARK, [
            (bx + 2, crown_base_y), (bx + 32, crown_base_y),
            (bx + 30, crown_base_y - 12), (bx + 4, crown_base_y - 12)
        ], 2)
        for gem_x in [bx + 8, bx + 17, bx + 26]:
            pg.draw.circle(surface, COLOR_CRIMSON, (gem_x, crown_base_y - 6), 2)

        crown_body_pts = [
            (bx + 5, crown_base_y - 12),
            (bx + 29, crown_base_y - 12),
            (bx + 25, crown_base_y - 36),
            (bx + 17, crown_base_y - 48),
            (bx + 9, crown_base_y - 36)
        ]
        pg.draw.polygon(surface, COLOR_GOLD, crown_body_pts)
        pg.draw.polygon(surface, COLOR_GOLD_DARK, crown_body_pts, 2)
        pg.draw.line(surface, COLOR_GOLD_LIGHT, (bx + 8, crown_base_y - 24), (bx + 26, crown_base_y - 24), 2)
        pg.draw.line(surface, COLOR_GOLD_LIGHT, (bx + 17, crown_base_y - 12), (bx + 17, crown_base_y - 48), 2)
        pg.draw.circle(surface, COLOR_CRIMSON, (bx + 17, crown_base_y - 24), 3)
        pg.draw.circle(surface, COLOR_GOLD_LIGHT, (bx + 17, crown_base_y - 48), 3)

        # Golden Kirita-mukut top finial (royal crown crest)
        pg.draw.polygon(surface, COLOR_GOLD, [
            (bx + 17, crown_base_y - 58),
            (bx + 22, crown_base_y - 48),
            (bx + 12, crown_base_y - 48)
        ])
        pg.draw.polygon(surface, COLOR_GOLD_DARK, [
            (bx + 17, crown_base_y - 58),
            (bx + 22, crown_base_y - 48),
            (bx + 12, crown_base_y - 48)
        ], 1)
        pg.draw.circle(surface, COLOR_CRIMSON, (bx + 17, crown_base_y - 52), 2)
        pg.draw.circle(surface, COLOR_GOLD_LIGHT, (bx + 17, crown_base_y - 58), 2)

        # 7. Contoured Arms, Visible Grip & Dynamic Kodanda Bow Mechanics
        if is_victory:
            # --- VICTORY STANCE: ABHAYA MUDRA & GROUNDED KODANDA BOW ---
            # Left arm holding grounded Kodanda bow stave at his side
            l_shoulder = (bx + 40, torso_y + 14)
            l_elbow = (bx + 48, torso_y + 44)
            l_hand = (bx + 52, torso_y + 74)

            pg.draw.polygon(surface, COLOR_RAMA_BLUE, [
                (l_shoulder[0] - 5, l_shoulder[1] - 4), (l_elbow[0] + 5, l_elbow[1]),
                (l_hand[0] + 5, l_hand[1]), (l_hand[0] - 5, l_hand[1]),
                (l_elbow[0] - 5, l_elbow[1]), (l_shoulder[0] - 5, l_shoulder[1] + 8)
            ])
            pg.draw.circle(surface, COLOR_GOLD, l_elbow, 6)
            pg.draw.circle(surface, COLOR_CRIMSON, l_elbow, 3)
            pg.draw.rect(surface, COLOR_GOLD, (l_hand[0] - 6, l_hand[1] - 4, 12, 8), border_radius=2)
            pg.draw.circle(surface, COLOR_RAMA_BLUE, l_hand, 6)

            # Grounded Kodanda Bow held gracefully at side
            bow_top = (bx + 52, torso_y - 100)
            bow_bottom = (bx + 52, by)
            bow_pts = [
                bow_top,
                (bx + 66, torso_y - 20),
                (bx + 68, torso_y + 40),
                (bx + 62, torso_y + 90),
                bow_bottom
            ]
            pg.draw.lines(surface, (140, 90, 25), False, bow_pts, 7)
            pg.draw.lines(surface, COLOR_GOLD, False, bow_pts, 3)
            pg.draw.line(surface, (255, 255, 240), bow_top, bow_bottom, 2)
            pg.draw.circle(surface, COLOR_GOLD_LIGHT, bow_top, 5)
            pg.draw.circle(surface, COLOR_CRIMSON, bow_top, 3)
            pg.draw.circle(surface, COLOR_GOLD_LIGHT, bow_bottom, 5)

            # Right arm raised in sacred Abhaya Mudra (Blessing & Reassurance)
            r_shoulder = (bx - 22, torso_y + 12)
            r_elbow = (bx - 12, torso_y + 42)
            r_hand = (bx + 14, torso_y + 22)

            pg.draw.polygon(surface, COLOR_RAMA_BLUE, [
                (r_shoulder[0] - 6, r_shoulder[1] - 6), (r_elbow[0] - 6, r_elbow[1] + 6),
                (r_hand[0] - 4, r_hand[1] + 6), (r_hand[0] + 4, r_hand[1] - 6),
                (r_elbow[0] + 6, r_elbow[1] - 6), (r_shoulder[0] + 6, r_shoulder[1] + 6)
            ])
            pg.draw.circle(surface, COLOR_GOLD, r_elbow, 6)
            pg.draw.circle(surface, COLOR_CRIMSON, r_elbow, 3)
            # Golden wrist kada
            pg.draw.rect(surface, COLOR_GOLD, (r_hand[0] - 4, r_hand[1] + 4, 12, 7), border_radius=2)
            # Raised palm facing viewer
            pg.draw.ellipse(surface, COLOR_RAMA_LIGHT, (r_hand[0] - 4, r_hand[1] - 12, 12, 16))
            pg.draw.circle(surface, COLOR_CRIMSON, (r_hand[0] + 2, r_hand[1] - 4), 3) # Auspicious lotus mark on palm
        else:
            s_draw = draw_progress * draw_progress * (3.0 - 2.0 * draw_progress)
            l_shoulder = (bx + 44, torso_y + 14)
            l_elbow = (bx + 74, torso_y + 20)
            l_hand = (bx + 108, torso_y + 20)

            pg.draw.polygon(surface, COLOR_RAMA_BLUE, [
                (l_shoulder[0] - 4, l_shoulder[1] - 8),
                (l_elbow[0], l_elbow[1] - 8),
                (l_hand[0] - 6, l_hand[1] - 6),
                (l_hand[0] - 6, l_hand[1] + 6),
                (l_elbow[0], l_elbow[1] + 8),
                (l_shoulder[0] - 4, l_shoulder[1] + 8)
            ])
            pg.draw.polygon(surface, COLOR_RAMA_SHADOW, [
                (l_shoulder[0] - 4, l_shoulder[1] + 3),
                (l_elbow[0], l_elbow[1] + 4),
                (l_hand[0] - 6, l_hand[1] + 6),
                (l_elbow[0], l_elbow[1] + 8),
                (l_shoulder[0] - 4, l_shoulder[1] + 8)
            ])
            pg.draw.circle(surface, COLOR_GOLD, l_elbow, 6)
            pg.draw.circle(surface, COLOR_CRIMSON, l_elbow, 3)
            pg.draw.rect(surface, COLOR_GOLD, (l_hand[0] - 12, l_hand[1] - 6, 8, 12), border_radius=2)
            pg.draw.circle(surface, COLOR_RAMA_BLUE, l_hand, 6)

            r_shoulder = (bx - 22, torso_y + 12)
            r_elbow_x = bx + 4 - int(26 * s_draw)
            r_elbow_y = torso_y + 40 - int(8 * s_draw)
            r_hand_x = bx + 88 - int(62 * s_draw)
            r_hand_y = torso_y + 20

            pg.draw.polygon(surface, COLOR_RAMA_BLUE, [
                (r_shoulder[0] - 6, r_shoulder[1] - 6),
                (r_elbow_x - 4, r_elbow_y - 7),
                (r_hand_x - 5, r_hand_y - 5),
                (r_hand_x - 5, r_hand_y + 5),
                (r_elbow_x + 4, r_elbow_y + 7),
                (r_shoulder[0] + 6, r_shoulder[1] + 6)
            ])
            pg.draw.circle(surface, COLOR_GOLD, (r_elbow_x, r_elbow_y), 5)
            pg.draw.circle(surface, COLOR_RAMA_BLUE, (r_hand_x, r_hand_y), 5)

            bow_grip = l_hand
            flex_dx = int(16 * s_draw)
            bow_top = (bow_grip[0] - 16 - flex_dx, bow_grip[1] - 135)
            bow_bottom = (bow_grip[0] - 16 - flex_dx, bow_grip[1] + 135)

            limb_upper = [
                bow_grip,
                (bow_grip[0] + 14 - flex_dx * 0.5, bow_grip[1] - 55),
                (bow_grip[0] - 2 - flex_dx, bow_grip[1] - 105),
                bow_top
            ]
            limb_lower = [
                bow_grip,
                (bow_grip[0] + 14 - flex_dx * 0.5, bow_grip[1] + 55),
                (bow_grip[0] - 2 - flex_dx, bow_grip[1] + 105),
                bow_bottom
            ]
            pg.draw.lines(surface, (140, 90, 25), False, limb_upper, 7)
            pg.draw.lines(surface, (140, 90, 25), False, limb_lower, 7)
            pg.draw.lines(surface, COLOR_GOLD, False, limb_upper, 3)
            pg.draw.lines(surface, COLOR_GOLD, False, limb_lower, 3)
            pg.draw.circle(surface, COLOR_GOLD_LIGHT, bow_top, 5)
            pg.draw.circle(surface, COLOR_CRIMSON, bow_top, 3)
            pg.draw.circle(surface, COLOR_GOLD_LIGHT, bow_bottom, 5)
            pg.draw.circle(surface, COLOR_CRIMSON, bow_bottom, 3)

            pg.draw.line(surface, (255, 255, 240), bow_top, (r_hand_x, r_hand_y), 2)
            pg.draw.line(surface, (255, 255, 240), bow_bottom, (r_hand_x, r_hand_y), 2)

            # Update dynamic arrow launch coordinates
            self.arrow_start = (bow_grip[0] + 70, bow_grip[1])

            # 8. Nocked Brahmastra Arrow
            if draw_progress > 0.05 and not self.arrow_active and self.state in ('RAMA_AIM', 'ARROW_CHARGE'):
                arrow_tip = self.arrow_start
                pg.draw.line(surface, COLOR_GOLD_LIGHT, (r_hand_x, r_hand_y), arrow_tip, 3)
                pg.draw.polygon(surface, (255, 255, 255), [
                    (arrow_tip[0] + 18, arrow_tip[1]),
                    (arrow_tip[0] + 4, arrow_tip[1] - 8),
                    (arrow_tip[0] + 9, arrow_tip[1]),
                    (arrow_tip[0] + 4, arrow_tip[1] + 8)
                ])
                pg.draw.circle(surface, (255, 245, 180), arrow_tip, 3)
                pg.draw.polygon(surface, (20, 160, 130), [
                    (r_hand_x, r_hand_y),
                    (r_hand_x - 12, r_hand_y - 6),
                    (r_hand_x - 10, r_hand_y),
                    (r_hand_x - 12, r_hand_y + 6)
                ])

                if self.state == 'ARROW_CHARGE':
                    charge_pulse = (math.sin(t * 20) + 1.0) * 0.5
                    tip_glow = pg.Surface((60, 60), pg.SRCALPHA)
                    pg.draw.circle(tip_glow, (255, 240, 120, int(130 + 80 * charge_pulse)), (30, 30), int(16 + 10 * charge_pulse))
                    pg.draw.circle(tip_glow, (255, 255, 255, 230), (30, 30), 6)
                    # Center the 60x60 bloom directly on the sharp tip of the golden arrowhead (arrow_tip[0] + 18)
                    arrowhead_apex = (arrow_tip[0] + 18, arrow_tip[1])
                    surface.blit(tip_glow, (arrowhead_apex[0] - 30, arrowhead_apex[1] - 30))

    # --------------------------------------------------------------------------
    # FUNCTION 3: TEN-HEADED RAVANA REFINED VECTOR ILLUSTRATION
    # --------------------------------------------------------------------------
    def draw_ravana(self, surface):
        """
        Draws the majestic King Ravana matching the authentic royal epic design:
        - Warm Indian skin tones with flowing dark locks and thick black handlebar moustaches
        - 10 distinct heads arranged in a regal crescent row with tiered golden Mukuts & rubies
        - Dominant central king head directly supported by muscular neck and cascading pearl necklaces
        - Athletic V-taper torso with golden Kavacha, pectoral plates, and 12-beam solar medallion
        - Scalloped shoulder pauldrons with royal purple under-sleeves
        - Emerald-studded golden belt with center Lion-Face (Simha-Mukha) buckle
        - Flared crimson robes with gold borders, royal purple dhoti panels, and diamond-patterned patka
        - Heroic warrior legs planted firmly on the wooden stage with golden padukas
        - Exactly TWO arms: left hand gripping curved Chandrahas sword; right hand gripping golden Bhala spear
        - Permanent celebratory bonfire upon demolition (never reappears).
        """
        pg = self.pygame
        rx = self.ravana_rx
        ry = self.ravana_ry
        dmg = self.effigy_damage
        t = self.total_time
        c_y = int(self.effigy_collapse_y)

        # Reference-accurate Palette
        SKIN_BASE = (228, 160, 118)
        SKIN_SHADOW = (188, 120, 80)
        SKIN_LIGHT = (246, 184, 142)
        HAIR_COLOR = (24, 18, 22)
        GOLD_MAIN = (252, 198, 28)
        GOLD_DARK = (182, 126, 18)
        GOLD_LIGHT = (255, 242, 150)
        RUBY = (218, 24, 42)
        EMERALD = (16, 165, 84)
        PEARL = (255, 252, 242)
        CRIMSON = (206, 26, 40)
        CRIMSON_DARK = (136, 14, 25)
        PURPLE_ROYAL = (112, 28, 110)
        PURPLE_DARK = (76, 16, 76)

        char_factor = min(1.0, dmg * 1.5)
        def char_c(base_rgb):
            return (
                int(base_rgb[0] * (1.0 - char_factor * 0.75)),
                int(base_rgb[1] * (1.0 - char_factor * 0.85)),
                int(base_rgb[2] * (1.0 - char_factor * 0.85))
            )

        # 1. Scaffolding Stage with Natural Bamboo Texture
        stage_w = 320
        stage_h = 34
        stage_top = ry - stage_h # grounded flush with terrace
        pg.draw.rect(surface, (85, 50, 22), (rx - stage_w // 2, stage_top, stage_w, stage_h))
        for slat_y in range(stage_top + 6, ry, 8):
            pg.draw.line(surface, (115, 75, 35), (rx - stage_w // 2, slat_y), (rx + stage_w // 2, slat_y), 2)
            pg.draw.line(surface, (60, 35, 15), (rx - stage_w // 2, slat_y + 2), (rx + stage_w // 2, slat_y + 2), 1)
        pg.draw.line(surface, (55, 30, 12), (rx - stage_w // 2, stage_top), (rx + stage_w // 2, ry), 4)
        pg.draw.line(surface, (55, 30, 12), (rx - stage_w // 2, ry), (rx + stage_w // 2, stage_top), 4)
        pg.draw.circle(surface, (160, 130, 80), (rx, stage_top + stage_h // 2), 6)
        pg.draw.rect(surface, (230, 95, 20), (rx - stage_w // 2, ry - 10, stage_w, 10))

        # PERMANENT POST-DEMOLITION BONFIRE STATE (NEVER REAPPEAR!)
        if dmg >= 0.95:
            bonfire_w = 230
            debris_glow = pg.Surface((bonfire_w + 50, 66), pg.SRCALPHA)
            pulse = (math.sin(t * 14) + 1.0) * 0.5
            pg.draw.ellipse(debris_glow, (255, 80, 10, int(170 + 40 * pulse)), (0, 0, bonfire_w + 50, 66))
            pg.draw.ellipse(debris_glow, (255, 200, 30, int(200 + 45 * pulse)), (25, 14, bonfire_w, 38))
            surface.blit(debris_glow, (rx - bonfire_w // 2 - 25, 496))

            for log_i, (lx, ly, lw, lh) in enumerate([
                (-75, 514, 65, 10), (-20, 510, 80, 12), (32, 512, 70, 10),
                (-50, 504, 60, 8), (15, 502, 55, 8)
            ]):
                pg.draw.ellipse(surface, (45, 18, 14), (rx + lx, ly, lw, lh))
                pg.draw.ellipse(surface, (255, 140, 20), (rx + lx + 6, ly + 2, lw - 12, max(2, lh - 4)), 1)

            for fh in self.falling_heads:
                if fh['grounded'] or fh['y'] >= 510:
                    pg.draw.circle(surface, (35, 18, 18), (int(fh['x']), 522), int(fh['r'] * 0.65))
            return

        # Fire glow around base as damage increases
        if dmg > 0.05:
            fire_pulse = (math.sin(t * 12) + 1.0) * 0.5
            illum_r = int(140 + 40 * fire_pulse)
            illum_surf = pg.Surface((illum_r * 2, illum_r * 2), pg.SRCALPHA)
            pg.draw.circle(illum_surf, (255, 120, 20, int(45 + 30 * fire_pulse * min(1.0, dmg * 1.8))), (illum_r, illum_r), illum_r)
            surface.blit(illum_surf, (rx - illum_r, 340 + c_y - illum_r))

        # 2. RED CAPE DRAPING BEHIND BODY
        cape_pts = [
            (rx - 85, 275 + c_y),
            (rx - 130, 370 + c_y),
            (rx - 110, 485 + int(c_y * 0.4)),
            (rx - 75, 505),
            (rx + 75, 505),
            (rx + 110, 485 + int(c_y * 0.4)),
            (rx + 130, 370 + c_y),
            (rx + 85, 275 + c_y)
        ]
        pg.draw.polygon(surface, char_c(CRIMSON_DARK), cape_pts)
        pg.draw.lines(surface, char_c((170, 18, 30)), False, [
            (rx - 85, 275 + c_y), (rx - 130, 370 + c_y), (rx - 110, 485 + int(c_y * 0.4))
        ], 2)
        pg.draw.lines(surface, char_c((170, 18, 30)), False, [
            (rx + 85, 275 + c_y), (rx + 130, 370 + c_y), (rx + 110, 485 + int(c_y * 0.4))
        ], 2)

        # 3. ATHLETIC WARRIOR LEGS & GOLDEN ARMORED PADUKAS
        foot_y = stage_top
        l_foot_x = rx - 68
        r_foot_x = rx + 68
        knee_y = 445 + int(c_y * 0.3)

        # Muscular calves visible between lower dhoti and ankle cuffs
        pg.draw.polygon(surface, char_c(SKIN_BASE), [
            (l_foot_x - 14, foot_y - 12), (l_foot_x + 12, foot_y - 12),
            (l_foot_x + 16, knee_y + 10), (l_foot_x - 16, knee_y + 10)
        ])
        pg.draw.line(surface, char_c(SKIN_SHADOW), (l_foot_x - 14, foot_y - 12), (l_foot_x - 16, knee_y + 10), 3)

        pg.draw.polygon(surface, char_c(SKIN_BASE), [
            (r_foot_x - 12, foot_y - 12), (r_foot_x + 14, foot_y - 12),
            (r_foot_x + 16, knee_y + 10), (r_foot_x - 16, knee_y + 10)
        ])
        pg.draw.line(surface, char_c(SKIN_SHADOW), (r_foot_x + 14, foot_y - 12), (r_foot_x + 16, knee_y + 10), 3)

        # Golden Ankle Cuffs (Pada-Kadas) with Ruby studs
        for fx in (l_foot_x, r_foot_x):
            pg.draw.rect(surface, char_c(GOLD_MAIN), (fx - 14, foot_y - 16, 28, 8), border_radius=2)
            pg.draw.rect(surface, char_c(GOLD_DARK), (fx - 14, foot_y - 16, 28, 8), 1, border_radius=2)
            pg.draw.circle(surface, char_c(RUBY), (fx, foot_y - 12), 3)

        # Armored Golden Padukas with upturned curved toes (matching reference image)
        # Left Paduka
        pg.draw.polygon(surface, char_c(GOLD_MAIN), [
            (l_foot_x - 32, foot_y), (l_foot_x + 16, foot_y),
            (l_foot_x + 14, foot_y - 12), (l_foot_x - 22, foot_y - 12),
            (l_foot_x - 36, foot_y - 8), (l_foot_x - 38, foot_y - 14), (l_foot_x - 34, foot_y - 14)
        ])
        pg.draw.polygon(surface, char_c(GOLD_DARK), [
            (l_foot_x - 32, foot_y), (l_foot_x + 16, foot_y),
            (l_foot_x + 14, foot_y - 12), (l_foot_x - 22, foot_y - 12),
            (l_foot_x - 36, foot_y - 8), (l_foot_x - 38, foot_y - 14), (l_foot_x - 34, foot_y - 14)
        ], 2)
        pg.draw.circle(surface, char_c(RUBY), (l_foot_x - 6, foot_y - 7), 4)
        pg.draw.circle(surface, char_c(GOLD_LIGHT), (l_foot_x - 7, foot_y - 8), 1)

        # Right Paduka
        pg.draw.polygon(surface, char_c(GOLD_MAIN), [
            (r_foot_x - 16, foot_y), (r_foot_x + 32, foot_y),
            (r_foot_x + 34, foot_y - 14), (r_foot_x + 38, foot_y - 14), (r_foot_x + 36, foot_y - 8),
            (r_foot_x + 22, foot_y - 12), (r_foot_x - 14, foot_y - 12)
        ])
        pg.draw.polygon(surface, char_c(GOLD_DARK), [
            (r_foot_x - 16, foot_y), (r_foot_x + 32, foot_y),
            (r_foot_x + 34, foot_y - 14), (r_foot_x + 38, foot_y - 14), (r_foot_x + 36, foot_y - 8),
            (r_foot_x + 22, foot_y - 12), (r_foot_x - 14, foot_y - 12)
        ], 2)
        pg.draw.circle(surface, char_c(RUBY), (r_foot_x + 6, foot_y - 7), 4)
        pg.draw.circle(surface, char_c(GOLD_LIGHT), (r_foot_x + 5, foot_y - 8), 1)

        # 4. ROYAL DHOTI & EMBROIDERED SASHES (PURPLE THIGH PANELS, CRIMSON OUTER DRAPES)
        waist_y = 370 + c_y
        waist_w = 96

        # Purple Royal Dhoti wrapping around thighs
        l_thigh = [
            (rx - waist_w // 2 + 6, waist_y),
            (rx - 12, waist_y),
            (l_foot_x + 16, knee_y + 12),
            (l_foot_x - 22, knee_y + 12),
            (rx - waist_w // 2 - 14, waist_y + 40)
        ]
        pg.draw.polygon(surface, char_c(PURPLE_ROYAL), l_thigh)
        pg.draw.polygon(surface, char_c(PURPLE_DARK), l_thigh, 2)
        pg.draw.line(surface, char_c(GOLD_MAIN), (l_foot_x - 22, knee_y + 12), (l_foot_x + 16, knee_y + 12), 3)

        r_thigh = [
            (rx + 12, waist_y),
            (rx + waist_w // 2 - 6, waist_y),
            (rx + waist_w // 2 + 14, waist_y + 40),
            (r_foot_x + 22, knee_y + 12),
            (r_foot_x - 16, knee_y + 12)
        ]
        pg.draw.polygon(surface, char_c(PURPLE_ROYAL), r_thigh)
        pg.draw.polygon(surface, char_c(PURPLE_DARK), r_thigh, 2)
        pg.draw.line(surface, char_c(GOLD_MAIN), (r_foot_x - 16, knee_y + 12), (r_foot_x + 22, knee_y + 12), 3)

        # Flared Crimson Outer Drapes (Left and Right)
        l_drape = [
            (rx - waist_w // 2 + 6, waist_y + 8),
            (rx - waist_w // 2 - 38, waist_y + 55),
            (rx - waist_w // 2 - 46, 455 + int(c_y * 0.4)),
            (rx - waist_w // 2 - 24, 485 + int(c_y * 0.2)),
            (rx - 22, 475 + int(c_y * 0.2)),
            (rx - 14, waist_y + 8)
        ]
        pg.draw.polygon(surface, char_c(CRIMSON), l_drape)
        pg.draw.polygon(surface, char_c(CRIMSON_DARK), l_drape, 2)
        # Scalloped Golden Border with ruby gems along hem
        pg.draw.lines(surface, char_c(GOLD_MAIN), False, [
            (rx - waist_w // 2 - 38, waist_y + 55),
            (rx - waist_w // 2 - 46, 455 + int(c_y * 0.4)),
            (rx - waist_w // 2 - 24, 485 + int(c_y * 0.2)),
            (rx - 22, 475 + int(c_y * 0.2))
        ], 5)
        pg.draw.lines(surface, char_c(GOLD_LIGHT), False, [
            (rx - waist_w // 2 - 38, waist_y + 55),
            (rx - waist_w // 2 - 46, 455 + int(c_y * 0.4)),
            (rx - waist_w // 2 - 24, 485 + int(c_y * 0.2)),
            (rx - 22, 475 + int(c_y * 0.2))
        ], 2)
        for ti in range(5):
            tx = rx - waist_w // 2 - 40 + ti * 12
            ty = 460 + int(c_y * 0.3) + ti * 5
            pg.draw.polygon(surface, char_c(GOLD_MAIN), [(tx, ty), (tx + 5, ty - 6), (tx + 10, ty)])

        r_drape = [
            (rx + 14, waist_y + 8),
            (rx + 22, 475 + int(c_y * 0.2)),
            (rx + waist_w // 2 + 24, 485 + int(c_y * 0.2)),
            (rx + waist_w // 2 + 46, 455 + int(c_y * 0.4)),
            (rx + waist_w // 2 + 38, waist_y + 55),
            (rx + waist_w // 2 - 6, waist_y + 8)
        ]
        pg.draw.polygon(surface, char_c(CRIMSON), r_drape)
        pg.draw.polygon(surface, char_c(CRIMSON_DARK), r_drape, 2)
        pg.draw.lines(surface, char_c(GOLD_MAIN), False, [
            (rx + 22, 475 + int(c_y * 0.2)),
            (rx + waist_w // 2 + 24, 485 + int(c_y * 0.2)),
            (rx + waist_w // 2 + 46, 455 + int(c_y * 0.4)),
            (rx + waist_w // 2 + 38, waist_y + 55)
        ], 5)
        pg.draw.lines(surface, char_c(GOLD_LIGHT), False, [
            (rx + 22, 475 + int(c_y * 0.2)),
            (rx + waist_w // 2 + 24, 485 + int(c_y * 0.2)),
            (rx + waist_w // 2 + 46, 455 + int(c_y * 0.4)),
            (rx + waist_w // 2 + 38, waist_y + 55)
        ], 2)
        for ti in range(5):
            tx = rx + 26 + ti * 12
            ty = 478 + int(c_y * 0.2) - ti * 5
            pg.draw.polygon(surface, char_c(GOLD_MAIN), [(tx, ty), (tx + 5, ty - 6), (tx + 10, ty)])

        # Central Long Crimson Patka (Vertical Embroidered Sash)
        patka_w = 34
        patka_pts = [
            (rx - patka_w // 2, waist_y),
            (rx + patka_w // 2, waist_y),
            (rx + patka_w // 2 + 4, 470 + int(c_y * 0.3)),
            (rx, 495 + int(c_y * 0.2)),
            (rx - patka_w // 2 - 4, 470 + int(c_y * 0.3))
        ]
        pg.draw.polygon(surface, char_c(CRIMSON), patka_pts)
        pg.draw.polygon(surface, char_c(GOLD_MAIN), patka_pts, 3)
        # Gold Diamond Embroidery Motifs along the center patka
        for dia_y in [waist_y + 30, waist_y + 60, waist_y + 90]:
            d_size = 7
            pg.draw.polygon(surface, char_c(GOLD_MAIN), [
                (rx, dia_y - d_size), (rx + d_size, dia_y),
                (rx, dia_y + d_size), (rx - d_size, dia_y)
            ])
            pg.draw.circle(surface, char_c(RUBY), (rx, dia_y), 3)
            pg.draw.circle(surface, char_c(GOLD_LIGHT), (rx - 1, dia_y - 1), 1)

        # Yellow/Gold Fluttering Side Sash Ends
        pg.draw.polygon(surface, char_c(GOLD_MAIN), [
            (rx - waist_w // 2 - 30, 460 + int(c_y * 0.3)),
            (rx - waist_w // 2 - 58, 486 + int(c_y * 0.2)),
            (rx - waist_w // 2 - 38, 498 + int(c_y * 0.2)),
            (rx - waist_w // 2 - 20, 476 + int(c_y * 0.3))
        ])
        pg.draw.polygon(surface, char_c(GOLD_MAIN), [
            (rx + waist_w // 2 + 30, 460 + int(c_y * 0.3)),
            (rx + waist_w // 2 + 58, 486 + int(c_y * 0.2)),
            (rx + waist_w // 2 + 38, 498 + int(c_y * 0.2)),
            (rx + waist_w // 2 + 20, 476 + int(c_y * 0.3))
        ])

        # 5. GOLDEN BELT & LION FACE (SIMHA-MUKHA) BUCKLE
        belt_rect = (rx - waist_w // 2 - 4, waist_y - 12, waist_w + 8, 16)
        pg.draw.rect(surface, char_c(GOLD_MAIN), belt_rect, border_radius=4)
        pg.draw.rect(surface, char_c(GOLD_DARK), belt_rect, 2, border_radius=4)
        for gx_off in [-38, -25, 25, 38]:
            pg.draw.circle(surface, char_c(EMERALD), (rx + gx_off, waist_y - 4), 4)
            pg.draw.circle(surface, (255, 255, 255), (rx + gx_off - 1, waist_y - 5), 1)

        # Central Golden Lion Face (Simha-Mukha) Buckle
        lion_cx = rx
        lion_cy = waist_y - 4
        pg.draw.circle(surface, char_c((215, 145, 20)), (lion_cx, lion_cy), 20)
        for i in range(14):
            ang = i * (math.pi * 2 / 14)
            mx = lion_cx + math.cos(ang) * 18
            my = lion_cy + math.sin(ang) * 18
            pg.draw.circle(surface, char_c(GOLD_MAIN), (int(mx), int(my)), 4)
        pg.draw.circle(surface, char_c(GOLD_LIGHT), (lion_cx, lion_cy), 14)
        pg.draw.circle(surface, char_c(GOLD_DARK), (lion_cx, lion_cy), 14, 2)
        pg.draw.circle(surface, char_c(GOLD_MAIN), (lion_cx - 9, lion_cy - 9), 4)
        pg.draw.circle(surface, char_c(GOLD_MAIN), (lion_cx + 9, lion_cy - 9), 4)
        pg.draw.circle(surface, char_c((60, 20, 10)), (lion_cx - 4, lion_cy - 2), 2)
        pg.draw.circle(surface, char_c((60, 20, 10)), (lion_cx + 4, lion_cy - 2), 2)
        pg.draw.polygon(surface, char_c((180, 40, 20)), [(lion_cx, lion_cy + 2), (lion_cx - 3, lion_cy), (lion_cx + 3, lion_cy)])
        pg.draw.arc(surface, char_c((60, 20, 10)), (lion_cx - 5, lion_cy + 1, 10, 6), 0, math.pi, 2)
        pg.draw.circle(surface, char_c(RUBY), (lion_cx, lion_cy - 7), 2)

        # 5. ATHLETIC V-TAPER TORSO & GOLDEN BREASTPLATE (KAVACHA)
        chest_y = 265 + c_y
        shoulder_w = 156

        # Purple Under-Tunic
        torso_base = [
            (rx - waist_w // 2 + 2, waist_y - 10),
            (rx + waist_w // 2 - 2, waist_y - 10),
            (rx + shoulder_w // 2, chest_y + 12),
            (rx - shoulder_w // 2, chest_y + 12)
        ]
        pg.draw.polygon(surface, char_c(PURPLE_DARK), torso_base)

        # Golden Breastplate (Kavacha) with V-taper
        kavacha_pts = [
            (rx - waist_w // 2 + 8, waist_y - 10),
            (rx + waist_w // 2 - 8, waist_y - 10),
            (rx + shoulder_w // 2 - 12, chest_y + 6),
            (rx - shoulder_w // 2 + 12, chest_y + 6)
        ]
        pg.draw.polygon(surface, char_c(GOLD_MAIN), kavacha_pts)
        pg.draw.polygon(surface, char_c(GOLD_DARK), kavacha_pts, 3)

        # Pectoral Plates
        pg.draw.ellipse(surface, char_c((255, 215, 60)), (rx - 52, chest_y + 18, 48, 30))
        pg.draw.ellipse(surface, char_c((255, 215, 60)), (rx + 4, chest_y + 18, 48, 30))
        pg.draw.ellipse(surface, char_c(GOLD_DARK), (rx - 52, chest_y + 18, 48, 30), 2)
        pg.draw.ellipse(surface, char_c(GOLD_DARK), (rx + 4, chest_y + 18, 48, 30), 2)

        # Central Sun Disc on Chest (Arrow Target)
        sun_cx = rx
        sun_cy = 328 + c_y
        pg.draw.circle(surface, char_c((160, 110, 15)), (sun_cx, sun_cy), 20)
        pg.draw.circle(surface, char_c(GOLD_MAIN), (sun_cx, sun_cy), 17)
        for beam_i in range(8):
            b_ang = (beam_i / 8.0) * math.pi * 2
            p_in = (sun_cx + math.cos(b_ang) * 7, sun_cy + math.sin(b_ang) * 7)
            p_out = (sun_cx + math.cos(b_ang) * 16, sun_cy + math.sin(b_ang) * 16)
            pg.draw.line(surface, char_c(GOLD_DARK), p_in, p_out, 2)
        pg.draw.circle(surface, char_c(RUBY), (sun_cx, sun_cy), 7)
        pg.draw.circle(surface, char_c(GOLD_LIGHT), (sun_cx - 2, sun_cy - 2), 2)

        self.arrow_target = (sun_cx, sun_cy)

        # Scalloped Golden Shoulder Pauldrons (Epaulets) with Ruby Studs
        l_paul_center = (rx - 68, chest_y + 6)
        r_paul_center = (rx + 68, chest_y + 6)

        for side, p_cx in [(-1, l_paul_center[0]), (1, r_paul_center[0])]:
            pg.draw.circle(surface, char_c(PURPLE_ROYAL), (p_cx + side * 12, chest_y + 18), 16)
            paul_pts = [
                (p_cx - side * 18, chest_y - 4),
                (p_cx + side * 30, chest_y - 2),
                (p_cx + side * 34, chest_y + 24),
                (p_cx - side * 6, chest_y + 26)
            ]
            pg.draw.polygon(surface, char_c(GOLD_MAIN), paul_pts)
            pg.draw.polygon(surface, char_c(GOLD_DARK), paul_pts, 2)
            pg.draw.circle(surface, char_c(RUBY), (p_cx + side * 10, chest_y + 8), 5)
            pg.draw.circle(surface, char_c(GOLD_LIGHT), (p_cx + side * 9, chest_y + 7), 2)

        # Multi-Strand Pearl & Jewel Necklaces
        collar_pts = [
            (rx - 36, chest_y + 6),
            (rx + 36, chest_y + 6),
            (rx + 28, chest_y - 12),
            (rx - 28, chest_y - 12)
        ]
        pg.draw.polygon(surface, char_c(GOLD_MAIN), collar_pts)
        pg.draw.polygon(surface, char_c(GOLD_DARK), collar_pts, 2)
        for ci in range(-3, 4):
            pg.draw.circle(surface, char_c(RUBY if ci % 2 == 0 else EMERALD), (rx + ci * 8, chest_y - 3), 3)

        # Inner Pearls
        for p_idx in range(13):
            p_rat = p_idx / 12.0
            px = rx - 36 + p_rat * 72
            py = chest_y + 6 + math.sin(p_rat * math.pi) * 22
            pg.draw.circle(surface, char_c(PEARL), (int(px), int(py)), 3)
            if p_idx == 6:
                pg.draw.circle(surface, char_c(RUBY), (int(px), int(py + 4)), 5)
                pg.draw.circle(surface, char_c(GOLD_MAIN), (int(px), int(py + 4)), 5, 1)

        # Outer Pearls & Ruby Medallion
        for p_idx in range(15):
            p_rat = p_idx / 14.0
            px = rx - 48 + p_rat * 96
            py = chest_y + 8 + math.sin(p_rat * math.pi) * 44
            pg.draw.circle(surface, char_c(GOLD_LIGHT), (int(px), int(py)), 3)
            if p_idx == 7:
                pg.draw.circle(surface, char_c(RUBY), (int(px), int(py + 5)), 6)
                pg.draw.circle(surface, char_c(GOLD_MAIN), (int(px), int(py + 5)), 6, 2)

        # Impact Fissure Cracks — Enhanced with branching fractures and molten glow
        if dmg > 0.05:
            fissure_spread = min(1.0, dmg * 2.0)
            fissures = [
                [(sun_cx, sun_cy), (sun_cx - int(16 * fissure_spread), sun_cy - int(22 * fissure_spread)), (sun_cx - int(32 * fissure_spread), sun_cy - int(42 * fissure_spread)), (sun_cx - int(45 * fissure_spread), sun_cy - int(60 * fissure_spread))],
                [(sun_cx, sun_cy), (sun_cx + int(18 * fissure_spread), sun_cy - int(20 * fissure_spread)), (sun_cx + int(36 * fissure_spread), sun_cy - int(38 * fissure_spread)), (sun_cx + int(50 * fissure_spread), sun_cy - int(55 * fissure_spread))],
                [(sun_cx, sun_cy), (sun_cx - int(12 * fissure_spread), sun_cy + int(26 * fissure_spread)), (sun_cx - int(20 * fissure_spread), sun_cy + int(50 * fissure_spread)), (sun_cx - int(28 * fissure_spread), sun_cy + int(68 * fissure_spread))],
                [(sun_cx, sun_cy), (sun_cx + int(14 * fissure_spread), sun_cy + int(22 * fissure_spread)), (sun_cx + int(25 * fissure_spread), sun_cy + int(52 * fissure_spread)), (sun_cx + int(35 * fissure_spread), sun_cy + int(70 * fissure_spread))],
                [(sun_cx, sun_cy), (sun_cx - int(22 * fissure_spread), sun_cy + int(8 * fissure_spread)), (sun_cx - int(48 * fissure_spread), sun_cy + int(18 * fissure_spread))],
                [(sun_cx, sun_cy), (sun_cx + int(20 * fissure_spread), sun_cy + int(6 * fissure_spread)), (sun_cx + int(44 * fissure_spread), sun_cy + int(12 * fissure_spread))]
            ]
            fis_pulse = (math.sin(t * 20) + 1.0) * 0.5
            f_color = (255, int(160 + 90 * fis_pulse), int(20 + 30 * fis_pulse))
            # Molten glow around fissure origin
            glow_r = int(24 + 12 * fis_pulse * fissure_spread)
            glow_surf = self._get_cached_glow((255, 120, 20), glow_r, int(80 + 60 * fis_pulse * fissure_spread))
            surface.blit(glow_surf, (sun_cx - glow_r, sun_cy - glow_r))
            for fis in fissures:
                pg.draw.lines(surface, f_color, False, fis, max(2, int(4 * fissure_spread)))
                pg.draw.lines(surface, (255, 255, 230), False, fis, 1)
                # Ember glow at fissure tips
                tip = fis[-1]
                tip_glow = self._get_cached_glow(f_color, 8, int(65 * fissure_spread))
                surface.blit(tip_glow, (tip[0] - 8, tip[1] - 8))

        # 6. MUSCULAR WARRIOR NECK & FLOWING DARK HAIR LOCKS
        neck_top_y = 230 + c_y
        neck_w = 48
        neck_pts = [
            (rx - neck_w // 2, chest_y + 4),
            (rx + neck_w // 2, chest_y + 4),
            (rx + neck_w // 2 - 4, neck_top_y),
            (rx - neck_w // 2 + 4, neck_top_y)
        ]
        pg.draw.polygon(surface, char_c(SKIN_BASE), neck_pts)
        pg.draw.line(surface, char_c(SKIN_SHADOW), (rx - 14, chest_y + 4), (rx - 18, neck_top_y), 3)
        pg.draw.line(surface, char_c(SKIN_LIGHT), (rx + 14, chest_y + 4), (rx + 18, neck_top_y), 2)

        # Soft curved dark hair locks behind neck and shoulders
        pg.draw.circle(surface, char_c(HAIR_COLOR), (rx - 32, chest_y - 2), 16)
        pg.draw.circle(surface, char_c(HAIR_COLOR), (rx + 32, chest_y - 2), 16)
        pg.draw.circle(surface, char_c(HAIR_COLOR), (rx - 44, chest_y + 14), 14)
        pg.draw.circle(surface, char_c(HAIR_COLOR), (rx + 44, chest_y + 14), 14)

        # 7. EXACTLY TWO MUSCULAR ARMS WITH WEAPONS (NATURAL ATHLETIC ANATOMY)
        if dmg < 0.75:
            # --- VIEWER'S LEFT ARM: Holding Curved Chandrahas Sword ---
            l_sh = (rx - 78, chest_y + 16)
            l_el = (rx - 130, chest_y + 68)
            l_hd = (rx - 142, waist_y + 18)

            # Powerful deltoid shoulder cap (broad at the shoulder near heads)
            pg.draw.circle(surface, char_c(SKIN_BASE), l_sh, 16)
            pg.draw.circle(surface, char_c(SKIN_LIGHT), (l_sh[0] + 2, l_sh[1] - 3), 13)

            # Upper arm: powerful & broad at shoulder (30px), tapering naturally to elbow (22px)
            u_pts_l = [
                (rx - 89, chest_y + 5),
                (rx - 138, chest_y + 60),
                (rx - 122, chest_y + 76),
                (rx - 67, chest_y + 27)
            ]
            pg.draw.polygon(surface, char_c(SKIN_BASE), u_pts_l)
            pg.draw.polygon(surface, char_c(SKIN_SHADOW), u_pts_l, 2)
            pg.draw.line(surface, char_c(SKIN_LIGHT), (rx - 85, chest_y + 10), (rx - 130, chest_y + 64), 3)
            pg.draw.line(surface, char_c(SKIN_SHADOW), (rx - 75, chest_y + 24), (rx - 124, chest_y + 72), 3)

            # Golden Bicep Armlet (Keyur)
            keyur_l = (int(l_sh[0] * 0.45 + l_el[0] * 0.55), int(l_sh[1] * 0.45 + l_el[1] * 0.55))
            pg.draw.circle(surface, char_c(GOLD_MAIN), keyur_l, 9)
            pg.draw.circle(surface, char_c(RUBY), keyur_l, 4)

            # Forearm: starts at elbow (22px), tapers naturally down to wrist (14px, never wider!)
            f_pts_l = [
                (rx - 141, chest_y + 66),
                (rx - 148, waist_y + 17),
                (rx - 136, waist_y + 19),
                (rx - 119, chest_y + 70)
            ]
            pg.draw.polygon(surface, char_c(SKIN_BASE), f_pts_l)
            pg.draw.polygon(surface, char_c(SKIN_SHADOW), f_pts_l, 2)
            pg.draw.line(surface, char_c(SKIN_LIGHT), (rx - 136, chest_y + 70), (rx - 143, waist_y + 16), 2)

            # Golden Wrist Kada / Bracer (neat, fitted to the wrist)
            pg.draw.rect(surface, char_c(GOLD_MAIN), (l_hd[0] - 8, l_hd[1] - 8, 16, 7), border_radius=2)
            pg.draw.circle(surface, char_c(RUBY), (l_hd[0], l_hd[1] - 4), 2)

            # Hand & Gripping Fist
            pg.draw.circle(surface, char_c(SKIN_BASE), (l_hd[0], l_hd[1] + 2), 7)

            # Chandrahas Sword hilt passing through hand
            hilt_x, hilt_y = l_hd[0] - 2, l_hd[1] + 2
            pg.draw.line(surface, char_c(GOLD_MAIN), (hilt_x - 14, hilt_y + 14), (hilt_x + 14, hilt_y - 14), 5)
            pg.draw.circle(surface, char_c(GOLD_MAIN), (hilt_x - 15, hilt_y + 15), 4)
            pg.draw.circle(surface, char_c(RUBY), (hilt_x, hilt_y), 3)

            # Curled fingers gripping the hilt
            for fi, (fox, foy) in enumerate([(-4, 0), (-2, 2), (0, 4), (2, 6)]):
                pg.draw.circle(surface, char_c(SKIN_LIGHT), (l_hd[0] + fox, l_hd[1] + foy), 3)
                pg.draw.circle(surface, char_c(SKIN_SHADOW), (l_hd[0] + fox, l_hd[1] + foy), 3, 1)

            # Curved Chandrahas Blade
            sword_pts = [
                (hilt_x + 6, hilt_y - 8),
                (hilt_x - 25, hilt_y - 65),
                (hilt_x - 55, hilt_y - 135),
                (hilt_x - 52, hilt_y - 195),
                (hilt_x - 32, hilt_y - 140),
                (hilt_x - 12, hilt_y - 70),
                (hilt_x + 12, hilt_y - 8)
            ]
            pg.draw.polygon(surface, (230, 242, 255), sword_pts)
            pg.draw.polygon(surface, (170, 195, 220), sword_pts, 2)
            pg.draw.lines(surface, (255, 255, 255), False, [
                (hilt_x - 25, hilt_y - 65), (hilt_x - 55, hilt_y - 135), (hilt_x - 52, hilt_y - 195)
            ], 2)

            # --- VIEWER'S RIGHT ARM: Holding Royal Golden Spear (Bhala) ---
            r_sh = (rx + 78, chest_y + 16)
            r_el = (rx + 130, chest_y + 68)
            r_hd = (rx + 142, waist_y + 18)

            # Powerful deltoid shoulder cap (broad at the shoulder near heads)
            pg.draw.circle(surface, char_c(SKIN_BASE), r_sh, 16)
            pg.draw.circle(surface, char_c(SKIN_LIGHT), (r_sh[0] - 2, r_sh[1] - 3), 13)

            # Upper arm: powerful & broad at shoulder (30px), tapering naturally to elbow (22px)
            u_pts_r = [
                (rx + 67, chest_y + 27),
                (rx + 122, chest_y + 76),
                (rx + 138, chest_y + 60),
                (rx + 89, chest_y + 5)
            ]
            pg.draw.polygon(surface, char_c(SKIN_BASE), u_pts_r)
            pg.draw.polygon(surface, char_c(SKIN_SHADOW), u_pts_r, 2)
            pg.draw.line(surface, char_c(SKIN_LIGHT), (rx + 85, chest_y + 10), (rx + 130, chest_y + 64), 3)
            pg.draw.line(surface, char_c(SKIN_SHADOW), (rx + 75, chest_y + 24), (rx + 124, chest_y + 72), 3)

            # Golden Bicep Armlet (Keyur)
            keyur_r = (int(r_sh[0] * 0.45 + r_el[0] * 0.55), int(r_sh[1] * 0.45 + r_el[1] * 0.55))
            pg.draw.circle(surface, char_c(GOLD_MAIN), keyur_r, 9)
            pg.draw.circle(surface, char_c(RUBY), keyur_r, 4)

            # Forearm: starts at elbow (22px), tapers naturally down to wrist (14px, never wider!)
            f_pts_r = [
                (rx + 119, chest_y + 70),
                (rx + 136, waist_y + 19),
                (rx + 148, waist_y + 17),
                (rx + 141, chest_y + 66)
            ]
            pg.draw.polygon(surface, char_c(SKIN_BASE), f_pts_r)
            pg.draw.polygon(surface, char_c(SKIN_SHADOW), f_pts_r, 2)
            pg.draw.line(surface, char_c(SKIN_LIGHT), (rx + 136, chest_y + 70), (rx + 143, waist_y + 16), 2)

            # Golden Wrist Kada / Bracer
            pg.draw.rect(surface, char_c(GOLD_MAIN), (r_hd[0] - 8, r_hd[1] - 8, 16, 7), border_radius=2)
            pg.draw.circle(surface, char_c(RUBY), (r_hd[0], r_hd[1] - 4), 2)

            # Hand & Gripping Fist
            pg.draw.circle(surface, char_c(SKIN_BASE), (r_hd[0], r_hd[1] + 2), 7)

            # Golden Spear (Bhala) passing through hand
            spear_bot = (r_hd[0] - 50, r_hd[1] + 130)
            spear_top = (r_hd[0] + 75, r_hd[1] - 200)
            pg.draw.line(surface, char_c((140, 95, 25)), spear_bot, spear_top, 5)
            pg.draw.line(surface, char_c(GOLD_MAIN), spear_bot, spear_top, 2)

            # Curled fingers gripping spear shaft
            for fi, (fox, foy) in enumerate([(-4, 0), (-2, 2), (0, 4), (2, 6)]):
                pg.draw.circle(surface, char_c(SKIN_LIGHT), (r_hd[0] + fox, r_hd[1] + foy), 3)
                pg.draw.circle(surface, char_c(SKIN_SHADOW), (r_hd[0] + fox, r_hd[1] + foy), 3, 1)

            tip_x, tip_y = spear_top
            pg.draw.circle(surface, char_c(GOLD_MAIN), (tip_x, tip_y), 9)
            pg.draw.circle(surface, char_c(RUBY), (tip_x, tip_y), 5)
            spear_head = [
                (tip_x, tip_y),
                (tip_x + 15, tip_y - 25),
                (tip_x + 28, tip_y - 68),
                (tip_x + 4, tip_y - 45),
                (tip_x - 10, tip_y - 28)
            ]
            pg.draw.polygon(surface, char_c(GOLD_MAIN), spear_head)
            pg.draw.polygon(surface, char_c(GOLD_DARK), spear_head, 2)
            pg.draw.polygon(surface, char_c(RUBY), [(tip_x + 8, tip_y - 35), (tip_x + 18, tip_y - 56), (tip_x + 4, tip_y - 42)])

        # 8. EXACTLY 10 DISTINCT HEADS (GENTLE ROYAL CREST ARCH, MATCHING REFERENCE PICTURE)
        head_positions = [
            (rx, 206 + c_y, 27, True, 0),         # Central Head (Dominant King)
            (rx - 32, 210 + c_y, 18, False, 1),   # Left 1
            (rx - 64, 213 + c_y, 17, False, 2),   # Left 2
            (rx - 94, 216 + c_y, 16, False, 3),   # Left 3
            (rx - 122, 219 + c_y, 15, False, 4),  # Left 4
            (rx + 32, 210 + c_y, 18, False, 5),   # Right 1
            (rx + 64, 213 + c_y, 17, False, 6),   # Right 2
            (rx + 94, 216 + c_y, 16, False, 7),   # Right 3
            (rx + 122, 219 + c_y, 15, False, 8),  # Right 4
            (rx + 148, 222 + c_y, 14, False, 9)   # Right 5 (exactly 10 heads)
        ]

        draw_order = [4, 9, 8, 3, 7, 2, 6, 1, 5, 0]

        for h_idx in draw_order:
            if self.effigy_heads_collapsed[h_idx]:
                continue
            hx, hy, hr, is_center, _ = head_positions[h_idx]

            face_col = char_c(SKIN_BASE)
            pg.draw.circle(surface, face_col, (hx, hy), hr)
            pg.draw.circle(surface, char_c(SKIN_SHADOW), (hx, hy), hr, 2)

            pg.draw.ellipse(surface, char_c(SKIN_LIGHT), (hx - hr + 4, hy - hr + 4, int(hr * 1.5), int(hr * 1.4)))
            pg.draw.circle(surface, face_col, (hx, hy), hr - 2)

            eye_spacing = int(hr * 0.42)
            eye_y = hy - 3
            pg.draw.ellipse(surface, (255, 255, 255), (hx - eye_spacing - 4, eye_y - 2, 8, 5))
            pg.draw.circle(surface, (40, 25, 20), (hx - eye_spacing, eye_y), 2)
            pg.draw.circle(surface, (255, 255, 255), (hx - eye_spacing + 1, eye_y - 1), 1)

            pg.draw.ellipse(surface, (255, 255, 255), (hx + eye_spacing - 4, eye_y - 2, 8, 5))
            pg.draw.circle(surface, (40, 25, 20), (hx + eye_spacing, eye_y), 2)
            pg.draw.circle(surface, (255, 255, 255), (hx + eye_spacing + 1, eye_y - 1), 1)

            pg.draw.line(surface, char_c(HAIR_COLOR), (hx - eye_spacing - 5, eye_y - 5), (hx - 2, eye_y - 3), 2)
            pg.draw.line(surface, char_c(HAIR_COLOR), (hx + 2, eye_y - 3), (hx + eye_spacing + 5, eye_y - 5), 2)

            pg.draw.line(surface, char_c(SKIN_SHADOW), (hx, eye_y - 2), (hx - 2, hy + 2), 2)
            pg.draw.line(surface, char_c(SKIN_SHADOW), (hx - 2, hy + 2), (hx + 2, hy + 2), 2)

            # Curled Black Handlebar Mustache
            mustache_y = hy + 6
            pg.draw.arc(surface, char_c(HAIR_COLOR), (hx - eye_spacing - 6, mustache_y - 4, eye_spacing * 2 + 12, 10), 0, math.pi, 3)
            pg.draw.line(surface, char_c(HAIR_COLOR), (hx - eye_spacing - 6, mustache_y), (hx - eye_spacing - 10, mustache_y - 5), 2)
            pg.draw.line(surface, char_c(HAIR_COLOR), (hx + eye_spacing + 6, mustache_y), (hx + eye_spacing + 10, mustache_y - 5), 2)

            # Tilak & Earrings
            pg.draw.line(surface, char_c(RUBY), (hx, hy - hr + 4), (hx, hy - 4), 2)
            pg.draw.circle(surface, char_c(GOLD_MAIN), (hx, hy - hr + 4), 2)

            pg.draw.circle(surface, char_c(GOLD_MAIN), (hx - hr + 2, hy + 4), 3)
            pg.draw.circle(surface, char_c(RUBY), (hx - hr + 2, hy + 4), 1)
            pg.draw.circle(surface, char_c(GOLD_MAIN), (hx + hr - 2, hy + 4), 3)
            pg.draw.circle(surface, char_c(RUBY), (hx + hr - 2, hy + 4), 1)

            # Layered Golden Mukut (Crown) with flared side wings
            crown_w = int(hr * 2.0)
            crown_h = int(hr * 2.1) if is_center else int(hr * 1.5)
            crown_base_y = hy - int(hr * 0.65)

            # Flared side wings of Mukut
            wing_w = int(hr * 0.7)
            wing_h = int(hr * 0.6)
            pg.draw.polygon(surface, char_c(GOLD_MAIN), [
                (hx - crown_w // 2, crown_base_y),
                (hx - crown_w // 2 - wing_w, crown_base_y - wing_h // 2),
                (hx - crown_w // 2 + 2, crown_base_y - wing_h)
            ])
            pg.draw.polygon(surface, char_c(GOLD_DARK), [
                (hx - crown_w // 2, crown_base_y),
                (hx - crown_w // 2 - wing_w, crown_base_y - wing_h // 2),
                (hx - crown_w // 2 + 2, crown_base_y - wing_h)
            ], 1)
            pg.draw.polygon(surface, char_c(GOLD_MAIN), [
                (hx + crown_w // 2, crown_base_y),
                (hx + crown_w // 2 + wing_w, crown_base_y - wing_h // 2),
                (hx + crown_w // 2 - 2, crown_base_y - wing_h)
            ])
            pg.draw.polygon(surface, char_c(GOLD_DARK), [
                (hx + crown_w // 2, crown_base_y),
                (hx + crown_w // 2 + wing_w, crown_base_y - wing_h // 2),
                (hx + crown_w // 2 - 2, crown_base_y - wing_h)
            ], 1)

            crown_pts = [
                (hx - crown_w // 2, crown_base_y),
                (hx + crown_w // 2, crown_base_y),
                (hx + crown_w // 3, hy - crown_h),
                (hx, hy - crown_h - (22 if is_center else 10)),
                (hx - crown_w // 3, hy - crown_h)
            ]
            pg.draw.polygon(surface, char_c(GOLD_MAIN), crown_pts)
            pg.draw.polygon(surface, char_c(GOLD_DARK), crown_pts, 2)
            # Crown horizontal gold bands
            pg.draw.line(surface, char_c(GOLD_LIGHT), (hx - crown_w // 3, hy - int(hr * 0.9)), (hx + crown_w // 3, hy - int(hr * 0.9)), 2)
            pg.draw.line(surface, char_c(GOLD_LIGHT), (hx - crown_w // 4, hy - int(hr * 1.3)), (hx + crown_w // 4, hy - int(hr * 1.3)), 2)

            # Ruby Gem band along base of crown
            for gem_x in range(hx - crown_w // 3, hx + crown_w // 3 + 1, max(6, crown_w // 4)):
                pg.draw.circle(surface, char_c(RUBY), (gem_x, crown_base_y - 3), 2)

            # Central Ruby Gem in Crown
            gem_r = 5 if is_center else 3
            pg.draw.circle(surface, char_c(RUBY), (hx, hy - int(hr * 1.15)), gem_r)
            pg.draw.circle(surface, char_c(GOLD_LIGHT), (hx - 1, hy - int(hr * 1.15) - 1), max(1, gem_r // 2))

            # Spire Finial (Kalasha)
            spire_top = hy - crown_h - (22 if is_center else 10)
            pg.draw.circle(surface, char_c(GOLD_LIGHT), (hx, spire_top), 4 if is_center else 2)
            pg.draw.polygon(surface, char_c(GOLD_MAIN), [(hx, spire_top - 7), (hx - 3, spire_top), (hx + 3, spire_top)])

        # 9. Render Detached Falling Heads with Rotational Spin
        for fh in self.falling_heads:
            if not fh['grounded'] and fh['y'] < 540:
                fh_size = int(fh['r'] * 3)
                fh_surf = pg.Surface((fh_size, fh_size), pg.SRCALPHA)
                center_p = (fh_size // 2, fh_size // 2)
                pg.draw.circle(fh_surf, (30, 20, 25), center_p, int(fh['r']))
                pg.draw.circle(fh_surf, (255, 140, 20), center_p, max(1, int(fh['r']) - 2))
                rot_surf = pg.transform.rotate(fh_surf, fh['angle'])
                surface.blit(rot_surf, (int(fh['x'] - rot_surf.get_width() // 2), int(fh['y'] - rot_surf.get_height() // 2)))

    # --------------------------------------------------------------------------
    # FUNCTION 4: BOW AND ARROW FLIGHT DYNAMICS
    # --------------------------------------------------------------------------
    def draw_bow_and_arrow(self, surface):
        if not self.arrow_active:
            return

        pg = self.pygame
        ax, ay = self.arrow_pos

        bloom_surf = pg.Surface((90, 90), pg.SRCALPHA)
        pg.draw.circle(bloom_surf, (255, 215, 50, 75), (45, 45), 42)
        pg.draw.circle(bloom_surf, (255, 245, 180, 140), (45, 45), 24)
        pg.draw.circle(bloom_surf, (255, 255, 255, 240), (45, 45), 10)
        surface.blit(bloom_surf, (ax - 45, ay - 45))

        arrow_len = 55
        dx = math.cos(self.arrow_angle) * arrow_len
        dy = math.sin(self.arrow_angle) * arrow_len
        tail = (ax - dx, ay - dy)
        head = (ax, ay)
        pg.draw.line(surface, (255, 235, 140), tail, head, 4)

        pg.draw.polygon(surface, (255, 255, 255), [
            (ax + math.cos(self.arrow_angle) * 16, ay + math.sin(self.arrow_angle) * 16),
            (ax + math.cos(self.arrow_angle + 2.4) * 12, ay + math.sin(self.arrow_angle + 2.4) * 12),
            (ax, ay),
            (ax + math.cos(self.arrow_angle - 2.4) * 12, ay + math.sin(self.arrow_angle - 2.4) * 12)
        ])

        pg.draw.circle(surface, (20, 160, 140), tail, 4)
        pg.draw.circle(surface, (255, 215, 0), tail, 2)

        spiral_phase = self.total_time * 25
        for s in range(5):
            s_ratio = s / 5.0
            sx = tail[0] * s_ratio + head[0] * (1.0 - s_ratio)
            sy = tail[1] * s_ratio + head[1] * (1.0 - s_ratio)
            ring_offset = math.sin(spiral_phase + s * 1.5) * 10
            pg.draw.circle(surface, (255, 220, 80), (int(sx), int(sy + ring_offset)), 3)

    # --------------------------------------------------------------------------
    # FUNCTION 5: PROGRESSIVE STAGED DESTRUCTION SEQUENCE WITH HEAD PHYSICS
    # --------------------------------------------------------------------------
    def simulate_destruction(self, dt):
        """
        Multi-stage staged collapse driven monotonically by self.destruction_timer:
        Stage 1: Blinding impact flash, shockwave, navel fissure flames
        Stage 2: Fire spreads rapidly through torso, effigy crackers detonate
        Stage 3: Heads detonate sequentially: heads detach and tumble with physics
        Stage 4: Structural wooden frame fractures and effigy collapses into celebratory bonfire
        """
        if self.state not in ('DESTRUCTION', 'CLIMAX', 'GREETING'):
            return

        rx = self.ravana_rx
        ry = self.ravana_ry
        impact_x, impact_y = self.arrow_target
        self.destruction_timer += dt
        t_dest = self.destruction_timer
        self.cracker_timer += dt

        # Stage 1: Initial Impact & Core Flame (t_dest = 0.0 to 1.5s)
        if t_dest < 1.5:
            self.effigy_damage = min(0.35, t_dest * 0.25)
            for _ in range(5):
                self.psystem.add_fire_particle(impact_x + random.uniform(-25, 25), impact_y + random.uniform(-25, 25), 1.2)
                self.psystem.add_spark_particle(impact_x, impact_y, speed_range=(90, 280))

        # Stage 2: Fire Spreads & Effigy Crackers Detonate (t_dest = 1.5s to 3.5s)
        elif t_dest < 3.5:
            self.effigy_damage = min(0.65, 0.35 + (t_dest - 1.5) * 0.15)
            for _ in range(8):
                fx = rx + random.uniform(-75, 75)
                fy = ry - random.uniform(140, 270)
                self.psystem.add_fire_particle(fx, fy, 1.4)
                self.psystem.add_smoke_particle(fx, fy, 1.1)

            if self.cracker_timer > 0.08:
                self.cracker_timer = 0.0
                cx = rx + random.uniform(-70, 70)
                cy = ry - random.uniform(120, 280)
                self.psystem.trigger_cracker_burst(cx, cy)
                self.audio.play('cracker_pop')
                self.screen_shake = max(self.screen_shake, 3.5)

        # Stage 3: Heads Ignite, Explode & Detach Sequentially (t_dest = 3.5s to 5.5s)
        elif t_dest < 5.5:
            self.effigy_damage = min(0.85, 0.65 + (t_dest - 3.5) * 0.1)

            detonate_order = [4, 8, 3, 7, 2, 6, 1, 5, 9, 0]
            step_idx = int((t_dest - 3.5) / 0.18)
            if step_idx < len(detonate_order):
                target_head = detonate_order[step_idx]
                if not self.effigy_heads_collapsed[target_head]:
                    self.effigy_heads_collapsed[target_head] = True
                    # Demolition firecrackers on effigy: crisp cracker burst and effigy pop
                    self.audio.play('cracker_pop')
                    self.audio.play_at_volume('impact', 0.45)
                    self.screen_shake = 5.0

                    head_offsets = {
                        0: (0, -352, 27),
                        1: (-32, -348, 18), 2: (-64, -345, 17), 3: (-94, -342, 16), 4: (-122, -339, 15),
                        5: (32, -348, 18), 6: (64, -345, 17), 7: (94, -342, 16), 8: (122, -339, 15),
                        9: (148, -336, 14)
                    }
                    h_ox, h_oy, h_r = head_offsets[target_head]
                    hx, hy = rx + h_ox, ry + h_oy + int(self.effigy_collapse_y)

                    self.psystem.trigger_cracker_burst(hx, hy)
                    for _ in range(8):
                        self.psystem.add_debris(hx, hy)

                    out_dir = -1.0 if target_head in [1, 2, 3, 4] else (1.0 if target_head in [5, 6, 7, 8, 9] else random.choice([-0.5, 0.5]))
                    self.falling_heads.append({
                        'x': float(hx),
                        'y': float(hy),
                        'r': h_r,
                        'vx': out_dir * random.uniform(110, 190) + random.uniform(-25, 25),
                        'vy': -random.uniform(90, 200),
                        'angle': 0.0,
                        'va': random.uniform(-180, 180),
                        'grounded': False
                    })

            for _ in range(12):
                self.psystem.add_fire_particle(rx + random.uniform(-90, 90), ry - random.uniform(200, 360), 1.8)
                self.psystem.add_smoke_particle(rx + random.uniform(-70, 70), ry - random.uniform(240, 380), 1.5)

        # Stage 4: Towering Inferno & Structural Wooden Frame Collapse (t_dest >= 5.5s)
        else:
            self.effigy_damage = min(1.0, 0.85 + (t_dest - 5.5) * 0.08)
            if self.effigy_damage >= 1.0:
                self.effigy_heads_collapsed = [True] * 10

            if self.effigy_collapse_y < 180:
                self.effigy_collapse_y += 55 * dt
                # Fixed: use accumulator instead of frame-rate-dependent modulo
                self._debris_accumulator += dt
                if self._debris_accumulator >= 0.45:  # spawn debris every ~0.45 seconds
                    self._debris_accumulator = 0.0
                    self.psystem.add_debris(rx + random.uniform(-60, 60), ry - 140)
                    self.audio.play_at_volume('cracker_pop', 0.25)  # subtle crackle during collapse

            for _ in range(8):
                self.psystem.add_fire_particle(rx + random.uniform(-70, 70), 524 - random.uniform(5, 40), 1.6)
            for _ in range(4):
                self.psystem.add_smoke_particle(rx + random.uniform(-50, 50), 510 - random.uniform(10, 80), 1.3)

        # Update Detached Heads Physics (Gravity, Motion, Spin)
        for fh in self.falling_heads:
            if not fh['grounded']:
                fh['vy'] += 380 * dt
                fh['x'] += fh['vx'] * dt
                fh['y'] += fh['vy'] * dt
                fh['angle'] += fh['va'] * dt
                if fh['y'] >= 540:
                    fh['grounded'] = True
                    self.psystem.trigger_cracker_burst(fh['x'], 540)
                    self.audio.play('cracker_pop')
                elif random.random() < 0.4:
                    self.psystem.add_spark_particle(fh['x'], fh['y'], speed_range=(20, 80))

    # --------------------------------------------------------------------------
    # FUNCTION 6: FIRE AND SMOKE RENDERING
    # --------------------------------------------------------------------------
    def _get_cached_glow(self, color, radius, alpha):
        """Get or create a cached circular glow surface. Massive performance win."""
        pg = self.pygame
        # Quantize to reduce cache entries: radius to nearest 2, alpha to nearest 10
        q_rad = max(2, (radius // 2) * 2)
        q_alpha = max(5, (alpha // 10) * 10)
        key = (color[0], color[1], color[2], q_rad, q_alpha)
        cached = self._particle_cache.get(key)
        if cached is not None:
            return cached
        # Evict oldest if cache is full
        if len(self._particle_cache) >= self._particle_cache_max:
            # Remove first 64 entries (FIFO approximation)
            keys_to_remove = list(self._particle_cache.keys())[:64]
            for k in keys_to_remove:
                del self._particle_cache[k]
        surf = pg.Surface((q_rad * 2, q_rad * 2), pg.SRCALPHA)
        pg.draw.circle(surf, (color[0], color[1], color[2], min(255, q_alpha)), (q_rad, q_rad), q_rad)
        self._particle_cache[key] = surf
        return surf

    def fire_and_smoke(self, surface):
        """Render all particles using cached glow surfaces for performance."""
        pg = self.pygame
        for p in self.psystem.particles:
            ratio = p.life / p.max_life
            alpha = int(255 * ratio)
            px, py = int(p.x), int(p.y)

            if p.ptype == 'fire':
                rad = max(1, int(p.size))
                fire_surf = self._get_cached_glow(p.color, rad, min(255, int(alpha * 1.2)))
                surface.blit(fire_surf, (px - rad, py - rad))
                if rad > 4:
                    core_surf = self._get_cached_glow((255, 255, 220), rad // 2, alpha)
                    surface.blit(core_surf, (px - rad // 2, py - rad // 2))

            elif p.ptype == 'smoke':
                rad = max(2, int(p.size))
                s_alpha = int(90 * ratio)
                smoke_surf = self._get_cached_glow(p.color, rad, s_alpha)
                surface.blit(smoke_surf, (px - rad, py - rad))

            elif p.ptype in ('spark', 'willow', 'peony'):
                rad = max(1, int(p.size))
                if rad >= 2:
                    glow_surf = self._get_cached_glow(p.color, rad * 2, min(130, int(alpha * 0.75)))
                    surface.blit(glow_surf, (px - rad * 2, py - rad * 2))
                pg.draw.circle(surface, p.color, (px, py), rad)
                pg.draw.circle(surface, (255, 255, 240), (px, py), max(1, rad // 2))

            elif p.ptype == 'debris':
                rad = max(2, int(p.size))
                pg.draw.rect(surface, p.color, (px - rad, py - rad, rad * 2, rad * 2))
                pg.draw.circle(surface, (255, 140, 20), (px, py), max(1, rad // 2))

    # --------------------------------------------------------------------------
    # FUNCTION 7: FIREWORKS & FESTIVE CLIMAX
    # --------------------------------------------------------------------------
    def fireworks(self, surface, dt):
        if self.state not in ('CLIMAX', 'GREETING'):
            return

        pg = self.pygame

        # 1. Atmospheric Sky Flashes from Firework Detonations
        for fl in self.psystem.sky_flashes:
            f_rad = int(fl['radius'])
            f_col = fl['color']
            f_alpha = int(min(65, fl['alpha']))
            if f_alpha > 0:
                flash_surf = pg.Surface((f_rad * 2, f_rad * 2), pg.SRCALPHA)
                for step, step_ratio in enumerate([1.0, 0.7, 0.4]):
                    s_r = int(f_rad * step_ratio)
                    s_a = int(f_alpha * (0.3 + 0.3 * (step + 1)))
                    pg.draw.circle(flash_surf, (f_col[0], f_col[1], f_col[2], min(255, s_a)), (f_rad, f_rad), s_r)
                surface.blit(flash_surf, (int(fl['x'] - f_rad), int(fl['y'] - f_rad)))

        # 2. Firework Rocket Launching
        self.firework_timer += dt
        interval = 0.42 if self.state == 'CLIMAX' else 0.70
        if self.firework_timer > interval:
            self.firework_timer = 0.0
            fx = random.uniform(140, WIDTH - 140)
            target_y = random.uniform(75, 230)
            self.psystem.launch_firework(fx, HEIGHT - 70, target_y)
            self.audio.play('rocket_whistle')

        # Play sound ONLY for newly exploded fireworks this frame — synced with visual burst
        for fw in getattr(self.psystem, '_newly_exploded', []):
            self.audio.play('firework')

        # 3. Ground Anaar Spark Fountains (throttled: every other frame to reduce particle count)
        if int(self.total_time * FPS) % 2 == 0:
            self.psystem.trigger_anaar_spark(135, 556)
            self.psystem.trigger_anaar_spark(WIDTH - 135, 556)

        # 4. Floating Sky Lanterns (Kandils)
        for lan in self.psystem.lanterns:
            lx = int(lan['x'] + math.sin(lan['sway_phase']) * 14)
            ly = int(lan['y'])
            l_sz = int(lan['size'])
            l_alpha = int(lan['alpha'])
            lan_surf = pg.Surface((l_sz * 2 + 12, l_sz * 2 + 16), pg.SRCALPHA)
            pg.draw.ellipse(lan_surf, (255, 180, 40, l_alpha // 2), (0, 0, l_sz * 2 + 12, l_sz * 2 + 16))
            pg.draw.rect(lan_surf, (255, 220, 100, l_alpha), (5, 5, l_sz * 2 + 2, l_sz * 2 + 6), border_radius=3)
            pg.draw.circle(lan_surf, (255, 255, 220, min(255, l_alpha + 30)), (l_sz + 6, l_sz + 9), max(2, l_sz // 3))
            surface.blit(lan_surf, (lx - l_sz - 6, ly - l_sz - 8))

    # --------------------------------------------------------------------------
    # FUNCTION 8: TRANSITIONS & CAMERA EFFECTS
    # --------------------------------------------------------------------------
    def transitions(self, surface, dt):
        pg = self.pygame

        if self.white_flash > 0.01:
            flash_surf = self._flash_surface
            alpha = int(255 * min(1.0, self.white_flash))
            flash_surf.fill((255, 250, 220, alpha))
            surface.blit(flash_surf, (0, 0))
            self.white_flash = max(0.0, self.white_flash - dt * 2.2)

        if self.screen_shake > 0.1:
            self.screen_shake = max(0.0, self.screen_shake - dt * 14.0)

        # Cinematic Letterbox Bars
        bar_height = 36
        pg.draw.rect(surface, (4, 4, 10), (0, 0, WIDTH, bar_height))
        pg.draw.rect(surface, (4, 4, 10), (0, HEIGHT - bar_height, WIDTH, bar_height))
        pg.draw.line(surface, COLOR_GOLD_DARK, (0, bar_height), (WIDTH, bar_height), 1)
        pg.draw.line(surface, COLOR_GOLD_DARK, (0, HEIGHT - bar_height), (WIDTH, HEIGHT - bar_height), 1)

    # --------------------------------------------------------------------------
    # FUNCTION 9: FINAL GREETING ("HAPPY DUSSEHRA") WITH FLORAL ELEMENTS
    # --------------------------------------------------------------------------
    def _draw_marigold_flower(self, surface, cx, cy, radius, alpha=255, rot=0.0):
        """Draw an authentic Indian marigold (Genda phool) with layered ruffled petals."""
        pg = self.pygame
        rings = [
            (radius, (240, 110, 15), 12),
            (radius * 0.72, (255, 180, 20), 10),
            (radius * 0.45, (255, 225, 45), 8)
        ]
        for ring_r, color, count in rings:
            step_ang = (math.pi * 2) / count
            for i in range(count):
                ang = rot + i * step_ang
                px = cx + math.cos(ang) * ring_r * 0.62
                py = cy + math.sin(ang) * ring_r * 0.62
                p_r = max(2, int(ring_r * 0.38))
                p_surf = pg.Surface((p_r * 2 + 2, p_r * 2 + 2), pg.SRCALPHA)
                pg.draw.circle(p_surf, (color[0], color[1], color[2], alpha), (p_r + 1, p_r + 1), p_r)
                surface.blit(p_surf, (int(px - p_r - 1), int(py - p_r - 1)))
        # Dark amber/ruby core
        c_r = max(2, int(radius * 0.22))
        c_surf = pg.Surface((c_r * 2 + 2, c_r * 2 + 2), pg.SRCALPHA)
        pg.draw.circle(c_surf, (175, 35, 12, alpha), (c_r + 1, c_r + 1), c_r)
        pg.draw.circle(c_surf, (255, 240, 140, min(255, alpha)), (c_r + 1, c_r + 1), max(1, c_r // 2))
        surface.blit(c_surf, (int(cx - c_r - 1), int(cy - c_r - 1)))

    def _draw_sacred_lotus(self, surface, cx, cy, size, alpha=255):
        """Draw an unfolding sacred Indian lotus (Kamal) with rose petals and golden stamen."""
        pg = self.pygame
        petals = [
            (-0.70, -0.22, 0.28, 0.50, (215, 55, 105)),
            (0.70, -0.22, 0.28, 0.50, (215, 55, 105)),
            (-0.40, -0.55, 0.30, 0.62, (240, 90, 145)),
            (0.40, -0.55, 0.30, 0.62, (240, 90, 145)),
            (0.0, -0.82, 0.32, 0.72, (255, 155, 195)),
        ]
        for ox_f, oy_f, rx_f, ry_f, col in petals:
            px = int(cx + ox_f * size)
            py = int(cy + oy_f * size)
            rw = max(2, int(rx_f * size * 2))
            rh = max(2, int(ry_f * size * 2))
            p_surf = pg.Surface((rw + 4, rh + 4), pg.SRCALPHA)
            pg.draw.ellipse(p_surf, (col[0], col[1], col[2], alpha), (2, 2, rw, rh))
            pg.draw.ellipse(p_surf, (255, 230, 240, min(255, int(alpha * 0.65))), (2 + rw//4, 2 + rh//4, max(1, rw//2), max(1, rh//2)))
            surface.blit(p_surf, (px - rw//2, py - rh//2))
        # Golden pericarp / stamen
        c_r = max(2, int(size * 0.22))
        c_surf = pg.Surface((c_r * 2 + 2, c_r * 2 + 2), pg.SRCALPHA)
        pg.draw.circle(c_surf, (255, 215, 0, alpha), (c_r + 1, c_r + 1), c_r)
        pg.draw.circle(c_surf, (255, 140, 20, alpha), (c_r + 1, c_r + 1), max(1, c_r // 2))
        surface.blit(c_surf, (int(cx - c_r - 1), int(cy - size * 0.08 - c_r - 1)))

    def _draw_toran_garland(self, surface, cx, top_y, width, dip, alpha, t):
        """Draw a festive draped marigold & mango leaf toran garland spanning above greeting."""
        pg = self.pygame
        steps = 16
        prev_pt = None
        for i in range(steps + 1):
            ratio = i / float(steps)
            gx = cx - width // 2 + int(ratio * width)
            gy = int(top_y + (4 * dip * ratio * (1.0 - ratio)))
            if prev_pt is not None:
                # Golden garland string
                pg.draw.line(surface, (215, 165, 30, min(255, int(alpha * 0.75))), prev_pt, (gx, gy), 2)
            prev_pt = (gx, gy)
            if i % 2 == 0:
                # Sacred green mango leaf (Amra-patra)
                leaf_sway = math.sin(t * 2.2 + i * 0.7) * 3
                leaf_h = 20
                leaf_w = 7
                l_surf = pg.Surface((leaf_w * 2 + 6, leaf_h + 4), pg.SRCALPHA)
                pg.draw.polygon(l_surf, (28, 128, 42, alpha), [
                    (leaf_w + 3, 2),
                    (leaf_w * 2 + 2, leaf_h // 2),
                    (leaf_w + 3 + int(leaf_sway), leaf_h),
                    (3, leaf_h // 2)
                ])
                surface.blit(l_surf, (gx - leaf_w - 3, gy))
            else:
                # Festive marigold blossom
                self._draw_marigold_flower(surface, gx, gy, 12, alpha, rot=t * 1.5 + i)

    def final_greeting(self, surface):
        if self.state != 'GREETING':
            return

        pg = self.pygame
        t = self.total_time
        fade_progress = min(1.0, self.state_time / 1.5)
        text_alpha = int(255 * fade_progress)

        # 1. Radial Golden Ambient Back-Glow
        glow_radius = 290
        glow_surf = pg.Surface((glow_radius * 2, glow_radius * 2), pg.SRCALPHA)
        pulse = (math.sin(t * 3.5) + 1.0) * 0.5
        g_alpha = int((50 + 35 * pulse) * fade_progress)
        pg.draw.circle(glow_surf, (255, 200, 40, g_alpha), (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surf, (WIDTH // 2 - glow_radius, 220 - glow_radius))

        # 2. Sacred Rotating Lotus Mandala Aura (behind the title)
        mandala_r = 135
        m_surf = pg.Surface((mandala_r * 2 + 10, mandala_r * 2 + 10), pg.SRCALPHA)
        num_m_petals = 12
        for mi in range(num_m_petals):
            m_ang = (mi / float(num_m_petals)) * math.pi * 2 + t * 0.25
            m_px = mandala_r + 5 + math.cos(m_ang) * (mandala_r * 0.72)
            m_py = mandala_r + 5 + math.sin(m_ang) * (mandala_r * 0.72)
            pg.draw.circle(m_surf, (255, 185, 45, int((35 + 20 * pulse) * fade_progress)), (int(m_px), int(m_py)), 22)
            pg.draw.circle(m_surf, (255, 235, 120, int((45 + 25 * pulse) * fade_progress)), (int(m_px), int(m_py)), 10)
        surface.blit(m_surf, (WIDTH // 2 - mandala_r - 5, 215 - mandala_r - 5))

        # 3. Traditional Festive Floral Toran Garland Arch (above the message)
        self._draw_toran_garland(surface, WIDTH // 2, 105, 780, 42, text_alpha, t)

        # 4. Render 3D Beveled Golden Text: "HAPPY DUSSEHRA"
        greeting_text = "HAPPY DUSSEHRA"
        surf_shadow = self.font_title.render(greeting_text, True, (40, 15, 0))
        surf_dark_gold = self.font_title.render(greeting_text, True, (170, 115, 15))
        surf_gold = self.font_title.render(greeting_text, True, (255, 215, 0))
        surf_light = self.font_title.render(greeting_text, True, (255, 250, 200))

        text_w = surf_gold.get_width()
        text_h = surf_gold.get_height()
        tx = WIDTH // 2 - text_w // 2
        ty = 175

        temp_surf = pg.Surface((text_w + 20, text_h + 20), pg.SRCALPHA)
        temp_surf.blit(surf_shadow, (10, 10))
        temp_surf.blit(surf_dark_gold, (8, 8))
        temp_surf.blit(surf_gold, (6, 6))
        temp_surf.blit(surf_light, (4, 4))
        temp_surf.set_alpha(text_alpha)
        surface.blit(temp_surf, (tx - 6, ty - 6))

        # 5. Flanking Radiant Marigold Flowers & Jasmine Buds (framing the greeting text)
        flower_rot = t * 1.2
        # Left main marigold
        self._draw_marigold_flower(surface, tx - 52, ty + text_h // 2, 28, text_alpha, rot=flower_rot)
        # Left companion jasmine blossoms
        self._draw_sacred_lotus(surface, tx - 85, ty + text_h // 2 - 18, 14, text_alpha)
        self._draw_sacred_lotus(surface, tx - 85, ty + text_h // 2 + 18, 14, text_alpha)
        # Right main marigold
        self._draw_marigold_flower(surface, tx + text_w + 52, ty + text_h // 2, 28, text_alpha, rot=-flower_rot)
        # Right companion jasmine blossoms
        self._draw_sacred_lotus(surface, tx + text_w + 85, ty + text_h // 2 - 18, 14, text_alpha)
        self._draw_sacred_lotus(surface, tx + text_w + 85, ty + text_h // 2 + 18, 14, text_alpha)

        # 6. Animated Diamond Sparkles on Letter Vertices
        sparkle_coords = [
            (tx + 22, ty + 12),
            (tx + text_w * 0.24, ty + 8),
            (tx + text_w * 0.48, ty + 10),
            (tx + text_w * 0.72, ty + 12),
            (tx + text_w - 22, ty + 10)
        ]
        for s_idx, (sx, sy) in enumerate(sparkle_coords):
            s_pulse = (math.sin(t * 6 + s_idx * 1.8) + 1.0) * 0.5
            if s_pulse > 0.4:
                s_size = int(6 + 8 * (s_pulse - 0.4) / 0.6)
                pg.draw.line(surface, (255, 255, 255), (sx - s_size, sy), (sx + s_size, sy), 2)
                pg.draw.line(surface, (255, 255, 255), (sx, sy - s_size), (sx, sy + s_size), 2)
                pg.draw.circle(surface, (255, 235, 140), (sx, sy), 3)

        # 7. Victory Subtitle
        subtitle_text = "VICTORY OF GOOD OVER EVIL  •  VIJAYADASHAMI"
        sub_surf = self.font_subtitle.render(subtitle_text, True, (255, 230, 160))
        sub_w = sub_surf.get_width()
        sub_x = WIDTH // 2 - sub_w // 2
        sub_y = ty + text_h + 18

        sub_temp = pg.Surface((sub_w + 10, sub_surf.get_height() + 10), pg.SRCALPHA)
        sub_temp.blit(sub_surf, (5, 5))
        sub_temp.set_alpha(text_alpha)
        surface.blit(sub_temp, (sub_x - 5, sub_y - 5))

        # 8. Ornamental Divider with Blooming Sacred Lotus
        line_y = sub_y + 42
        pg.draw.line(surface, COLOR_GOLD_DARK, (WIDTH // 2 - 250, line_y), (WIDTH // 2 - 32, line_y), 2)
        pg.draw.line(surface, COLOR_GOLD_DARK, (WIDTH // 2 + 32, line_y), (WIDTH // 2 + 250, line_y), 2)
        # End flourishes
        pg.draw.circle(surface, COLOR_GOLD, (WIDTH // 2 - 250, line_y), 5)
        pg.draw.circle(surface, COLOR_GOLD, (WIDTH // 2 + 250, line_y), 5)
        # Center blooming lotus blossom
        self._draw_sacred_lotus(surface, WIDTH // 2, line_y, 20, text_alpha)

        hint_surf = self.font_ui.render("[SPACE] Replay  |  [F] Fullscreen  |  [S] Slow-Mo  |  [P] Pause  |  [M] Mute  |  [ESC] Exit", True, (215, 205, 230))
        surface.blit(hint_surf, (WIDTH // 2 - hint_surf.get_width() // 2, HEIGHT - 26))

    # --------------------------------------------------------------------------
    # STATE MACHINE & MAIN CINEMATIC LOOP
    # --------------------------------------------------------------------------
    def run(self):
        pg = self.pygame
        running = True
        draw_progress = 0.0

        # Start Sacred Tambura Ambient Drone
        self.audio.start_ambient()

        while running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            if self.slow_mo:
                dt *= 0.35
            if self.paused:
                dt = 0.0

            self.state_time += dt
            self.total_time += dt

            # Event Handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_f:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            try:
                                self.screen = pg.display.set_mode((self.target_w, self.target_h), pg.FULLSCREEN | pg.DOUBLEBUF)
                            except Exception:
                                self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.DOUBLEBUF)
                        else:
                            # 16:10 windowed mode
                            win_w = 1440
                            win_h = 900
                            self.screen = pg.display.set_mode((win_w, win_h), pg.RESIZABLE | pg.DOUBLEBUF)
                    elif event.key == pg.K_s:
                        self.slow_mo = not self.slow_mo
                    elif event.key == pg.K_p:
                        self.paused = not self.paused
                    elif event.key == pg.K_m:
                        self.audio.toggle_mute()
                    elif event.key == pg.K_SPACE and self.state == 'GREETING':
                        # Full replay reset — clears ALL state including particles
                        self.state = 'INTRO'
                        self.state_time = 0.0
                        self.total_time = 0.0
                        self.destruction_timer = 0.0
                        self.effigy_damage = 0.0
                        self.effigy_collapse_y = 0.0
                        self._debris_accumulator = 0.0
                        self._post_demolition_stage = 0
                        self._post_demolition_timer = 0.0
                        self.effigy_heads_collapsed = [False] * 10
                        self.falling_heads.clear()
                        self.arrow_active = False
                        self.screen_shake = 0.0
                        self.white_flash = 0.0
                        # Fresh particle system — clears all residual particles, fireworks, etc.
                        self.psystem = ParticleSystem()
                        self._particle_cache.clear()
                        self.audio.stop_all_effects()
                        self.audio.start_ambient()

            # State Transitions
            if self.state == 'INTRO':
                if self.state_time > 3.0:
                    self.state = 'RAMA_AIM'
                    self.state_time = 0.0
                    self.audio.play('bow_draw')

            elif self.state == 'RAMA_AIM':
                draw_progress = min(1.0, self.state_time / 2.8)
                if self.state_time > 2.8:
                    self.state = 'ARROW_CHARGE'
                    self.state_time = 0.0

            elif self.state == 'ARROW_CHARGE':
                draw_progress = 1.0
                tip_x, tip_y = self.arrow_start
                for _ in range(3):
                    ang = random.uniform(0, math.pi * 2)
                    dist = random.uniform(20, 42)
                    self.psystem.particles.append(Particle(
                        tip_x + math.cos(ang) * dist, tip_y + math.sin(ang) * dist,
                        -math.cos(ang) * 55, -math.sin(ang) * 55,
                        (255, 240, 140), 2.5, 0.4, 'spark'
                    ))
                if self.state_time > 1.2:
                    self.state = 'ARROW_FLY'
                    self.state_time = 0.0
                    self.arrow_active = True
                    self.arrow_pos = list(self.arrow_start)
                    self.audio.play('arrow_launch')

            elif self.state == 'ARROW_FLY':
                draw_progress = 0.0
                t_fly = min(1.0, self.state_time / 0.95)
                self.arrow_pos[0] = self.arrow_start[0] * (1.0 - t_fly) + self.arrow_target[0] * t_fly
                arc_y = -math.sin(t_fly * math.pi) * 35
                self.arrow_pos[1] = (self.arrow_start[1] * (1.0 - t_fly) + self.arrow_target[1] * t_fly) + arc_y
                # Exact analytical tangent derivative d(pos)/dt along parabolic arc
                vx_tangent = self.arrow_target[0] - self.arrow_start[0]
                vy_tangent = (self.arrow_target[1] - self.arrow_start[1]) - 35.0 * math.pi * math.cos(t_fly * math.pi)
                self.arrow_angle = math.atan2(vy_tangent, vx_tangent)

                for _ in range(6):
                    self.psystem.add_spark_particle(self.arrow_pos[0], self.arrow_pos[1], speed_range=(25, 95))

                if t_fly >= 1.0:
                    self.state = 'DESTRUCTION'
                    self.state_time = 0.0
                    self.destruction_timer = 0.0
                    self.arrow_active = False
                    self.white_flash = 1.0
                    self.screen_shake = 12.0
                    self.audio.play('impact')

            elif self.state == 'DESTRUCTION':
                self.simulate_destruction(dt)
                if self.destruction_timer > 7.0:
                    self.state = 'CLIMAX'
                    self.state_time = 0.0
                    self.white_flash = 0.6
                    self.audio.play('shankha')
                    self.audio.play('victory_bell')
                    # Grand celebratory fireworks sequence starts AFTER the demolition fireworks:
                    # Audio 1: dragon-studio-fireworks-07 (6s opening victory barrage)
                    self.audio.play_at_volume('ext_firework_1', 0.75)
                    self._post_demolition_stage = 1
                    self._post_demolition_timer = 0.0

            elif self.state == 'CLIMAX':
                self.simulate_destruction(dt)
                self._post_demolition_timer += dt
                if random.random() < 0.40 and not self.paused:
                    for _ in range(random.randint(1, 3)):
                        self.psystem.add_flower_petal()
                if self.state_time > 3.5:
                    self.state = 'GREETING'
                    self.state_time = 0.0
                    self.audio.play('victory_bell')
                    # Audio 2: dragon-studio-fireworks-13 (6s celebration barrage) as "HAPPY DUSSEHRA" appears!
                    self._post_demolition_stage = 2
                    self.audio.play_at_volume('ext_firework_2', 0.80)
                    # Celestial Flower Shower (Pushpa Vrishti) burst to celebrate the victory message
                    for _ in range(35):
                        self.psystem.add_flower_petal(x=random.uniform(30, WIDTH - 30))

            elif self.state == 'GREETING':
                self.simulate_destruction(dt)
                self._post_demolition_timer += dt
                # Continuous graceful floral shower during the greeting message
                if random.random() < 0.65 and not self.paused:
                    for _ in range(random.randint(1, 3)):
                        self.psystem.add_flower_petal()
                # Audio 3: freesound_community-fireworks-29629 (36.5s grand finale fireworks display)
                # kicks in after the initial barrages crest into the full celebration
                if self._post_demolition_stage == 2 and self._post_demolition_timer >= 8.5:
                    self._post_demolition_stage = 3
                    self.audio.play_at_volume('ext_firework_big', 0.75)
                elif self._post_demolition_stage == 3 and self._post_demolition_timer >= 45.0:
                    # Loop the celebration audio if remaining on greeting screen
                    self._post_demolition_timer = 8.5
                    self.audio.play_at_volume('ext_firework_big', 0.70)

            # Update Particle Physics & Fireworks
            self.psystem.update(dt)

            # Render Scene onto pre-allocated backbuffer (no per-frame allocation)
            render_surface = self._render_surface
            render_surface.fill((0, 0, 0))
            self.draw_background(render_surface)
            self.fireworks(render_surface, dt)
            self.draw_rama(render_surface, draw_progress)
            self.draw_ravana(render_surface)
            self.draw_bow_and_arrow(render_surface)
            self.fire_and_smoke(render_surface)
            self.psystem.draw_petals(render_surface, pg_module=pg)
            self.transitions(render_surface, dt)
            self.final_greeting(render_surface)

            # Draw Pause Overlay if paused (reuse pre-allocated surface)
            if self.paused:
                pause_overlay = self._pause_overlay
                pause_overlay.fill((0, 0, 0, 110))
                p_text = self.font_subtitle.render("PAUSED  -  Press [P] to Resume", True, (255, 235, 160))
                pw = p_text.get_width()
                ph = p_text.get_height()
                px = WIDTH // 2 - pw // 2
                py = HEIGHT // 2 - ph // 2
                pg.draw.rect(pause_overlay, (20, 15, 30, 220), (px - 22, py - 12, pw + 44, ph + 24), border_radius=8)
                pg.draw.rect(pause_overlay, COLOR_GOLD, (px - 22, py - 12, pw + 44, ph + 24), 2, border_radius=8)
                pause_overlay.blit(p_text, (px, py))
                render_surface.blit(pause_overlay, (0, 0))

            # Draw Slow-Mo indicator if active
            if self.slow_mo and not self.paused:
                s_text = self.font_ui.render("[SLOW-MOTION 0.35x ACTIVE]", True, (255, 215, 0))
                render_surface.blit(s_text, (24, 46))

            # Apply Screen Shake
            shake_x, shake_y = 0, 0
            if self.screen_shake > 0.1:
                shake_x = int(random.uniform(-self.screen_shake, self.screen_shake))
                shake_y = int(random.uniform(-self.screen_shake, self.screen_shake))

            scr_w, scr_h = self.screen.get_size()
            if (scr_w, scr_h) == (WIDTH, HEIGHT):
                self.screen.fill((0, 0, 0))
                self.screen.blit(render_surface, (shake_x, shake_y))
            else:
                if self._scaled_surface is None or self._scaled_surface.get_size() != (scr_w, scr_h):
                    self._scaled_surface = pg.Surface((scr_w, scr_h))
                pg.transform.smoothscale(render_surface, (scr_w, scr_h), self._scaled_surface)
                self.screen.fill((0, 0, 0))
                self.screen.blit(self._scaled_surface, (shake_x, shake_y))
            pg.display.flip()

        pg.quit()
        sys.exit(0)


# ==============================================================================
# SECTION 5: TURTLE / TKINTER VECTOR ANIMATION ENGINE
# ==============================================================================
class DasaraTurtleEngine:
    def __init__(self):
        import turtle
        self.turtle = turtle
        self.screen = turtle.Screen()
        self.screen.setup(width=DEFAULT_WINDOW_WIDTH, height=DEFAULT_WINDOW_HEIGHT)
        self.screen.title(WINDOW_TITLE)
        self.screen.bgcolor('#060A1A')
        self.screen.tracer(0, 0)

        self.pen_bg = turtle.Turtle()
        self.pen_rama = turtle.Turtle()
        self.pen_ravana = turtle.Turtle()
        self.pen_vfx = turtle.Turtle()
        self.pen_text = turtle.Turtle()

        for p in (self.pen_bg, self.pen_rama, self.pen_ravana, self.pen_vfx, self.pen_text):
            p.hideturtle()
            p.speed(0)
            p.penup()

        self.state_time = 0.0
        self.state = 'INTRO'
        self.arrow_x = -360
        self.arrow_y = -60

        self.screen.listen()
        self.screen.onkey(self.exit_app, 'Escape')

    def exit_app(self):
        try:
            self.screen.bye()
        except Exception:
            pass
        sys.exit(0)

    def background(self):
        p = self.pen_bg
        p.clear()
        p.goto(-WIDTH//2, -180)
        p.fillcolor('#1C1218')
        p.begin_fill()
        for x, y in [(-WIDTH//2, -HEIGHT//2), (WIDTH//2, -HEIGHT//2), (WIDTH//2, -180)]:
            p.goto(x, y)
        p.end_fill()

        # Full Moon
        p.goto(380, 200)
        p.fillcolor('#FFF8E0')
        p.begin_fill()
        p.circle(42)
        p.end_fill()

        # Mandir Shikhara
        p.goto(100, -180)
        p.fillcolor('#1A162A')
        p.begin_fill()
        p.goto(100, 40)
        p.goto(150, 180)
        p.goto(200, 40)
        p.goto(200, -180)
        p.end_fill()

        p.goto(150, 180)
        p.fillcolor('#FF6600')
        p.begin_fill()
        p.goto(190, 195)
        p.goto(150, 210)
        p.end_fill()

        for dx in range(-480, 480, 160):
            p.goto(dx, -180)
            p.fillcolor('#8C3214')
            p.begin_fill()
            p.circle(10)
            p.end_fill()
            p.goto(dx, -172)
            p.fillcolor('#FF9900')
            p.begin_fill()
            p.circle(6)
            p.end_fill()

    def draw_rama(self, drawn=False):
        p = self.pen_rama
        p.clear()
        rx, ry = -380, -180

        # Body
        p.goto(rx, ry)
        p.fillcolor('#3E7DC5')
        p.begin_fill()
        p.goto(rx - 20, ry + 120)
        p.goto(rx + 25, ry + 120)
        p.goto(rx + 15, ry)
        p.end_fill()

        # Dhoti with gold border
        p.goto(rx - 25, ry)
        p.fillcolor('#F5B819')
        p.begin_fill()
        p.goto(rx - 25, ry + 60)
        p.goto(rx + 20, ry + 60)
        p.goto(rx + 20, ry)
        p.end_fill()
        p.goto(rx - 25, ry + 6)
        p.pencolor('#B41220')
        p.pensize(3)
        p.pendown()
        p.goto(rx + 20, ry + 6)
        p.penup()

        # Head & Golden Crown with Peacock feather
        p.goto(rx, ry + 140)
        p.fillcolor('#3E7DC5')
        p.begin_fill()
        p.circle(18)
        p.end_fill()

        p.goto(rx - 15, ry + 155)
        p.fillcolor('#FFD700')
        p.begin_fill()
        p.goto(rx + 15, ry + 155)
        p.goto(rx, ry + 190)
        p.end_fill()

        # Royal Golden Kirita Crest Gem Finial (replacing peacock feather)
        p.goto(rx, ry + 190)
        p.fillcolor('#FFD700')
        p.begin_fill()
        p.circle(5)
        p.end_fill()
        p.goto(rx, ry + 195)
        p.fillcolor('#DA182A')
        p.begin_fill()
        p.circle(2)
        p.end_fill()

        # Kodanda Bow
        p.goto(rx + 50, ry + 60)
        p.pencolor('#FFD700')
        p.pensize(4)
        p.pendown()
        p.goto(rx + 65, ry + 130)
        p.goto(rx + 50, ry + 200)
        p.penup()

        nock = (rx + 10, ry + 130) if drawn else (rx + 55, ry + 130)
        p.pencolor('#FFFFFF')
        p.pensize(2)
        p.goto(rx + 50, ry + 60)
        p.pendown()
        p.goto(nock)
        p.goto(rx + 50, ry + 200)
        p.penup()

    def draw_ravana(self, stage=0):
        p = self.pen_ravana
        p.clear()
        if stage >= 4:
            return

        rv_x, rv_y = 320, -180 + (stage * 30)

        # Scaffolding
        p.goto(rv_x - 120, -180)
        p.fillcolor('#5A3719')
        p.begin_fill()
        p.goto(rv_x + 120, -180)
        p.goto(rv_x + 100, -210)
        p.goto(rv_x - 100, -210)
        p.end_fill()

        color_dhoti = '#8A0E1A' if stage < 2 else '#331111'
        p.goto(rv_x - 65, rv_y)
        p.fillcolor(color_dhoti)
        p.begin_fill()
        p.goto(rv_x + 65, rv_y)
        p.goto(rv_x + 55, rv_y + 160)
        p.goto(rv_x - 55, rv_y + 160)
        p.end_fill()

        p.goto(rv_x - 45, rv_y + 60)
        p.fillcolor('#D4A019' if stage < 2 else '#553311')
        p.begin_fill()
        p.goto(rv_x + 45, rv_y + 60)
        p.goto(rv_x + 40, rv_y + 150)
        p.goto(rv_x - 40, rv_y + 150)
        p.end_fill()

        # Sunburst disc on chest
        p.goto(rv_x, rv_y + 105)
        p.fillcolor('#B41220' if stage < 2 else '#331111')
        p.begin_fill()
        p.circle(12)
        p.end_fill()

        # Exactly TWO Arms holding Chandrahas and Gada
        if stage < 3:
            p.pencolor('#FFD700')
            p.pensize(4)
            # Left arm holding sword
            p.goto(rv_x - 45, rv_y + 130)
            p.pendown()
            p.goto(rv_x - 90, rv_y + 120)
            p.goto(rv_x - 120, rv_y + 150)
            p.penup()
            # Right arm holding mace
            p.goto(rv_x + 45, rv_y + 130)
            p.pendown()
            p.goto(rv_x + 90, rv_y + 120)
            p.goto(rv_x + 120, rv_y + 150)
            p.penup()

        # Exactly 10 Heads
        head_spacing = 26
        for i in range(-4, 6):
            if stage >= 3 and abs(i) > 1:
                continue
            hx = rv_x + i * head_spacing
            hy = rv_y + 180 - abs(i) * 5
            hr = 16 if i == 0 else 12

            p.goto(hx, hy)
            p.fillcolor('#E4A076' if stage < 2 else '#442222')
            p.begin_fill()
            p.circle(hr)
            p.end_fill()

            p.goto(hx - hr, hy + hr)
            p.fillcolor('#FFD700')
            p.begin_fill()
            p.goto(hx + hr, hy + hr)
            p.goto(hx, hy + hr + (18 if i == 0 else 12))
            p.end_fill()

    def bow_and_arrow(self):
        p = self.pen_vfx
        p.clear()
        p.goto(self.arrow_x, self.arrow_y)
        p.pencolor('#FFD700')
        p.pensize(4)
        p.pendown()
        p.goto(self.arrow_x - 50, self.arrow_y)
        p.penup()
        p.goto(self.arrow_x, self.arrow_y)
        p.fillcolor('#FFFFFF')
        p.begin_fill()
        p.goto(self.arrow_x - 14, self.arrow_y + 7)
        p.goto(self.arrow_x - 14, self.arrow_y - 7)
        p.end_fill()

    def destruction(self, stage):
        p = self.pen_vfx
        p.clear()
        for _ in range(12 + stage * 8):
            fx = 320 + random.uniform(-60, 60)
            fy = -140 + random.uniform(-40, 160)
            p.goto(fx, fy)
            p.fillcolor(random.choice(['#FF3300', '#FF9900', '#FFD700', '#FFFFFF']))
            p.begin_fill()
            p.circle(random.randint(6, 20))
            p.end_fill()

    def fireworks(self):
        p = self.pen_vfx
        for _ in range(6):
            bx = random.randint(-450, 450)
            by = random.randint(40, 260)
            b_color = random.choice(['#FFD700', '#FF3366', '#33FF99', '#FF9900', '#CC66FF'])
            p.pencolor(b_color)
            p.pensize(2)
            for ang in range(0, 360, 45):
                rad = math.radians(ang)
                p.goto(bx, by)
                p.pendown()
                p.goto(bx + math.cos(rad) * 45, by + math.sin(rad) * 45)
                p.penup()

    def final_greeting(self):
        p = self.pen_text
        p.clear()
        p.goto(2, 68)
        p.pencolor('#3A1800')
        p.write("HAPPY DUSSEHRA", align="center", font=("Georgia", 58, "bold"))
        p.goto(0, 70)
        p.pencolor('#FFD700')
        p.write("HAPPY DUSSEHRA", align="center", font=("Georgia", 58, "bold"))

        p.goto(0, 20)
        p.pencolor('#FFE099')
        p.write("VICTORY OF GOOD OVER EVIL • VIJAYADASHAMI", align="center", font=("Georgia", 18, "normal"))

        p.goto(0, -280)
        p.pencolor('#A0A0B0')
        p.write("Press [ESC] to Exit", align="center", font=("Arial", 12, "normal"))

    def update_loop(self):
        self.state_time += 0.05

        if self.state == 'INTRO':
            self.background()
            self.draw_rama(drawn=False)
            self.draw_ravana(stage=0)
            if self.state_time > 2.5:
                self.state = 'AIM'
                self.state_time = 0.0

        elif self.state == 'AIM':
            self.draw_rama(drawn=True)
            if self.state_time > 1.8:
                self.state = 'FLY'
                self.state_time = 0.0
                self.arrow_x = -320

        elif self.state == 'FLY':
            self.draw_rama(drawn=False)
            self.arrow_x += 24
            self.bow_and_arrow()
            if self.arrow_x >= 320:
                self.state = 'DESTROY'
                self.state_time = 0.0

        elif self.state == 'DESTROY':
            stage = int(self.state_time / 1.0)
            self.draw_ravana(stage=stage)
            self.destruction(stage=stage)
            if self.state_time > 4.5:
                self.state = 'GREETING'
                self.state_time = 0.0

        elif self.state == 'GREETING':
            self.pen_vfx.clear()
            self.fireworks()
            self.final_greeting()

        self.screen.update()
        self.screen.ontimer(self.update_loop, 40)

    def run(self):
        self.background()
        self.draw_rama()
        self.draw_ravana()
        self.screen.update()
        self.screen.ontimer(self.update_loop, 40)
        self.turtle.done()


# ==============================================================================
# SECTION 6: ENTRY POINT DISPATCHER
# ==============================================================================
def main():
    use_turtle = '--turtle' in sys.argv
    has_pygame = False
    try:
        import pygame
        import numpy
        has_pygame = True
    except ImportError:
        has_pygame = False

    if use_turtle or not has_pygame:
        print("[INFO] Launching Vijayadashami Animation in Turtle Engine...")
        engine = DasaraTurtleEngine()
        engine.run()
    else:
        print("[INFO] Launching Vijayadashami Cinematic Animation in Pygame Engine (2880x1800 Fullscreen 60FPS)...")
        engine = DasaraCinematicEngine()
        engine.run()


if __name__ == '__main__':
    main()
