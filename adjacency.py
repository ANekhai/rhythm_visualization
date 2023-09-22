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

        intro_text = Text("A simple rhythm")
        explanatory_text = Text("Let's play this rhythm")

        # animation
        self.play(FadeIn(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))
        self.play(FadeIn(rhythm))
        self.wait(3)
        self.play(FadeOut(rhythm))
        self.next_section("Playing the rhythm")
        self.play(FadeIn(explanatory_text))
        self.wait(1)
        self.play(FadeOut(explanatory_text))
        self.play(FadeIn(rhythm, start))
        self.play(Transform(start,end), run_time=2, rate_func=linear)
        self.wait(1)
        self.play(FadeOut(rhythm, start))


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

        intro_text = Text("We can label rhythms with numbers")
        mid_text = Text("Let's add some more rhythms")

        # show how we can label
        self.play(FadeIn(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))
        self.play(FadeIn(r1))
        self.play(r1.animate.move_to(RIGHT), FadeIn(l1))
        self.wait(1)
        self.next_section("Add a few more patterns")
        self.play(FadeOut(r1, l1))
        self.play(FadeIn(mid_text)), self.wait(2), self.play(FadeOut(mid_text))
        self.play(FadeIn(g1))
        self.play(g1.animate.next_to(g2, UP))
        self.play(g1.animate.align_to(g2, LEFT), FadeIn(g2, g3))
        self.wait(2)
        self.play(FadeOut(g1, g2, g3))

# TODO: Need to center label+rhythm to match with the labeling pattern in first animat
class NegatedRhythms(Scene):
    def construct(self):
        r1 = visualize_pattern(p1).move_to(RIGHT)
        
        l1 = Text("+1:").next_to(r1, LEFT).shift(LEFT).scale(2).next_to(r1, LEFT)
        l2 = Text("-1:").next_to(r1, LEFT).shift(LEFT).scale(2).next_to(r1, LEFT)
        intro_text = Text('We can also "negate" rhythms')
        
        # animation
        self.play(FadeIn(intro_text)), self.wait(2), self.play(FadeOut(intro_text))
        self.play(FadeIn(l1, r1))
        self.wait(1)
        self.play(Transform(l1, l2), r1.animate.flip())
        self.wait(1)
        self.play(FadeOut(l1, r1))


class CombiningRhythms(Scene):
    def construct(self):
        text1 = MarkupText(
            f'<span fgcolor="{YELLOW}">1</span>,<span fgcolor="{BLUE}">2</span>,<span fgcolor="{MAROON}">3</span>'
        )
        text2 = MarkupText(
            f'<span fgcolor="{BLUE}">-2</span>,<span fgcolor="{MAROON}">-3</span>,<span fgcolor="{YELLOW}">1</span>'
        ).to_edge(UL)

        r2 = visualize_pattern(p2, BLUE_A).scale(0.5).set_stroke(BLUE)
        r1 = visualize_pattern(p1, YELLOW_A).scale(0.5).set_stroke(YELLOW).next_to(r2,LEFT,buff=0)
        r3 = visualize_pattern(p3, MAROON_A).scale(0.5).set_stroke(MAROON).next_to(r2,RIGHT,buff=0)
        
        start, end = get_lr_lines(VGroup(r1,r2,r3))
        n_beats = sum(map(len,[p1, p2, p3]))

        intro_text = Text("Rhythms can combine into phrases")

        # first sequence combination
        self.play(FadeIn(intro_text)), self.wait(2), self.play(FadeOut(intro_text))
        self.play(FadeIn(text1))
        self.play(text1.animate.to_edge(UL), FadeIn(r1,r2,r3))
        # animate a sweeping red line going through beats
        self.wait(1)
        self.add(start)
        self.play(Transform(start, end),run_time=0.25*n_beats,rate_func=linear)
        self.wait(0.5)
        self.remove(start)
        self.wait(1)

        self.next_section("Another example of a sequence combination")
        # useful things for the complex movement
        left_most = r1.get_left()
        right_most = r3.get_right()
        r1_path = ArcBetweenPoints(r1.get_right(), right_most).shift(2*LEFT)
        segment_group = VGroup(r2, r3)

        # actually doing the movement
        self.play(FadeOut(text1), FadeIn(text2))
        # get segments in correct position
        self.play(MoveAlongPath(r1, r1_path), segment_group.animate.align_to(left_most, LEFT))
        # orient segments correctly
        self.play(r3.animate.flip(), r2.animate.flip())
        self.wait(1)
        self.add(start.move_to(left_most))
        self.play(Transform(start, end),run_time=0.25*n_beats,rate_func=linear)
        self.wait(0.5)
        self.play(FadeOut(text2, r1, r2, r3, start))

