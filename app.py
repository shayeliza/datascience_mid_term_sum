import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from shiny import App, render, ui, reactive

# this is my clean dataframe exported as a CSV file so that I don't have to clean it again. 
df = pd.read_csv('shiny_dataframe.csv')


module_choices = df['Module Name'].unique().tolist()

# UI
app_ui = ui.page_fluid(
    ui.input_select( "Module", "Pick a module",
                    choices =module_choices, selected = None), 
)


# Server 
def server (input, output, session):
    @reactive.calc # will return a value and will only recalculate when dependencies change
    def filtered_data():
        selected_module = input.module()
        if selected_module:
            module_df = df[df['Module Name'] == selected_module].copy()
# code from my notebook which creates a filtered dataframe dependant on which module is chosen (selected_module) from module_choices
            date_grouped = module_df.groupby('Date')
            attendance_series = date_grouped['Attended'].mean()
            attendance_df = attendance_series.to_frame(name=f'avg_attendance for {selected_module} module')

            return attendance_df
        return pd.DataFrame()
    

# App 
app = App(app_ui, server)


