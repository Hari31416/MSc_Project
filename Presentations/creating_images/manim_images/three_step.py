from manim import *
import numpy as np
import os

BACKGROUND_COLOR = WHITE
TEXT_COLOR = BLACK
config.background_color = BACKGROUND_COLOR
WAVE_FUNCTION_COLOR = "#ff0000"
BLUE_C = "#0d1d85"
GREEN_C = "#1f5c17"


class ThreeStep(ThreeDScene):
    def construct(self):
        pass

    def plot_arrow(self):
        arrow = VGroup()
        point = self.axes.c2p(2.88, -3)

        h_line_0_start = self.axes.c2p(-0.58, -3)
        h_line_0_end = point
        h_line_0 = Arrow(
            h_line_0_start, h_line_0_end, color=WAVE_FUNCTION_COLOR, buff=0
        )
        h_line_0 = DashedVMobject(h_line_0)
        arrow.add(h_line_0)

        hline_1_end = self.axes.c2p(4.5, -3)
        hline_1 = Line(point, hline_1_end, color=WAVE_FUNCTION_COLOR)
        arrow.add(hline_1)
        arc_start = hline_1_end - 0.01 * RIGHT

        arc_end = self.axes.c2p(4.5, 3)
        arc = ArcBetweenPoints(arc_start, arc_end, color=WAVE_FUNCTION_COLOR)
        arrow.add(arc)

        h_line_2_start = arc_end + 0.01 * RIGHT
        h_line_2_end = self.axes.c2p(0, 3)
        h_line_2 = Arrow(
            h_line_2_start,
            h_line_2_end,
            color=WAVE_FUNCTION_COLOR,
            buff=0,
            stroke_width=4,
        )
        arrow.add(h_line_2)

        # h_line_3_start = h_line_2_end + 0.5 * RIGHT
        # h_line_3_end_x = h_line_3_start[0]
        # h_line_3_end_y = -3
        # h_line_3_end = self.axes.c2p(h_line_3_end_x, h_line_3_end_y)
        # h_line_3 = Arrow(
        #     h_line_3_start,
        #     h_line_3_end,
        #     color=WAVE_FUNCTION_COLOR,
        #     buff=0,
        #     stroke_width=4,
        # )
        # arrow.add(h_line_3)

        label_0 = Text("Tunneling\nIonization", color=WAVE_FUNCTION_COLOR).scale(0.4)
        label_0.move_to(self.axes.c2p(1.5, -2.9))
        arrow.add(label_0)
        label_1 = Text("Recombination", color=WAVE_FUNCTION_COLOR).scale(0.4)
        label_1.next_to(h_line_2, DOWN, buff=0.01)
        arrow.add(label_1)
        label_2 = Text("Propagation", color=WAVE_FUNCTION_COLOR).scale(0.4)
        label_2.next_to(arc, LEFT, buff=0.01).rotate(90 * DEGREES).shift(1.8 * RIGHT)
        arrow.add(label_2)

        # arc_full_start = point
        # arc_full_end = self.axes.c2p(1, 3)
        # arc_full = ArcBetweenPoints(
        #     arc_full_start, arc_full_end, color=RED, angle=120 * DEGREES
        # )
        # arrow_f_start = arc_full_end + 0.01 * RIGHT
        # arrow_f_end = self.axes.c2p(0, 3)
        # arrow_f = Arrow(arrow_f_start, arrow_f_end, color=RED, buff=0)
        # arrow.add(arrow_f)
        # arrow.add(arc_full)

        return arrow

    def plot_lines(self):
        axes = Axes(
            x_range=[-5, 5.0, 0.1],
            y_range=[-5, 5, 0.1],
            x_length=10,
            axis_config={"color": GREEN},
            tips=False,
        )
        self.axes = axes
        hline = Arrow(axes.c2p(-6, 0), axes.c2p(6, 0), color=TEXT_COLOR, stroke_width=4)
        hline_label = MathTex("x", color=TEXT_COLOR).move_to(axes.c2p(5, -0.5))
        vline = Arrow(axes.c2p(0, -6), axes.c2p(0, 6), color=TEXT_COLOR, stroke_width=4)
        vline_label = MathTex("E", color=TEXT_COLOR).move_to(axes.c2p(-0.5, 4))
        self.add(hline, vline, hline_label, vline_label)

        def l0(x):
            return -1 / x**2

        def l1(x):
            return -x - 1 / x**2

        def l2(x):
            return -x

        potential = axes.plot(lambda x: l0(x), color=BLACK, use_smoothing=False)
        potential_p = axes.plot(lambda x: l1(x), color=BLUE_C, use_smoothing=False)
        electric = axes.plot(lambda x: l2(x), color=GREEN_C, use_smoothing=False)

        potential_label = Text("Unperturbed Potential", color=TEXT_COLOR).scale(0.4)
        potential_label.move_to(axes.c2p(2.0, 0.2))
        potential_p_label = Text("Perturbed Potential", color=BLUE_C).scale(0.4)
        potential_p_label.move_to(axes.c2p(-3.0, 1.0))
        electric_label = Text("Electric Potential", color=GREEN_C).scale(0.4)
        electric_label.move_to(axes.c2p(-1.0, 2.3))

        plots = VGroup(potential_p, electric, potential)
        labels = VGroup(potential_p_label, electric_label, potential_label)
        return plots, labels

    def bound_wave_function(self):
        axes = self.axes
        bound_state = VGroup()

        def bound(x):
            return 4 * np.sin(0.5 * np.pi * x)

        bound_wf = axes.plot(bound, color=WAVE_FUNCTION_COLOR, use_smoothing=False)
        bound_wf_label = Text("Initial State", color=WAVE_FUNCTION_COLOR).scale(3)
        bound_wf_label.next_to(bound_wf, DOWN, buff=0.3)
        bound_state.add(bound_wf, bound_wf_label)
        return bound_state

    def decaying_wave_function(self):
        axes2 = self.axes
        decaying_state = VGroup()

        def decaying(x):
            return np.exp(-1 * x) - 0.1 * x

        decaying_wf = axes2.plot(
            decaying, color=WAVE_FUNCTION_COLOR, use_smoothing=False, x_range=(0, 5)
        )
        decaying_wf_label = Text(
            "Exponential\n\tDecay", color=WAVE_FUNCTION_COLOR
        ).scale(1.1)
        decaying_wf_label.next_to(decaying_wf, DOWN, buff=0.1)
        decaying_state.add(decaying_wf, decaying_wf_label)
        return decaying_state

    def final_wave_function(self):
        axes = self.axes
        final_state = VGroup()

        def final(x):
            return 1 * np.cos(0.5 * np.pi * x)

        final_wf = axes.plot(final, color=WAVE_FUNCTION_COLOR, use_smoothing=False)
        final_wf_label = Text("Final State", color=WAVE_FUNCTION_COLOR).scale(3)
        final_wf_label.next_to(final_wf, UP, buff=0.3)
        final_state.add(final_wf, final_wf_label)
        return final_state

        # self.wait(5)


