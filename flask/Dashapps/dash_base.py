import dash_bootstrap_components as dbc
import dash_html_components as html




colors = {
    'background': '#fafafa',
    'text': '#000000',
    'warning':'#FF0000'
}


def warning_card():
    return dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H5("Warning", className="display-4",style={'color': colors['warning']}),
                html.P(
                    "The tools and the derived information from these tools can be wrong. "
                    "Although we build our tools with well known and tested software, there can be programming errors on our end, as well as with the third party components. "
                    "Moreover, some of the tools use data from various sources. We cannot guarantee the correctness of theses sources nor can we validate them. "
                    "Take these facts into account for everything you do with the tools. "
                    "In particular, don't use these tools to make descision for your investments or others. You can loose money! ",
                    className="lead",
                )
            ],
            fluid=True,
        )
    ],
    fluid=True,
)