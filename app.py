import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from shiny import App, render, ui, reactive
from shinywidgets import output_widget, render_widget



# UI
ui.page_fluid(
    ui.input_select( "Module", "Pick a module",
                    "choices" = [], selected = None), 
)


# Server 




# App 
app = App(app_ui, server)


