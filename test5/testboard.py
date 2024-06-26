import tkinter as tk
from window import BaseWindow, SubPage, SecondLevelSubPage
from icon import Icon
from APIcall import APIcall

class MainWindow(BaseWindow):
    def __init__(self, title, width, height, icons, subwin_configs, second_level_configs):
        super().__init__(title, width, height)
        self.icons = icons
        self.subwin_configs = subwin_configs
        self.second_level_configs = second_level_configs
        self.history = []
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_icon_grid()

    def create_icon_grid(self):
        rows, cols = 2, 3  # 3x2 grid
        for index, icon in enumerate(self.icons):
            button = icon.create_button(self.main_frame, self.navigate_to_subwin)
            row, col = divmod(index, cols)
            button.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        
        # Configure grid weights to evenly distribute space
        for row in range(rows):
            self.main_frame.grid_rowconfigure(row, weight=1)
        for col in range(cols):
            self.main_frame.grid_columnconfigure(col, weight=1)

    def navigate_to_subwin(self, title, message):
        current_frame = self.main_frame if not self.history else self.history[-1]
        self.history.append(current_frame)

        for widget in self.main_frame.winfo_children():
            widget.pack_forget() if isinstance(widget, tk.Frame) else widget.grid_forget()

        messages = [(msg, lambda t=title, m=msg: self.navigate_to_second_level(t, m)) for msg in self.subwin_configs[title]]
        text_font_size = 14  # Set the desired text font size
        sub_page = SubPage(self.main_frame, title, messages, text_font_size, self.navigate_home)
        sub_page.pack(fill=tk.BOTH, expand=True)
        self.history.append(sub_page)  # Push the sub_page onto the history stack

    def navigate_to_second_level(self, first_level_title, second_level_title):
        current_frame = self.main_frame if not self.history else self.history[-1]
        self.history.append(current_frame)

        for widget in self.main_frame.winfo_children():
            widget.pack_forget() if isinstance(widget, tk.Frame) else widget.grid_forget()

        second_level_info = self.second_level_configs[first_level_title][second_level_title]
        topic = second_level_info['topic']
        content = second_level_info['content']
        topic_font_size = second_level_info.get('topic_font_size', 16)
        content_font_size = second_level_info.get('content_font_size', 12)
        
        sub_page = SecondLevelSubPage(
            self.main_frame, second_level_title, topic, content,
            topic_font_size, content_font_size, self.navigate_back, self.navigate_home
        )
        sub_page.pack(fill=tk.BOTH, expand=True)
        self.history.append(sub_page)  # Push the sub_page onto the history stack

    def navigate_back(self):
        if len(self.history) > 1:
            self.history.pop()
            last_frame = self.history.pop()
            for widget in self.main_frame.winfo_children():
                widget.pack_forget() if isinstance(widget, tk.Frame) else widget.grid_forget()
            last_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.navigate_home()

    def navigate_home(self):
        self.history.clear()
        for widget in self.main_frame.winfo_children():
            widget.pack_forget() if isinstance(widget, tk.Frame) else widget.grid_forget()
        self.create_icon_grid()