# TODO: Need to center line that nodes are aligned on after we drop the rhythm
class SequenceToGraph(Scene):
    def construct(self):
        # useful values
        triple_buff = 3*DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

        # create three rhythm sequences
        r1 = visualize_pattern(p1, YELLOW_A).scale(0.4).set_stroke(YELLOW)
        r2 = visualize_pattern(p2, BLUE_A).scale(0.4).set_stroke(BLUE)
        r3 = visualize_pattern(p3, MAROON_A).scale(0.4).set_stroke(MAROON)
        r1.next_to(r2, LEFT, buff=triple_buff), r3.next_to(r2, RIGHT, buff=triple_buff)

        # labels for rhythms
        l1 = MarkupText(f'<span fgcolor="{YELLOW}">1</span>').next_to(r1, UP)
        l2 = MarkupText(f'<span fgcolor="{BLUE}">2</span>').next_to(r2, UP)
        l3 = MarkupText(f'<span fgcolor="{MAROON}">3</span>').next_to(r3, UP)
        
        # head and tail labels
        h1 = MarkupText(f'<span fgcolor="{YELLOW}">1h</span>').next_to(r1, DL).shift(RIGHT)
        t1 = MarkupText(f'<span fgcolor="{YELLOW}">1t</span>').next_to(r1, DR).shift(0.9*LEFT)
        h2 = MarkupText(f'<span fgcolor="{BLUE}">2h</span>').next_to(r2, DL).shift(RIGHT)
        t2 = MarkupText(f'<span fgcolor="{BLUE}">2t</span>').next_to(r2, DR).shift(0.9*LEFT)
        h3 = MarkupText(f'<span fgcolor="{MAROON}">3h</span>').next_to(r3, DL).shift(RIGHT)
        t3 = MarkupText(f'<span fgcolor="{MAROON}">3t</span>').next_to(r3, DR).shift(0.9*LEFT)
        node_labels = [h1, t1, h2, t2, h3, t3]

        # draw line to align labels on
        start = r1.get_left()
        end = r3.get_right()
        line = Line(start, end).move_to(ORIGIN)
        num_points = 6
        points = [line.point_from_proportion(i / (num_points - 1)) for i in range(num_points)]

        # circles for labels
        colors = ([YELLOW]*2) + ([BLUE]*2) + ([MAROON]*2)
        node_circles = [Circle(radius=0.75).set_stroke(c).move_to(p) for c,p in zip(colors, points)]

        # edges between nodes
        e1 = Line(node_circles[1].get_right(), node_circles[2].get_left())
        e2 = Line(node_circles[3].get_right(), node_circles[4].get_left())
        e3 = ArcBetweenPoints(node_circles[0].get_bottom(), node_circles[5].get_bottom(), angle=1.4)
        edges = [e1, e2, e3]

        # transition text
        intro_text1 = Text("Now the fun part!")
        intro_text2 = Text("Let's create an adjacency graph")

        explainer1 = Text("We label the heads and tails of each rhythm").scale(0.8).shift(2*DOWN)
        explainer2 = Text("These become the nodes of our graph").scale(0.8).shift(2*DOWN)
        explainer3 = Text("We draw edges between touching rhythm ends").scale(0.8).shift(2*DOWN)

        # animation
        self.play(FadeIn(intro_text1)), self.wait(1), self.play(FadeOut(intro_text1)),self.play(FadeIn(intro_text2)), self.wait(2), self.play(FadeOut(intro_text2))
        self.play(FadeIn(r1, r2, r3, l1, l2, l3))
        self.wait(1)
        self.play(FadeIn(*node_labels))
        self.play(FadeIn(explainer1)), self.wait(2), self.play(FadeOut(explainer1))

        self.next_section("Dropping the rhythm, keeping the graph")
        self.play(FadeOut(r1, r2, r3, l1, l2, l3))
        moved_labels = [l.animate.move_to(p) for l,p in zip(node_labels,points)]
        self.play(*moved_labels)
        self.play(FadeIn(*node_circles))
        self.play(FadeIn(explainer2)), self.wait(2), self.play(FadeOut(explainer2)), self.play(FadeIn(explainer3)), self.wait(2), self.play(FadeOut(explainer3))
        self.play(FadeIn(*edges))
        self.wait(1)
        self.play(FadeOut(*edges, *node_circles, *node_labels))



class GraphCreation(Scene):
    def construct(self):
        k = 4  # number of adjacencies
        theta = 2*PI/(2*k)  # distribute adjacencies evenly around circle
        
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

        # explanatory text
        text1 = Text("Normally I draw these graphs as a circle").scale(0.8)
        text2 = Text("Nodes start in the top left and run clockwise").scale(0.8)
        text3 = Text("But... I ran out of time").scale(0.8)
        text4 = Text("I did animate this, though!")        
        text1.next_to(text2, UP), text3.next_to(text2, DOWN)

        # animation
        self.play(FadeIn(text1)), self.play(FadeIn(text2)), self.play(FadeIn(text3)), self.wait(1), self.play(FadeOut(text1, text2, text3))
        self.play(FadeIn(text4)), self.wait(2), self.play(FadeOut(text4))
        self.play(Create(circle))
        self.wait(1)
        labels = [Text(t).move_to(p) for t,p in zip(label_text,label_dots)]
        self.play(FadeIn(dots_and_lpoints, *labels), FadeOut(*label_dots))
        self.wait(1), self.play(FadeOut(*labels))
        self.play(dots_and_lpoints.animate.flip())
        self.play(dots_and_lpoints.animate.rotate_about_origin(-PI/(2*k)))
        # create labels after transformation to stop them from mirroring and rotating
        labels = [Text(t).move_to(p) for t,p in zip(label_text,label_dots)]
        self.play(FadeIn(*labels))
        self.wait(2)
        self.play(FadeOut(dots_and_lpoints, *labels, circle))


class TextOutro(Scene):
    def construct(self):
        t1 = Text("TODOs")
        l1 = Text("1. Draw circular graphs")
        l2 = Text("2. Animate edge transformations")
        l3 = Text("3. Graph distance")
        l4 = Text("4. Add sound")
        l2.next_to(ORIGIN, UP), l1.next_to(l2, UP), l3.next_to(l2, DOWN), l4.next_to(l3, DOWN)

        out = Text("Thank you!").scale(2)

        # animation
        self.play(FadeIn(t1)), self.wait(1), self.play(FadeOut(t1))
        self.play(FadeIn(l1)), self.play(FadeIn(l2)), self.play(FadeIn(l3)), self.play(FadeIn(l4)), self.wait(2), self.play(FadeOut(l1, l2, l3, l4))
        self.play(FadeIn(out)), self.wait(2), self.play(FadeOut(out))