class ThreeStepOne(ThreeStep):
    def construct(self):
        self.create_lines_arrow()

    def create_lines_arrow(self):
        plots, labels = self.plot_lines()
        point = self.axes.c2p(2.88, -3)
        dot = Dot(color=BLACK, point=point, z_index=1).scale(1.5)
        arrow = self.plot_arrow()
        d_arrow_start = self.axes.c2p(-0.1, -3)
        d_arrow_end = self.axes.c2p(-0.1, 0)
        darrow = DoubleArrow(
            start=d_arrow_start,
            end=d_arrow_end,
            color=BLACK,
            buff=0,
            tip_length=0.2,
            stroke_width=4,
        )
        darrow = DashedVMobject(darrow, num_dashes=10)
        darrow_label = MathTex("I_p", color=BLACK).scale(0.8)
        darrow_label.next_to(darrow, LEFT, buff=0.05)
        self.add(plots, labels, dot, arrow, darrow, darrow_label)

        # self.camera.set_zoom(1.2)


class ThreeStepTwo(ThreeStep):
    def construct(self):
        self.create_lines_waves()

    def create_lines_waves(self):
        plots, labels = self.plot_lines()
        self.add(plots, labels)
        bound_state = self.bound_wave_function()
        bound_state.scale(0.13).move_to(self.axes.c2p(0.15, -3))
        self.add(bound_state)

        decaying = self.decaying_wave_function()
        decaying.scale(0.36).move_to(self.axes.c2p(1.7, -3))
        self.add(decaying)

        final = self.final_wave_function()
        final.scale(0.13).move_to(self.axes.c2p(3.25, -2.6))
        self.add(final)
        horizline_start = self.axes.c2p(-0.8, -2.8)
        horizline_end = self.axes.c2p(4.25, -2.8)
        horizline = DashedLine(horizline_start, horizline_end, color=BLACK)
        self.add(horizline)
        self.camera.set_zoom(1.2)


class ThreeStepFinal(ThreeStep):
    def construct(self):
        fig_one = self.create_lines_arrow()
        fig_two = self.create_lines_waves()
        fig_one.scale(0.5)
        # fig_one.scale(0.5).move_to(LEFT * 3.5)
        # fig_two.scale(0.5).move_to(RIGHT * 3.5)
        # self.add(fig_one, fig_two)
        self.add(fig_one)

    def create_lines_arrow(self):
        fig_one = VGroup()
        plots, labels = self.plot_lines()
        point = self.axes.c2p(2.88, -3)
        dot = Dot(color=BLACK, point=point, z_index=1).scale(1.5)
        arrow = self.plot_arrow()
        fig_one.add(plots, labels, dot, arrow)
        return fig_one

    def create_lines_waves(self):
        fig_two = VGroup()
        plots, labels = self.plot_lines()
        fig_two.add(plots, labels)
        bound_state = self.bound_wave_function()
        bound_state.scale(0.13).move_to(self.axes.c2p(0.15, -3))
        fig_two.add(bound_state)

        decaying = self.decaying_wave_function()
        decaying.scale(0.36).move_to(self.axes.c2p(1.7, -3))
        fig_two.add(decaying)

        final = self.final_wave_function()
        final.scale(0.13).move_to(self.axes.c2p(3.25, -2.6))
        fig_two.add(final)
        horizline_start = self.axes.c2p(-0.8, -2.8)
        horizline_end = self.axes.c2p(4.25, -2.8)
        horizline = DashedLine(horizline_start, horizline_end, color=BLACK)
        fig_two.add(horizline)
        return fig_two


if __name__ == "__main__":
    module_name = os.path.basename(__file__)
    command_A = "manim -v CRITICAL -p -qk --disable_caching --renderer=opengl "
    # command_A = "manim -v CRITICAL -p -qh --disable_caching --renderer=cairo -o /media/hari31416/Hari_SSD/Users/harik/Desktop/MSc_Project/Presentations/Reports/Sem_4_Major/images/three_step_two.png "
    command_A = "manim -v CRITICAL -p -qh --disable_caching --renderer=cairo -o /media/hari31416/Hari_SSD/Users/harik/Desktop/MSc_Project/Presentations/Reports/Sem_4_Major/three_step_two.png "
    command_B = module_name + " ThreeStepTwo"
    os.system(command_A + command_B)
