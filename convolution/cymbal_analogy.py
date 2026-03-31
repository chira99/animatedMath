from manim import *
import numpy as np

SIGNAL_COLOR = "#58C4DD"
KERNEL_COLOR = "#FF6B6B"
OUTPUT_COLOR = "#A8FF78"

class CymbalAnalogyScene(Scene):
    def construct(self):
        self._beat1_hook()
        self._beat2_analogy()

    # ── Beat 1: title ─────────────────────────────────────────────
    def _beat1_hook(self):
        title = Text("An intuitive introduction to convolution.", font_size=40)
        self.play(Write(title), run_time=3)
        self.wait(1)
        self.play(FadeOut(title), run_time=1)

    # ── Beat 2: cymbal analogy → flip-and-slide convolution ───────
    def _beat2_analogy(self):
        impulse_positions = [(0, 1.0), (1, 1.0), (3, 0.5)]

        # ── Phase 1: expanding cymbal arc ────────────────────────
        ax = Axes(
            x_range=[0, 5.5, 1], y_range=[-2, 2, 1],
            x_length=8, y_length=5,
            tips=True,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": list(range(0, 6))},
        )
        t_lbl = ax.get_x_axis_label(MathTex("t"))

        lbl1 = Text("Consider hitting a cymbal once…", font_size=40)
        self.play(Write(lbl1), run_time=1.5)
        self.wait(0.5)
        self.play(lbl1.animate.scale(0.65).to_edge(UP), run_time=0.8)
        self.wait(0.3)
        self.play(Create(ax), Write(t_lbl), run_time=0.5)
        self.wait(0.3)

        origin  = ax.c2p(0, 0)
        r_track = ValueTracker(0.01)

        def make_arc():
            r       = r_track.get_value()
            scene_r = (r / 5.0) * 4
            opacity = max(0.0, 1.0 - r / 5.0)
            arc = Arc(
                radius=scene_r, start_angle=-PI / 2, angle=PI,
                color=SIGNAL_COLOR, stroke_width=3,
            )
            arc.move_arc_center_to(origin)
            arc.set_stroke(opacity=opacity)
            return arc

        cymbal_arc = always_redraw(make_arc)
        self.add(cymbal_arc)
        self.play(r_track.animate.set_value(6.0), run_time=2.5)
        self.remove(cymbal_arc)

        # ── Phase 2: impulse response h(t) = e^{-t} ─────────────
        ax1 = Axes(
            x_range=[0, 5.5, 1], y_range=[0, 1.5, 1],
            x_length=8, y_length=3.5,
            tips=True,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": list(range(0, 6)), "numbers_to_exclude": []},
            y_axis_config={"numbers_to_include": [1], "decimal_number_config": {"num_decimal_places": 0}},
        )
        lbl2   = Text("It leaves a decaying impulse response h(t)", font_size=26).to_edge(UP)
        t_lbl1 = ax1.get_x_axis_label(MathTex("t"))
        self.play(
            ReplacementTransform(ax, ax1),
            ReplacementTransform(t_lbl, t_lbl1),
            ReplacementTransform(lbl1, lbl2),
            run_time=1,
        )

        def h_fn(t):
            return float(np.exp(-t))

        h_graph = ax1.plot(h_fn, x_range=[0, 5, 0.05], color=SIGNAL_COLOR)
        h_tex   = MathTex("h(t)", color=SIGNAL_COLOR, font_size=40).next_to(
            ax1.c2p(0.4, h_fn(0.4)), UR, buff=0.15,
        )
        self.play(Create(h_graph), Write(h_tex), run_time=2)
        self.wait(2)
        self.play(FadeOut(VGroup(h_graph, h_tex, lbl2)), run_time=0.5)

        # ── Phase 3: input signal x(t) — impulses at t = 0, 1, 3 ─
        x_group = VGroup(*[
            Arrow(ax1.c2p(pos, 0), ax1.c2p(pos, amp),
                  color=KERNEL_COLOR, stroke_width=3, buff=0, tip_length=0.2)
            for pos, amp in impulse_positions
        ])
        x_tex = MathTex("x(t)", color=KERNEL_COLOR, font_size=40).next_to(
            ax1.c2p(-0.3, 1.05), UL, buff=0.1,
        )
        lbl3 = Text(
            "Let's hit the cymbal at t = 0, 1, 3; softly at t = 3 ...",
            font_size=26,
        ).to_edge(UP)
        self.play(Write(lbl3), run_time=1.5)
        self.wait(1)
        self.play(FadeIn(x_group), Write(x_tex), run_time=2)
        self.wait(3)
        self.play(FadeOut(VGroup(ax1, t_lbl1, x_group, x_tex, lbl3)), run_time=1)

        # ── Phase 4: flip-and-slide convolution ──────────────────
        tau_ax = Axes(
            x_range=[-5, 8.5, 1], y_range=[0, 1.8, 0.5],
            x_length=10, y_length=3.5,
            tips=True,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": list(range(-5, 9)), "numbers_to_exclude": []},
            y_axis_config={"numbers_to_include": [1], "decimal_number_config": {"num_decimal_places": 0}},
        )
        tau_lbl = tau_ax.get_x_axis_label(MathTex(r"\tau"))

        msg_line1 = Text("The cymbal's amplitude is the convolution of", font_size=34)
        msg_line2 = VGroup(
            Text("the hitting pattern", font_size=34),
            MathTex("x(t)", color=KERNEL_COLOR, font_size=42),
            Text("and the impulse response", font_size=34),
            MathTex("h(t)", color=SIGNAL_COLOR, font_size=42),
        ).arrange(RIGHT, buff=0.18)
        msg = VGroup(msg_line1, msg_line2).arrange(DOWN, buff=0.45)
        self.play(Write(msg), run_time=2.5)
        self.wait(2.5)
        self.play(FadeOut(msg), run_time=0.8)

        eq = MathTex(
            r"y(t) = (x \ast h)(t) = \int x(\tau)\, h(t - \tau)\, d\tau",
            font_size=40,
        )
        self.play(Write(eq), run_time=2)
        self.wait(0.5)
        self.play(eq.animate.to_edge(UP, buff=0.15), run_time=1)
        self.play(Create(tau_ax), Write(tau_lbl), run_time=1)

        x_conv = VGroup(*[
            Arrow(tau_ax.c2p(pos, 0), tau_ax.c2p(pos, amp),
                  color=KERNEL_COLOR, stroke_width=3, buff=0, tip_length=0.2)
            for pos, amp in impulse_positions
        ])
        x_conv_lbl = MathTex(r"x(\tau)", color=KERNEL_COLOR, font_size=36).next_to(
            tau_ax.c2p(-0.3, 1.1), UL, buff=0.1,
        )
        self.play(FadeIn(x_conv), Write(x_conv_lbl), run_time=1)

        h_tau_curve = tau_ax.plot(
            lambda tau: float(np.exp(-tau)),
            x_range=[0, 5, 0.05], color=SIGNAL_COLOR,
        )
        h_tau_lbl = MathTex(r"h(\tau)", color=SIGNAL_COLOR, font_size=36).next_to(
            tau_ax.c2p(0.2, 1.1), UR, buff=0.1,
        )
        self.play(Create(h_tau_curve), Write(h_tau_lbl), run_time=1.5)
        self.wait(0.5)

        h_neg_lbl = MathTex(r"h(-\tau)", color=SIGNAL_COLOR, font_size=36).next_to(
            tau_ax.c2p(-0.5, 0.85), UL, buff=0.1,
        )
        flip_txt = Text("Flip h(τ) → h(−τ)", font_size=24, color=YELLOW).next_to(
            tau_ax, DOWN, buff=0.15,
        )
        self.play(
            Write(flip_txt),
            h_tau_curve.animate.flip(UP, about_point=tau_ax.c2p(0, 0)),
            ReplacementTransform(h_tau_lbl, h_neg_lbl),
            run_time=1.5,
        )
        self.wait(0.5)
        self.play(FadeOut(flip_txt), run_time=0.5)

        # Slide h(t−τ) across x(τ) and accumulate y(t)
        t_track = ValueTracker(0.0)

        def make_h_slide():
            t_val = t_track.get_value()
            lo    = max(-5.0, t_val - 5.0)
            hi    = min(8.5, t_val)
            if hi <= lo + 0.05:
                return VMobject()
            return tau_ax.plot(
                lambda tau: float(np.exp(-(t_val - tau))),
                x_range=[lo, hi, 0.05], color=SIGNAL_COLOR,
            )

        def make_h_slide_lbl():
            t_val = t_track.get_value()
            lbl_x = min(max(t_val, -4.5), 7.2)
            return MathTex(r"h(t-\tau)", color=SIGNAL_COLOR, font_size=36).next_to(
                tau_ax.c2p(lbl_x, 1.0), UR, buff=0.15,
            )

        # y(t) drawn as 3 separate smooth segments to avoid discontinuity artefacts at t=1 and t=3
        Y1_BOT = float(np.exp(-1.0))
        Y1_TOP = float(np.exp(-1.0) + 1.0)
        Y3_BOT = float(np.exp(-3.0) + np.exp(-2.0))
        Y3_TOP = float(np.exp(-3.0) + np.exp(-2.0) + 0.5)

        def build_y_segments(t_end):
            EPS   = 1e-3
            parts = VGroup()
            s1 = min(t_end, 1.0 - EPS)
            if s1 > EPS:
                parts.add(tau_ax.plot(
                    lambda s: float(np.exp(-s)),
                    x_range=[0.0, s1, 0.02], color=OUTPUT_COLOR,
                ))
            if t_end >= 1.0:
                parts.add(Line(
                    tau_ax.c2p(1.0, Y1_BOT), tau_ax.c2p(1.0, Y1_TOP),
                    color=OUTPUT_COLOR, stroke_width=2,
                ))
                s2 = min(t_end, 3.0 - EPS)
                if s2 > 1.0:
                    parts.add(tau_ax.plot(
                        lambda s: float(np.exp(-s) + np.exp(-(s - 1.0))),
                        x_range=[1.0, s2, 0.02], color=OUTPUT_COLOR,
                    ))
            if t_end >= 3.0:
                parts.add(Line(
                    tau_ax.c2p(3.0, Y3_BOT), tau_ax.c2p(3.0, Y3_TOP),
                    color=OUTPUT_COLOR, stroke_width=2,
                ))
                s3 = min(t_end, 7.9)
                if s3 > 3.0:
                    parts.add(tau_ax.plot(
                        lambda s: float(
                            np.exp(-s) + np.exp(-(s - 1.0)) + 0.5 * np.exp(-(s - 3.0))
                        ),
                        x_range=[3.0, s3, 0.02], color=OUTPUT_COLOR,
                    ))
            return parts

        def make_y():
            t_val = t_track.get_value()
            if t_val <= 0.0:
                return VMobject()
            return build_y_segments(t_val)

        # t counter — left-anchored so the label never shifts while digits change
        _tc_ref  = Text("t = 0.0", font_size=24, color=YELLOW)
        _tc_ref.move_to(tau_ax.get_bottom() + DOWN * 0.35)
        _tc_left = _tc_ref.get_left()
        _tc_y    = _tc_ref.get_center()[1]

        h_slide     = always_redraw(make_h_slide)
        h_slide_lbl = always_redraw(make_h_slide_lbl)
        y_accum     = always_redraw(make_y)
        t_counter   = always_redraw(lambda: Text(
            f"t = {t_track.get_value():.1f}", font_size=24, color=YELLOW,
        ).align_to(_tc_left, LEFT).set_y(_tc_y))
        y_label = MathTex("y(t)", color=OUTPUT_COLOR, font_size=36).next_to(
            tau_ax.c2p(-0.1, 1.65), UL, buff=0.1,
        )

        self.play(FadeOut(VGroup(h_tau_curve, h_neg_lbl)), run_time=0.3)
        self.add(h_slide, h_slide_lbl, y_accum, t_counter)
        self.play(Write(y_label), run_time=0.5)
        self.play(t_track.animate.set_value(8.0), run_time=12, rate_func=linear)
        self.wait(0.5)

        # Freeze always_redraw objects as static snapshots before fading out
        T_FINAL        = 8.0
        h_frozen_curve = tau_ax.plot(
            lambda tau: float(np.exp(-(T_FINAL - tau))),
            x_range=[T_FINAL - 5.0, T_FINAL, 0.05], color=SIGNAL_COLOR,
        )
        h_frozen_lbl = MathTex(r"h(t-\tau)", color=SIGNAL_COLOR, font_size=36).next_to(
            tau_ax.c2p(7.2, 1.0), UR, buff=0.15,
        )
        y_frozen         = build_y_segments(T_FINAL)
        t_counter_frozen = Text("t = 8.0", font_size=24, color=YELLOW).align_to(
            _tc_left, LEFT,
        ).set_y(_tc_y)

        self.remove(h_slide, h_slide_lbl, y_accum, t_counter)
        self.add(h_frozen_curve, h_frozen_lbl, y_frozen, t_counter_frozen)

        # Fade out x and h; relabel τ → t to show y(t) alone
        t_lbl_final = tau_ax.get_x_axis_label(MathTex("t"))
        self.play(
            FadeOut(VGroup(x_conv, x_conv_lbl, h_frozen_curve, h_frozen_lbl,
                           eq, t_counter_frozen)),
            ReplacementTransform(tau_lbl, t_lbl_final),
            run_time=1.5,
        )
        self.wait(1)
        self.play(FadeOut(VGroup(tau_ax, t_lbl_final, y_frozen, y_label)), run_time=1)
