import flet as ft


def homepage(page : ft.Page):

    # keyword table container
    keyword_output = ft.Column()

    # function to append the keyword
    def add_keyword(e):
        keyword = keyword_input.value
        if keyword:
            keyword_output.controls.append(
                ft.Row([
                    ft.Text("Keyword", width=200, size=18),
                    ft.Text("=", width=50, size=18),
                    ft.Text(keyword, size=18)
                ])
            )
            keyword_input.value = ""
            page.update()

    # keyword input
    keyword_input = ft.TextField(
        hint_text="Enter keyword here. Press Enter after each.",
        color=ft.Colors.GREEN_900,
        text_size=25,
        on_submit=add_keyword
    )

    # left section construct (dark green)
    left_section = ft.Container(
        content=ft.Column(
            controls= [
                ft.Text("Home", color="#efe9d9"),
                ft.Text("Applicants", color="#efe9d9"),
                ft.Text("Jobs", color="#efe9d9")
                ],
        ),
        bgcolor=ft.Colors.GREEN_900,
        padding=20,
        width=333.3,
    )


    # right section construct (cream)
    right_section = ft.Container(
        content=ft.Column(
            [
                # BANNER + JARGON
                ft.Row(
                    [
                        # title
                        ft.Text(
                            "CVRobin", 
                            color=ft.Colors.GREEN_900,
                            size=50
                            ),
                     
                        # jargon
                        ft.Text(
                            "Your reliable HRD substitute", 
                            color=ft.Colors.GREEN_900,
                            size =30
                            ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # BANNER SECTION 
                ft.Text(
                    "Home", 
                    color=ft.Colors.GREEN_900,
                    rtl = True,
                    size=25
                    ),

                # KEYWORD INPUT
                keyword_input, 

                # SEARCH ALGORITHM
                ft.Dropdown(
                    hint_text="Choose your algorithm", 
                    color=ft.Colors.GREEN_900,
                    options=[
                        ft.dropdown.Option("Knuth-Morris-Pratt"),
                        ft.dropdown.Option("Boyer-Moore"),
                        ft.dropdown.Option("Aho-Corasick"),
                        ],
                    text_size=25
                    ),

                # CV Count
                ft.TextField(hint_text="Insert your desirable CV count",
                             color=ft.Colors.GREEN_900,
                             text_size= 25
                             ), 

                # CV Count
                ft.ElevatedButton(text="Search",
                             color=ft.Colors.GREEN_900,
                             style= ft.ButtonStyle(
                                text_style=ft.TextStyle(size=20))
                             ) 
             ],
        ),
        bgcolor="#efe9d9",
        padding=20,
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

