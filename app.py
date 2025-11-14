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
    ui.input_select( "module", "Pick a module",
                    choices =module_choices, selected = None
    ),

    ui.output_plot("attendance_plot", height='600px')
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
            attendance_df = attendance_series.to_frame(name = 'avg_attendance')

            return attendance_df
        return pd.DataFrame()
    
    @output
    @render.plot
    def attendance_plot():
        attendance = filtered_data()
        
        if attendance.empty: 
            return plt.figure() 
        else:
            fig, ax = plt.subplots(figsize=(15,6))
            attendance['avg_attendance'].plot(kind='bar', ax=ax)
            plt.axhline(y=attendance['avg_attendance'].mean(), color='red', linestyle='--', label=f'Mean: {attendance["avg_attendance"].mean():.3f}')
            plt.xlabel('Date')
            plt.ylabel('Average attendance')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()  # doing this to prevent labels from getting cut iff
            
        return fig 

# App 
app = App(app_ui, server)


