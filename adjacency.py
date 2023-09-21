from manim import *

# some basic rhythm patterns
p1 = [1, 0, 0, 0]
p2 = [0, 1, 1, 0, 1]
p3 = [0, 1, 0]

# helper functions
def visualize_pattern(notes:list, color=WHITE, opacity=0.5)->VGroup:
    # create beat squares
    beats = [Square().set_fill(color, opacity=0.5 if note else 0.0) for note in notes]
    # position squares next to each other
    for i in range(1, len(beats)): beats[i].next_to(beats[i-1], buff=0.0)
    # center rhythm group
    return VGroup(*beats).center()

def get_lr_lines(objs:VGroup, color=RED, stroke_width=DEFAULT_STROKE_WIDTH*4)->tuple[Line]:
    start = Line(objs.get_corner(UL), objs.get_corner(DL), stroke_width=stroke_width).set_color(color)
    end = Line(objs.get_corner(UR), objs.get_corner(DR), stroke_width=stroke_width).set_color(color)
    return start, end


class BasicRhythm(Scene):
    def construct(self):

        rhythm = visualize_pattern(p2)
        start = Line(rhythm.get_corner(UL), rhythm.get_corner(DL), stroke_width=DEFAULT_STROKE_WIDTH*4).set_color(RED_A)
        end = Line(rhythm.get_corner(UR), rhythm.get_corner(DR), stroke_width=DEFAULT_STROKE_WIDTH*4).set_color(RED_A)

        self.add(rhythm)
        self.wait(2)
        self.add(start)
        self.play(Transform(start,end), run_time=2)
        self.wait(1)
        self.remove(start)
        self.wait(1)


# Scene 1: show a rhythm, animate a label in, add some more rhythms!
class RhythmLabeling(Scene):
    def construct(self):
        r1 = visualize_pattern(p1)
        r2 = visualize_pattern(p2)
        r3 = visualize_pattern(p3)

        l1 = Text("1:").next_to(r1, LEFT).scale(2)
        l2 = Text("2:").next_to(r2, LEFT).scale(2)
        l3 = Text("3:").next_to(r3, LEFT).scale(2)

        g1 = VGroup(l1, r1)
        g2 = VGroup(l2, r2.shift(RIGHT))
        g3 = VGroup(l3, r3.shift(RIGHT)).next_to(g2, DOWN).align_to(g2, LEFT)

        # show how we can label
        self.play(FadeIn(r1))
        self.play(r1.animate.move_to(RIGHT), FadeIn(l1))

        self.next_section("Add a few more patterns")
        self.remove(r1, l1)
        self.add(g1)
        self.play(g1.animate.next_to(g2, UP))
        self.play(g1.animate.align_to(g2, LEFT), FadeIn(g2, g3))


class NegatedRhythms(Scene):
    def construct(self):
        r1 = visualize_pattern(p1)
        
        l1 = Text("+1:").next_to(r1, LEFT).shift(LEFT).scale(2)
        l2 = Text("-1:").next_to(r1, LEFT).shift(LEFT).scale(2)

        self.add(l1, r1)
        self.wait(1)
        self.play(Transform(l1, l2), r1.animate.flip())
        self.wait(1)


class CombiningRhythms(Scene):
    def construct(self):
        text1 = MarkupText(
            f'<span fgcolor="{YELLOW}">1</span>,<span fgcolor="{BLUE}">2</span>,<span fgcolor="{MAROON}">3</span>'
        )
        text2 = MarkupText(
            f'<span fgcolor="{YELLOW}">1</span>,<span fgcolor="{BLUE}">2</span>,<span fgcolor="{MAROON}">3</span>'
        )

        r2 = visualize_pattern(p2, BLUE_A).scale(0.5).set_stroke(BLUE)
        r1 = visualize_pattern(p1, YELLOW_A).scale(0.5).set_stroke(YELLOW).next_to(r2,LEFT,buff=0)
        r3 = visualize_pattern(p3, MAROON_A).scale(0.5).set_stroke(MAROON).next_to(r2,RIGHT,buff=0)
        r2a = visualize_pattern(reversed(p2))
        
        start, end = get_lr_lines(VGroup(r1,r2,r3))
        n_beats = sum(map(len,[p1, p2, p3]))

        # first sequence combination
        self.play(FadeIn(text1))
        self.play(text1.animate.to_edge(UL), FadeIn(r1,r2,r3))
        # animate a sweeping red line going through beats
        self.add(start)
        self.play(Transform(start, end),run_time=0.25*n_beats)
        self.remove(end)
        self.wait(1)

        self.next_section("Another example of a sequence combination")
        self.wait()


class GraphCreation(Scene):
    def construct(self):
        k = 4  # number of adjacencies
        theta = 2*PI/(2*k)  # distribute adjacencies evenly
        
        # draw equidistant points along a circle
        circle = Circle(radius=3)
        angles = [i*theta for i in range(2*k)]
        points = [circle.point_at_angle(a) for a in angles]
        dots = [Dot(point=p).scale(2) for p in points]

        # place labels along an "outer" circle
        label_circle = Circle(radius=3.75)
        label_points  = [label_circle.point_at_angle(a) for a in angles]
        label_dots = [Dot(point=p) for p in label_points]
        
        label_text = sum([[f"{i+1}t", f"{i+1}h"] for i in range(k)], [])

        # grouped labels with dots
        dots_and_lpoints = VGroup(*dots, *label_dots)

        # animation
        self.play(Create(circle))
        self.wait(1)
        self.play(FadeIn(dots_and_lpoints), FadeOut(*label_dots))
        self.play(dots_and_lpoints.animate.flip())
        self.play(dots_and_lpoints.animate.rotate_about_origin(-PI/(2*k)))
        # create labels after transformation to stop them from mirroring and rotating
        labels = [Text(t).move_to(p) for t,p in zip(label_text,label_dots)]
        self.play(FadeIn(*labels))