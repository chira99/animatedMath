# Animated Math

Visual explainers for mathematical concepts, built with [Manim Community](https://www.manim.community/).

## Videos

### 1. Convolution — Intuitively
> *What do reverb, blurring, and edge detection have in common? One operation explains them all.*

Builds intuition for convolution from first principles using a cymbal analogy:
- A single cymbal hit produces a decaying impulse response `h(t) = e^{-t}`
- Multiple hits at `t = 0, 1, 3` produce the input signal `x(t)`
- The total sound you hear is the convolution `y(t) = (x * h)(t)`
- Visualised step-by-step: fix `x(τ)`, flip `h(τ)` → `h(−τ)`, slide and accumulate `y(t)`

Read the full _Medium article_ here: [Convolution, Intuitively — What a Cymbal Can Teach You About Signal Processing](https://medium.com/@chiranthajk/convolution-intuitively-what-a-cymbal-can-teach-you-about-signal-processing-3834227859e4)

## Setup

**Requirements**
- Python 3.10+
- [Manim Community v0.20+](https://docs.manim.community/en/stable/installation.html)
- LaTeX (BasicTeX or MacTeX) for math rendering

```bash
git clone https://github.com/chira99/animatedMath.git
cd animatedMath
python -m venv venv
source venv/bin/activate
pip install manim
```

## Rendering

```bash
# Preview (480p)
manim -ql convolution/intuition.py IntuitionScene

# 720p
manim -qm convolution/intuition.py IntuitionScene

# 1080p 60fps
manim -qh convolution/intuition.py IntuitionScene
```

Output is saved to `media/videos/`.

## Project Structure

```
animatedMath/
├── convolution/
│   └── intuition.py    # Convolution intuition scene
└── media/              # Rendered output (git-ignored)
```

## Built With

- [Manim Community](https://www.manim.community/) — mathematical animation engine
