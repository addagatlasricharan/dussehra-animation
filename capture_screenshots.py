"""
Automated Headless Screenshot Generator for Dussehra Animation.
Runs the Pygame engine headlessly using dummy drivers and captures
high-resolution keyframe snapshots for repository documentation.

Usage:
    python capture_screenshots.py
"""

import os
import sys
import importlib.util
from pathlib import Path

# Enable headless dummy drivers before importing pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

def capture():
    script_path = Path(__file__).parent / "Happy Dussehra Animation.py"
    if not script_path.exists():
        print(f"Error: Could not locate '{script_path}'")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("dasara", str(script_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    out_dir = Path(__file__).parent / "screenshots"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Initializing headless cinematic engine...")
    engine = mod.DasaraCinematicEngine()

    dt = 1.0 / 60.0
    total_time = 0.0

    targets = {
        "01_night_sanctum_intro": 1.6,
        "02_lord_rama_drawing_bow": 4.9,
        "03_brahmastra_flight": 7.42,
        "04_ravana_effigy_burning": 11.8,
        "05_bonfire_and_sky_lanterns": 14.8,
        "06_festive_fireworks_climax": 17.2,
        "07_happy_dussehra_greeting": 23.5,
    }

    captured = set()
    draw_progress = 0.0

    print(f"Stepping simulation to capture {len(targets)} keyframes...")
    while total_time < 25.0:
        engine.state_time += dt
        engine.total_time += dt
        total_time += dt

        if engine.state == "INTRO":
            if engine.state_time > 3.0:
                engine.state = "RAMA_AIM"
                engine.state_time = 0.0
        elif engine.state == "RAMA_AIM":
            draw_progress = min(1.0, engine.state_time / 2.8)
            if engine.state_time > 2.8:
                engine.state = "ARROW_CHARGE"
                engine.state_time = 0.0
        elif engine.state == "ARROW_CHARGE":
            draw_progress = 1.0
            tip_x, tip_y = engine.arrow_start
            for _ in range(3):
                ang = mod.random.uniform(0, mod.math.pi * 2)
                dist = mod.random.uniform(20, 42)
                engine.psystem.particles.append(
                    mod.Particle(
                        tip_x + mod.math.cos(ang) * dist,
                        tip_y + mod.math.sin(ang) * dist,
                        -mod.math.cos(ang) * 55,
                        -mod.math.sin(ang) * 55,
                        (255, 240, 140),
                        2.5,
                        0.4,
                        "spark",
                    )
                )
            if engine.state_time > 1.2:
                engine.state = "ARROW_FLY"
                engine.state_time = 0.0
                engine.arrow_active = True
                engine.arrow_pos = list(engine.arrow_start)
        elif engine.state == "ARROW_FLY":
            draw_progress = 0.0
            t_fly = min(1.0, engine.state_time / 0.95)
            engine.arrow_pos[0] = (
                engine.arrow_start[0] * (1.0 - t_fly) + engine.arrow_target[0] * t_fly
            )
            arc_y = -mod.math.sin(t_fly * mod.math.pi) * 35
            engine.arrow_pos[1] = (
                engine.arrow_start[1] * (1.0 - t_fly) + engine.arrow_target[1] * t_fly
            ) + arc_y
            vx_tangent = engine.arrow_target[0] - engine.arrow_start[0]
            vy_tangent = (
                engine.arrow_target[1] - engine.arrow_start[1]
            ) - 35.0 * mod.math.pi * mod.math.cos(t_fly * mod.math.pi)
            engine.arrow_angle = mod.math.atan2(vy_tangent, vx_tangent)
            for _ in range(6):
                engine.psystem.add_spark_particle(
                    engine.arrow_pos[0], engine.arrow_pos[1], speed_range=(25, 95)
                )
            if t_fly >= 1.0:
                engine.state = "DESTRUCTION"
                engine.state_time = 0.0
                engine.destruction_timer = 0.0
                engine.arrow_active = False
                engine.white_flash = 1.0
                engine.screen_shake = 12.0
        elif engine.state == "DESTRUCTION":
            engine.simulate_destruction(dt)
            if engine.destruction_timer > 7.0:
                engine.state = "CLIMAX"
                engine.state_time = 0.0
                engine.white_flash = 0.6
                engine._post_demolition_stage = 1
                engine._post_demolition_timer = 0.0
        elif engine.state == "CLIMAX":
            engine.simulate_destruction(dt)
            engine._post_demolition_timer += dt
            if mod.random.random() < 0.40:
                for _ in range(mod.random.randint(1, 3)):
                    engine.psystem.add_flower_petal()
            if engine.state_time > 3.5:
                engine.state = "GREETING"
                engine.state_time = 0.0
                engine._post_demolition_stage = 2
                for _ in range(35):
                    engine.psystem.add_flower_petal(
                        x=mod.random.uniform(30, mod.WIDTH - 30)
                    )
        elif engine.state == "GREETING":
            engine.simulate_destruction(dt)
            engine._post_demolition_timer += dt
            if mod.random.random() < 0.65:
                for _ in range(mod.random.randint(1, 3)):
                    engine.psystem.add_flower_petal()

        engine.psystem.update(dt)

        # Full offscreen frame render
        s = engine._render_surface
        s.fill((0, 0, 0))
        engine.draw_background(s)
        engine.fireworks(s, dt)
        engine.draw_rama(s, draw_progress)
        engine.draw_ravana(s)
        engine.draw_bow_and_arrow(s)
        engine.fire_and_smoke(s)
        engine.psystem.draw_petals(s, pg_module=pygame)
        engine.transitions(s, dt)
        engine.final_greeting(s)

        for name, t_target in targets.items():
            if name not in captured and total_time >= t_target:
                filepath = out_dir / f"{name}.png"
                pygame.image.save(s, str(filepath))
                print(f"  [+] Saved: {filepath.name} (t={total_time:.2f}s, state={engine.state})")
                captured.add(name)

    # Capture Isolated Background (no characters)
    print("Capturing isolated background...")
    bg_surf = pygame.Surface((1280, 800))
    engine.draw_background(bg_surf)
    bg_path = out_dir / "isolated_background.png"
    pygame.image.save(bg_surf, str(bg_path))
    print(f"  [+] Saved: {bg_path.name}")

    # Capture Isolated Lord Rama with Transparent Background
    print("Capturing Lord Rama closeup (transparent)...")
    rama_canvas = pygame.Surface((1280, 800), pygame.SRCALPHA)
    engine.draw_rama(rama_canvas, draw_progress=0.9)
    rama_crop = rama_canvas.subsurface(pygame.Rect(50, 140, 380, 430))
    rama_path = out_dir / "closeup_lord_rama.png"
    pygame.image.save(rama_crop, str(rama_path))
    print(f"  [+] Saved: {rama_path.name}")

    # Capture Isolated King Ravana with Transparent Background
    print("Capturing King Ravana closeup (transparent)...")
    ravana_canvas = pygame.Surface((1280, 800), pygame.SRCALPHA)
    engine.draw_ravana(ravana_canvas)
    ravana_crop = ravana_canvas.subsurface(pygame.Rect(720, 110, 520, 460))
    ravana_path = out_dir / "closeup_king_ravana.png"
    pygame.image.save(ravana_crop, str(ravana_path))
    print(f"  [+] Saved: {ravana_path.name}")

    print("All screenshots and character closeups successfully finished!")

if __name__ == "__main__":
    capture()