if __name__ == "__main__":
    screen_width = 800  # Approx. half the width of a standard screen
    screen_height = 600  # Approx. half the height of a standard screen

    icons = [
        Icon("Algebra 1", "algebra1.png", "Topics About Algebra 1", "       This is Algebra 1."),
        Icon("Geometry", "geometry.png", "Topics About Geometry", "     This is Geometry."),
        Icon("Algebra 2", "algebra2.png", "Topics About Algebra 2", "       This is Algebra 2."),
        Icon("Precalculus", "precalculus.png", "Topics About Precalculus", "        This is Precalculus."),
        Icon("Calculus", "calculus.png", "Topics About Calculus", "     This is Calculus."),
        Icon("Statistics", "statistics.png", "Topics About Statistics", "       This is Statistics.")
    ]

    subwin_configs = {
        "Topics About Algebra 1": ["A1T1", "A1T2", "A1T3", "A1T4", "A1T5", "A1T6"],
        "Topics About Geometry": ["Tools of Geometry", "Reasoning and Proof", "Parallel and Perpendicular Lines", "Congruent Triangles", "Relationships within Triangles", "Polygons and Quadrilaterals", 
                           "Similarity", "Right Triangles and Trigonometry", "Transformations", "Area", "Surface Area and Volume", "Circles"],
        "Topics About Algebra 2": ["A2T1", "A2T2", "A2T3", "A2T4", "A2T5", "A2T6"],
        "Topics About Precalculus": ["PCT1", "PCT2", "PCT3", "PCT4", "PCT5", "PCT6"],
        "Topics About Calculus": ["CT1", "CT2", "CT3", "CT4", "CT5", "CT6"],
        "Topics About Statistics": ["ST1", "ST2", "ST3", "ST4", "ST5", "ST6"]
    }

    second_level_configs = {
        "Topics About Algebra 1": {
            #A1T1 as algebra 1 topic 1
            "A1T1": {
                "topic": "Details about A1T1 in Algebra 1",
                "content": "        This is the content for Topic 1 in Algebra 1. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A1T2": {
                "topic": "Details about A1T2 in Algebra 1",
                "content": "        This is the content for Topic 2 in Algebra 1. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A1T3": {
                "topic": "Details about A1T3 in Algebra 1",
                "content": "        This is the content for Topic 3 in Algebra 1. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A1T4": {
                "topic": "Details about A1T4 in Algebra 1",
                "content": "        This is the content for Topic 4 in Algebra 1. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A1T5": {
                "topic": "Details about A1T5 in Algebra 1",
                "content": "        This is the content for Topic 5 in Algebra 1. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A1T6": {
                "topic": "Details about A1T6 in Algebra 1",
                "content": "        This is the content for Topic 6 in Algebra 1. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            }
            # Add other topics similarly...
        },

        "Topics About Geometry": {
            "Tools of Geometry": {
                "topic": "Details about Tools of Geometry in Geometry",
                "content": "        This topic covers the basic instruments and concepts used in geometry, such as points, lines, planes, angles, and the use of geometric tools like compasses, rulers, and protractors to construct and analyze shapes.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Reasoning and Proof": {
                "topic": "Details about Reasoning and Proof in Geometry",
                "content": "        This involves understanding and applying logical reasoning to develop and write geometric proofs. It includes concepts like inductive and deductive reasoning, theorems, postulates, and the structure of a formal proof.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Parallel and Perpendicular Lines": {
                "topic": "Details about Parallel and Perpendicular Lines in Geometry",
                "content": "        This topic explores the properties and relationships of parallel and perpendicular lines. It includes theorems related to angles formed by these lines and the criteria for establishing parallelism and perpendicularity.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Congruent Triangles": {
                "topic": "Details about Congruent Triangles in Geometry",
                "content": "        This focuses on the criteria for triangle congruence, such as SSS (Side-Side-Side), SAS (Side-Angle-Side), ASA (Angle-Side-Angle), and AAS (Angle-Angle-Side). It also covers the properties and applications of congruent triangles in solving geometric problems.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Relationships within Triangles": {
                "topic": "Details about Relationships within Triangles in Geometry",
                "content": "        This topic delves into the various relationships that exist within triangles, such as angle bisectors, medians, altitudes, and the properties of special triangles like isosceles and equilateral triangles.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Polygons and Quadrilaterals": {
                "topic": "Details about Polygons and Quadrilaterals in Geometry",
                "content": "        This covers the properties and classifications of polygons, with a focus on quadrilaterals. It includes the study of parallelograms, rectangles, squares, rhombuses, trapezoids, and their properties and relationships.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Similarity": {
                "topic": "Details about Similarity in Geometry",
                "content": "        This involves the concept of similar figures, particularly similar triangles. It includes the criteria for similarity, such as AA (Angle-Angle), SSS (Side-Side-Side), and SAS (Side-Angle-Side), and the use of proportions to solve problems involving similar figures.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Right Triangles and Trigonometry": {
                "topic": "Details about Right Triangles and Trigonometry in Geometry",
                "content": "        This topic covers the properties of right triangles and introduces basic trigonometric ratios (sine, cosine, and tangent). It also includes the Pythagorean theorem and its applications in solving problems involving right triangles.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Transformations": {
                "topic": "Details about Transformations in Geometry",
                "content": "        This involves the study of geometric transformations, including translations, rotations, reflections, and dilations. It explores how these transformations affect the properties of geometric figures and their coordinates.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Area": {
                "topic": "Details about Area in Geometry",
                "content": "        This topic focuses on the calculation of the area of various geometric shapes, including triangles, quadrilaterals, circles, and composite figures. It includes the use of formulas and problem-solving techniques.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Surface Area and Volume": {
                "topic": "Details about Surface Area and Volume in Geometry",
                "content": "        This covers the concepts and formulas for finding the surface area and volume of three-dimensional figures, such as prisms, cylinders, pyramids, cones, and spheres. It involves applying these formulas to solve real-world problems.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "Circles": {
                "topic": "Details about Circles in Geometry",
                "content": "        This topic explores the properties and theorems related to circles, including angles, arcs, chords, tangents, and secants. It also covers the calculation of circumference and area of a circle.",
                "topic_font_size": 18,
                "content_font_size": 14
            }
            # Add other lessons similarly...
        },

        "Topics About Algebra 2": {
            #A2T1 as algebra 2 topic 1
            "A2T1": {
                "topic": "Details about A2T1 in Geometry",
                "content": "        This is the content for Topic 1 in Algebra 2 in Geometry. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A2T2": {
                "topic": "Details about A2T2 in Algebra 1",
                "content": "        This is the content for Topic 2 in Algebra 2. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A2T3": {
                "topic": "Details about A2T3 in Algebra 1",
                "content": "        This is the content for Topic 3 in Algebra 2. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A2T4": {
                "topic": "Details about A2T4 in Algebra 1",
                "content": "        This is the content for Topic 4 in Algebra 2. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A2T5": {
                "topic": "Details about A2T5 in Algebra 1",
                "content": "        This is the content for Topic 5 in Algebra 2. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "A2T6": {
                "topic": "Details about A2T6 in Algebra 1",
                "content": "        This is the content for Topic 6 in Algebra 2. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            }
            # Add other lessons similarly...
        },

        "Topics About Precalculus": {
            #PCT1 as pre calculus topic 1
            "PCT1": {
                "topic": "Details about PCT1 in PreCalculus",
                "content": "        This is the content for Topic 1 in PreCalculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "PCT2": {
                "topic": "Details about PCT2 in PreCalculus",
                "content": "        This is the content for Topic 2 in PreCalculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "PCT3": {
                "topic": "Details about PCT3 in PreCalculus",
                "content": "        This is the content for Topic 3 in PreCalculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "PCT4": {
                "topic": "Details about PCT4 in PreCalculus",
                "content": "        This is the content for Topic 4 in PreCalculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "PCT5": {
                "topic": "Details about PCT5 in PreCalculus",
                "content": "        This is the content for Topic 5 in PreCalculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "PCT6": {
                "topic": "Details about PCT6 in PreCalculus",
                "content": "        This is the content for Topic 6 in PreCalculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            }
            # Add other lessons similarly...
        },

        "Topics About Calculus": {
            #CT1 as calculus topic 1
            "CT1": {
                "topic": "Details about CT1 in Geometry",
                "content": "        This is the content for Topic 1 in Calculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "CT2": {
                "topic": "Details about CT2 in Calculus",
                "content": "        This is the content for Topic 2 in Calculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "CT3": {
                "topic": "Details about CT3 in Calculus",
                "content": "        This is the content for Topic 3 in Calculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "CT4": {
                "topic": "Details about CT4 in Calculus",
                "content": "        This is the content for Topic 4 in Calculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "CT5": {
                "topic": "Details about CT5 in Calculus",
                "content": "        This is the content for Topic 5 in Calculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "CT6": {
                "topic": "Details about CT6 in Calculus",
                "content": "        This is the content for Topic 6 in Calculus. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            }
            # Add other lessons similarly...
        },

        "Topics About Statistics": {
            #ST1 as statistics topic 1
            "ST1": {
                "topic": "Details about ST1 in Statistics",
                "content": "        This is the content for Topic 1 in Statistics. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "ST2": {
                "topic": "Details about ST2 in Statistics",
                "content": "        This is the content for Topic 2 in Statistics. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "ST3": {
                "topic": "Details about ST3 in Statistics",
                "content": "        This is the content for Topic 3 in Statistics. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "ST4": {
                "topic": "Details about ST4 in Statistics",
                "content": "        This is the content for Topic 4 in Statistics. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "ST5": {
                "topic": "Details about ST5 in Statistics",
                "content": "        This is the content for Topic 5 in Statistics. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            },

            "ST6": {
                "topic": "Details about ST6 in Statistics",
                "content": "        This is the content for Topic 6 in Statistics. It should be formatted like an article with paragraphs and spacing.",
                "topic_font_size": 18,
                "content_font_size": 14
            }
            # Add other lessons similarly...
        }
    }

    main_window = MainWindow("MathGPT For High Schoolers", screen_width, screen_height, icons, subwin_configs, second_level_configs)
    main_window.run()
