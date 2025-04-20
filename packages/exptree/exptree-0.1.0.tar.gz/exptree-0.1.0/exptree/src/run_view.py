import base64
from pathlib import Path
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML, Image
import pandas as pd
import re


class RunView:
    def __init__(self, runs_data):
        self.runs_data = runs_data
        self.selected_run = None

        # Define custom styles
        self.styles = {
            'container': 'max-width: 1000px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;',
            'section': 'background-color: #f8f9fa; border-radius: 8px; padding: 15px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);',
            'header': 'background-color: #343a40; color: white; padding: 15px; border-radius: 8px 8px 0 0; margin-bottom: 0;',
            'table': 'width: 100%; border-collapse: collapse; margin-top: 8px;',
            'table_header': 'background-color: #e9ecef; font-weight: bold; text-align: left; padding: 10px;',
            'table_cell': 'padding: 8px; border-bottom: 1px solid #dee2e6;',
            'tag': 'display: inline-block; background-color: #e3f2fd; color: #0d47a1; padding: 4px 8px; border-radius: 4px; margin: 2px; font-size: 12px;',
            'badge': 'display: inline-block; padding: 4px 8px; font-size: 12px; border-radius: 12px; margin-right: 8px;',
            'title': 'font-size: 18px; font-weight: bold; margin-bottom: 10px;',
            'prompt': 'font-style: italic; background-color: #f5f5f5; padding: 12px; border-left: 4px solid #007bff; border-radius: 4px;',
        }

        # Apply custom CSS
        self.custom_css = widgets.HTML("""
        <style>
            .run-view-container { """ + self.styles['container'] + """ }
            .run-view-section { """ + self.styles['section'] + """ }
            .run-view-header { """ + self.styles['header'] + """ }
            .run-view-table { """ + self.styles['table'] + """ }
            .run-view-th { """ + self.styles['table_header'] + """ }
            .run-view-td { """ + self.styles['table_cell'] + """ }
            .run-view-tag { """ + self.styles['tag'] + """ }
            .run-view-badge { """ + self.styles['badge'] + """ }
            .run-view-title { """ + self.styles['title'] + """ }
            .run-view-prompt { """ + self.styles['prompt'] + """ }
            .widget-dropdown { width: 100% !important; margin-bottom: 15px; }
            .jupyter-widgets-output-area { padding: 0 !important; }
        </style>
        """)
        display(self.custom_css)

        # Create container
        self.main_container = widgets.VBox([])
        self.main_container.layout.margin = '20px 0'

        # Create tabs for organization
        self.tabs = widgets.Tab()
        self.details_tab = widgets.VBox([])
        self.hyperparams_tab = widgets.VBox([])
        self.metrics_tab = widgets.VBox([])
        self.artifacts_tab = widgets.VBox([])
        self.prompt_tab = widgets.VBox([])  # New tab for prompt display

        self.tabs.children = [self.details_tab, self.hyperparams_tab, self.metrics_tab, self.artifacts_tab,
                              self.prompt_tab]
        self.tabs.set_title(0, 'Details')
        self.tabs.set_title(1, 'Hyperparameters')
        self.tabs.set_title(2, 'Metrics')
        self.tabs.set_title(3, 'Artifacts')
        self.tabs.set_title(4, 'Prompt')  # Setting title for the new tab

        # Create header with run selector - FIX: Use widgets.HTML instead of HTML
        header_html = widgets.HTML(
            f'<div class="run-view-header"><div class="run-view-title">ML Run Explorer</div></div>')
        self.run_selector = widgets.Dropdown(
            options=list(self.runs_data.keys()),
            description='',
            placeholder='select run name',
            layout=widgets.Layout(width='350px')
        )
        selector_label = widgets.HTML('<strong>Select Run:</strong>')
        selector_box = widgets.HBox([self.run_selector])
        selector_box.layout.margin = '10px 0'

        # Create UI elements for details tab
        self.title_label = widgets.HTML()
        self.description_label = widgets.HTML()
        self.tags_container = widgets.HTML()

        # UI elements for hyperparameters tab
        self.hyperparameters_table = widgets.Output()

        # UI elements for metrics tab
        self.metrics_table = widgets.Output()
        self.metrics_chart = widgets.Output()

        # UI elements for artifacts tab
        self.artifacts_display = widgets.Output()

        # UI elements for prompt tab
        self.prompt_display = widgets.Output()

        # Link event to function
        self.run_selector.observe(self.on_run_change, names='value')

        # Assemble UI components
        self.details_tab.children = [self.title_label, self.description_label, self.tags_container]
        self.hyperparams_tab.children = [self.hyperparameters_table]
        self.metrics_tab.children = [self.metrics_table, self.metrics_chart]
        self.artifacts_tab.children = [self.artifacts_display]
        self.prompt_tab.children = [self.prompt_display]  # Add prompt display to prompt tab

        # FIX: This is where the error was occurring - all children must be widgets
        self.main_container.children = [header_html, selector_box, self.tabs]
        display(self.main_container)

        # Initialize with first run
        if self.runs_data:
            self.display_all(list(self.runs_data.keys())[0])

    def on_run_change(self, change):
        """Handle change in run selection."""
        selected_run_name = change['new']
        if not selected_run_name:
            return
        self.display_all(selected_run_name)

    @staticmethod
    def read_image(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
            return data

    def display_all(self, selected_run_name):
        # Get the selected run data
        run_data = self.runs_data[selected_run_name]

        # Update details tab
        self.title_label.value = f"""
        <div class="run-view-section">
            <div class="run-view-title">Run Name: {selected_run_name}</div>
        </div>
        """

        self.description_label.value = f"""
        <div class="run-view-section">
            <strong>Description:</strong>
            <p>{run_data.get('description', 'No description available.')}</p>
        </div>
        """

        # Format tags with badges
        tags = run_data.get('tags', [])
        tags_html = ""
        if tags:
            for tag in tags:
                tags_html += f'<span class="run-view-tag">{tag}</span>'
        else:
            tags_html = "No tags available"

        self.tags_container.value = f"""
        <div class="run-view-section">
            <strong>Tags:</strong><br>
            {tags_html}
        </div>
        """

        # Display hyperparameters with styled table
        with self.hyperparameters_table:
            clear_output(wait=True)
            hyperparameters = run_data.get('hyperparameters', {})
            if hyperparameters:
                hyperparameters_df = pd.DataFrame(hyperparameters.items(), columns=['Hyperparameter', 'Value'])
                # Convert to styled HTML table
                table_html = self.create_styled_table(hyperparameters_df)
                display(widgets.HTML(f'<div class="run-view-section">{table_html}</div>'))
            else:
                display(widgets.HTML('<div class="run-view-section">No hyperparameters available.</div>'))

        # Display metrics with styled table
        with self.metrics_table:
            clear_output(wait=True)
            metrics = run_data.get('metrics', {})
            if metrics:
                metrics_df = pd.DataFrame(metrics.items(), columns=['Metric', 'Value'])
                # Convert to styled HTML table
                table_html = self.create_styled_table(metrics_df)
                display(widgets.HTML(f'<div class="run-view-section">{table_html}</div>'))
            else:
                display(widgets.HTML('<div class="run-view-section">No metrics available.</div>'))

        # Display artifacts with improved layout
        with self.artifacts_display:
            clear_output(wait=True)
            artifacts = run_data.get('artifact', {})
            if artifacts:
                artifact_html = '<div class="run-view-section">'
                url_pattern = re.compile(r'https?://\S+')
                for artifact_name, artifact_value in artifacts.items():
                    file_type = Path(artifact_value).suffix.lower()
                    if file_type in [".jpg", ".jpeg", ".png", ".tiff", ".gif", ".tif"]:
                        img_data = RunView.read_image(artifact_value)
                        artifact_html += f"""
                        <div style="margin-bottom: 15px;">
                            <strong>{artifact_name}</strong>
                            <div style="margin-top: 8px;">
                                <img src='data:image/{file_type[1:]};base64,{img_data}' style='max-width: 100%; height: auto;
                                border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                            </div>
                        </div>
                        """
                    else:
                        # Check if the artifact_value is a URL
                        if url_pattern.fullmatch(artifact_value):
                            artifact_value = f'<a href="{artifact_value}" target="_blank">{artifact_value}</a>'
                        artifact_html += f"""
                        <div style="margin-bottom: 15px;">
                            <strong>{artifact_name}</strong>
                            <div style="margin-top: 8px; background-color: #f1f3f5; padding: 8px; 
                            border-radius: 4px; font-family: monospace;">{artifact_value}</div>
                        </div>
                        """
                artifact_html += '</div>'
                display(widgets.HTML(artifact_html))
            else:
                display(widgets.HTML('<div class="run-view-section">No artifacts available for this run.</div>'))

        # Display prompt with italic styling
        with self.prompt_display:
            clear_output(wait=True)
            prompt = run_data.get('prompt', {})
            if prompt:
                # Generate HTML for each key-value pair in the prompt dictionary
                prompt_sections = []
                for key, value in prompt.items():
                    prompt_sections.append(f"""
                    <div class="run-view-section">
                        <strong>{key}:</strong>
                        <div class="run-view-prompt">{value}</div>
                    </div>
                    """)

                # Join all sections and display
                prompt_html = ''.join(prompt_sections)
                display(widgets.HTML(prompt_html))
            else:
                display(widgets.HTML('<div class="run-view-section">No prompt available for this run.</div>'))

    def create_styled_table(self, df):
        """Create a styled HTML table from a dataframe"""
        html = '<table class="run-view-table">'

        # Add header
        html += '<thead><tr>'
        for col in df.columns:
            html += f'<th class="run-view-th">{col}</th>'
        html += '</tr></thead>'

        # Add rows
        html += '<tbody>'
        for _, row in df.iterrows():
            html += '<tr>'
            for item in row:
                # Format number values to have fewer decimal places if they're floats
                if isinstance(item, float):
                    formatted_item = f"{item:.4f}" if abs(item) < 1000 else f"{item:.2f}"
                    html += f'<td class="run-view-td">{formatted_item}</td>'
                else:
                    html += f'<td class="run-view-td">{item}</td>'
            html += '</tr>'
        html += '</tbody></table>'

        return html