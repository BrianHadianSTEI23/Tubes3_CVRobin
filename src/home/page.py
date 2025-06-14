import flet as ft
from results.page import results

def homepage(page : ft.Page):

    # initiate global variables
    keyword_list : list[str] = []

    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf"
    }

    # keyword table container
    keyword_output = ft.Container(
        content= ft.GridView(
                max_extent=200,  # each cell's max width
                child_aspect_ratio=2.5,  # width/height ratio
                spacing=10,
                run_spacing=10,
            ),
        margin=ft.margin.symmetric(horizontal=20)
    )
        

    # function to append the keyword
    def add_keyword(e):
        keyword = keyword_input.content.value
        keyword_list.append(keyword)
        if keyword:
            keyword_output.content.controls.append(  # Append to the GridView!
                ft.Container(
                    content=ft.Row(
                        controls=[ft.Text(keyword, size=22, color="#efe9d9")],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=10,
                    bgcolor=ft.Colors.GREEN_800,
                    border_radius=30,
                )
            )
            keyword_input.content.value = ""
            page.update()



    # keyword input
    keyword_input = ft.Container(
        content=ft.TextField(
            hint_text="Enter keyword here. Press Enter after each.",
            color=ft.Colors.GREEN_900,
            text_size=25,
            on_submit=add_keyword,
            content_padding=15,
        ),
        margin=ft.margin.symmetric(horizontal=20),
    )

    # search_algorithm
    search_algorithm = ft.Container(
                    content = ft.Dropdown(
                            hint_text="Choose your algorithm", 
                            color=ft.Colors.GREEN_900,
                            options=[
                                ft.dropdown.Option("Knuth-Morris-Pratt"),
                                ft.dropdown.Option("Boyer-Moore"),
                                ft.dropdown.Option("Aho-Corasick"),
                                ],
                            text_size=25,
                            expand=True,
                        ),
                    margin = ft.margin.Margin(left=20, top = 20, right=20, bottom=20 ),
                )
    
    # cv_count
    cv_count = ft.Container(
                    content = ft.TextField(
                        hint_text="Insert your desirable CV count",
                        color=ft.Colors.GREEN_900,
                        text_size= 25,
                        ), 
                    margin = ft.margin.Margin(left=20, top = 0, right=20, bottom=0),
                )

    # function for search button
    def search_all_cv(e):
        keyword_to_search = keyword_list
        total_cv_to_search = cv_count.content.value
        search_algorithm_to_search = search_algorithm.content.value
        page.views.clear()
        page.views.append(results(page, keyword_to_search, total_cv_to_search, search_algorithm_to_search))
        page.update()

    # left section construct (dark green)
    left_section = ft.Container(
        content=ft.Column(
            controls= [
                    ft.Container(
                        content = ft.Row(
                            controls = [
                                ft.ElevatedButton(
                                    text="Home",
                                    color=ft.Colors.GREEN_900,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size=20),
                                        padding=20,  # internal padding (vertical, horizontal)
                                        bgcolor=ft.Colors.GREEN_100,
                                        alignment=ft.alignment.top_left
                                    ),
                                    expand=True,  # allows button to grow inside expanding parent
                                    on_click=lambda e: page.go("/")
                                ),
                            ],
                            expand=True,  # allows container to grow horizontally
                            spacing=20,
                        ),
                        margin=ft.margin.symmetric(horizontal=20, vertical=20),
                    ),
                    ft.Container(
                        content = ft.Row(
                            controls = [
                                ft.ElevatedButton(
                                    text="Jobs",
                                    color=ft.Colors.GREEN_900,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size=20),
                                        padding=20,  # internal padding (vertical, horizontal)
                                        bgcolor=ft.Colors.GREEN_100,
                                        alignment=ft.alignment.top_left
                                    ),
                                    expand=True,  # allows button to grow inside expanding parent
                                    on_click=lambda e: page.go("/jobs")
                                ),
                            ],
                            expand=True,  # allows container to grow horizontally
                            spacing=20,
                        ),
                        margin=ft.margin.symmetric(horizontal=20, vertical=20),
                    ),
                    ft.Container(
                        content = ft.Row(
                            controls = [
                                ft.ElevatedButton(
                                    text="Applicants",
                                    color=ft.Colors.GREEN_900,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size=20),
                                        padding=20,  # internal padding (vertical, horizontal)
                                        bgcolor=ft.Colors.GREEN_100,
                                        alignment=ft.alignment.top_left
                                    ),
                                    expand=True,  # allows button to grow inside expanding parent
                                    on_click=lambda e: page.go("/applicants")
                                ),
                            ],
                            expand=True,  # allows container to grow horizontally
                            spacing=20,
                        ),
                        margin=ft.margin.symmetric(horizontal=20, vertical=20),
                    )
                ],
        ),
        bgcolor=ft.Colors.GREEN_900,
        padding=ft.padding.Padding(left = 30, right = 30, top = 200, bottom=30),
        width=333.3,
    )

    # right section construct (cream)
    right_section = ft.Container(
        content=ft.Column(
            [
                # BANNER + JARGON
                ft.Container(
                    content=ft.Row(
                        [
                            # title
                            ft.Text(
                                "CVRobin", 
                                color=ft.Colors.GREEN_900,
                                size=50,
                                style=ft.TextStyle(
                                        weight=ft.FontWeight.W_800,
                                        font_family="Tahoma"
                                    )
                                ),
                        
                            # jargon
                            ft.Text(
                                "Your reliable HRD substitute", 
                                color=ft.Colors.GREEN_900,
                                size =30,
                                style=ft.TextStyle(
                                        weight=ft.FontWeight.W_100,
                                        italic=True,
                                        font_family="Consolas"
                                    )
                                ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    expand_loose=True,
                    margin=30,
                    padding=10,
                ),

                # BANNER SECTION 
                ft.Container(
                    content=ft.Text(
                        "Home",
                        color="#efe9d9",
                        size=25,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    bgcolor=ft.Colors.GREEN_900,
                    padding=20,
                    margin=ft.margin.symmetric(vertical=20),
                    alignment=ft.alignment.center_right,  # align content inside container
                    width=800
                ),



                # KEYWORD INPUT
                keyword_input, 
                keyword_output,

                # SEARCH ALGORITHM
                search_algorithm,

                # CV Count
                cv_count,

                # search button
                ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.ElevatedButton(
                                text="Search",
                                color=ft.Colors.GREEN_900,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(size=20),
                                    padding=ft.Padding(top = 30, bottom = 30, right = 20, left= 20),  # internal padding (vertical, horizontal)
                                    bgcolor=ft.Colors.GREEN_100,
                                ),
                                expand=True,  # allows button to grow inside expanding parent
                                on_click=search_all_cv
                            ),
                        ],
                        expand=True,  # allows container to grow horizontally
                        spacing=20,
                    ),
                    margin=ft.margin.symmetric(horizontal=20, vertical=20),
                )

             ],
            horizontal_alignment=ft.CrossAxisAlignment.END
        ),
        bgcolor="#efe9d9",
        # padding=20,
        expand=True,  # Fills half the width
    )

    return ft.View(
        route = "/",
        controls=[
            ft.Row(
                controls = [
                    left_section,
                    right_section
                ],
                expand=True
            )
        ],
    )

