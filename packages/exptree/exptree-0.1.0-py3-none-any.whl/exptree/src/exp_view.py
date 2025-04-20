import sys
from datetime import datetime

import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import pandas as pd
import time

class ExperimentView:
    def __init__(self, experiments):
        self.experiments = experiments
        self.df = None
        self.numerical_columns = []
        self.current_experiment = None

        # Define styles
        self.card_style = "border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);"
        self.header_style = "font-size: 1.3em; font-weight: bold; color: #3a3a3a; margin-bottom: 12px;"
        self.label_style = "font-weight: bold; color: #555;"
        self.value_style = "color: #333;"
        self.table_style = """
        <style>
        .table-container {
            overflow-x: auto;
            max-width: 100%;
            margin-bottom: 20px;
        }
        table {
            border-collapse: collapse; 
            width: auto; 
            margin-top: 10px; 
            font-family: Arial, sans-serif;
            white-space: nowrap;
        }
        th {
            background-color: #f2f2f2; 
            padding: 12px; 
            text-align: left; 
            border: 1px solid #ddd; 
            font-weight: bold;
            position: sticky;
            top: 0;
        }
        td {
            padding: 10px; 
            border: 1px solid #ddd;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .metrics-summary-container {
            overflow-x: auto;
            white-space: nowrap;
            padding-bottom: 10px;
        }
        .metrics-card {
            display: inline-block;
            background-color: #f5f5f5;
            border-radius: 5px;
            padding: 12px;
            min-width: 180px;
            margin-right: 15px;
        }
        .run-view-section {
            margin-bottom: 15px;
            border-left: 3px solid #3498db;
            padding-left: 15px;
        }
        .run-view-prompt {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-top: 5px;
            white-space: pre-wrap;
            font-family: monospace;
            max-height: 300px;
            overflow-y: auto;
        }
        .prompt-cell {
            white-space: pre-wrap;
            font-family: monospace;
            max-height: 200px;
            overflow-y: auto;
            background-color: #f8f9fa;
            padding: 8px;
            border-radius: 4px;
        }
        .download-btn {
            padding: 6px 12px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 5px;
            font-size: 0.9em;
            transition: background-color 0.3s;
        }
        .download-btn:hover {
            background-color: #2980b9;
        }
        .download-container {
            float: right;
            margin-bottom: 10px;
        }
        </style>
        """

        # Create UI elements with improved styling
        self.experiment_selector = widgets.Dropdown(
            options=list(self.experiments.keys()),
            description='Experiment:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='350px')
        )

        # Page header
        self.page_header = widgets.HTML(
            value=f"<h1 style='color: #2c3e50; margin-bottom: 20px;'>Experiment Dashboard</h1>"
        )

        # Experiment details section
        self.experiment_card = widgets.HTML()

        # Controls section
        self.filter_text = widgets.Text(
            description='Filter runs:',
            placeholder='Enter keyword',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='350px', margin='0 20px 0 0')
        )

        self.sort_by_dropdown = widgets.Dropdown(
            description='Sort by:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='250px', margin='0 20px 0 0')
        )

        self.sort_order_dropdown = widgets.Dropdown(
            options=['Ascending', 'Descending'],
            description='Order:',
            value='Descending',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='200px')
        )

        # Create a control panel with filters and sorting
        self.control_panel = widgets.HBox([
            self.filter_text,
            self.sort_by_dropdown,
            self.sort_order_dropdown
        ], layout=widgets.Layout(
            border='1px solid #e0e0e0',
            padding='10px',
            margin='20px 0',
            background_color='#f9f9f9',
            border_radius='5px'
        ))

        # Metrics summary section
        self.metrics_summary = widgets.HTML()

        # Download buttons
        self.download_buttons = self.create_download_buttons()

        # Results table
        self.output_table = widgets.Output()

        header_box = widgets.HBox([
            # Title on the left
            widgets.HTML(value=f"<div style='{self.header_style}'>Run Comparison</div>"),
            # Spacer to push buttons to right
            widgets.HTML(value="<div style='flex-grow: 1;'></div>"),
            # Buttons on the right
            self.download_buttons
        ], layout=widgets.Layout(
            width='100%',
            justify_content='space-between',
            align_items='center'
        ))

        self.table_container = widgets.VBox([
            header_box,
            self.output_table,
        ], layout=widgets.Layout(
            border='1px solid #e0e0e0',
            padding='15px',
            border_radius='8px',
            margin='10px 0'
        ))

        # Status bar for notifications
        self.status_bar = widgets.HTML(
            value="<div style='padding: 8px; color: #555; font-style: italic;'>Ready to analyze experiments</div>"
        )

        # Link events to functions
        self.experiment_selector.observe(self.on_experiment_change, names='value')
        self.filter_text.observe(self.apply_filter, names='value')
        self.sort_by_dropdown.observe(self.sort_table, names='value')
        self.sort_order_dropdown.observe(self.sort_table, names='value')

        # Initial display of experiment data
        self.update_display(self.experiment_selector.value)

        # Display the UI components in a structured layout
        display(self.page_header)
        display(self.experiment_selector)
        display(self.experiment_card)
        display(self.metrics_summary)
        display(self.control_panel)
        display(self.table_container)
        display(self.status_bar)

    def create_dataframe(self, selected_experiment):
        """Convert run data into a pandas DataFrame."""
        runs = self.experiments[selected_experiment]['runs']

        # Extracting data for DataFrame creation
        data = []
        for run in runs:
            run_data = {
                "Run Name": run.get("name", run.get("run_id", ""))
            }

            # Add created_at and last_updated if available
            if "created_at" in run:
                run_data["Created At"] = run["created_at"]

            if "last_updated" in run:
                run_data["Last Updated"] = run["last_updated"]

            if "created_by" in run:
                run_data["Created By"] = run["created_by"]

            # Dynamically adding hyperparameters and metrics
            for key, value in run.get('hyperparameters', {}).items():
                run_data[f'HP: {key}'] = value

            for key, value in run.get('metrics', {}).items():
                run_data[f'Metric: {key}'] = value

            for key, value in run.get('artifact', {}).items():
                run_data[f'{key}'] = value

            # Add prompts to the DataFrame
            for key, value in run.get('prompt', {}).items():
                run_data[f'Prompt: {key}'] = value

            data.append(run_data)

        self.df = pd.DataFrame(data)

        # Detecting numerical columns for sorting
        self.numerical_columns = self.df.select_dtypes(include=['number']).columns.tolist()
        self.sort_by_dropdown.options = ['Run Name'] + self.numerical_columns

        # Set default sort to the first metric if available
        metric_columns = [col for col in self.numerical_columns if col.startswith('Metric:')]
        if metric_columns:
            self.sort_by_dropdown.value = metric_columns[0]
        elif self.numerical_columns:
            self.sort_by_dropdown.value = self.numerical_columns[0]
        else:
            self.sort_by_dropdown.value = 'Run Name'



    def create_download_buttons(self):
        """Create download buttons for CSV and PDF formats using ipywidgets."""

        # Define Python functions for downloads
        def download_csv_clicked(b):
            self.df.to_csv(self.current_experiment+str(time.time())+".csv")

        # Create ipywidgets buttons
        csv_button = widgets.Button(
            description='Download CSV',
            button_style='info',
            tooltip='Download data as CSV'
        )

        # Connect the buttons to the callback functions
        csv_button.on_click(download_csv_clicked)

        # Create a container for the buttons
        return widgets.HBox([csv_button])


    def display_sorted_table(self, df):
        """Display the sorted DataFrame as an HTML table with runs as columns."""
        if df.empty:
            table_html = "<p>No data available for this experiment.</p>"
        else:
            # Create a copy of the DataFrame for display purposes
            display_df = df.copy()

            # Format numerical values to 4 decimal places
            for col in display_df.select_dtypes(include=['float']).columns:
                display_df[col] = display_df[col].map(lambda x: f"{x:.4f}" if pd.notnull(x) else '')

            # Transpose the DataFrame to have runs as columns
            # First, set the run name as the index before transposing
            display_df_transposed = display_df.set_index('Run Name').transpose()

            # Prepare the parameter labels as the first column
            # Create a new column for parameter names
            display_df_transposed.insert(0, 'Parameter', display_df_transposed.index)

            # Highlight best metric values
            metric_rows = [idx for idx in display_df_transposed.index if idx.startswith('Metric:')]
            for idx in metric_rows:
                row = display_df_transposed.loc[idx]
                numeric_values = pd.to_numeric(row[1:], errors='coerce')  # Skip the Parameter column

                # Determine if higher is better (e.g., accuracy) or lower is better (e.g., loss)
                higher_is_better = not ('loss' in idx.lower() or 'error' in idx.lower())

                # Find the best value
                if higher_is_better and not numeric_values.empty:
                    best_value = numeric_values.max()
                    for col in row.index[1:]:  # Skip the Parameter column
                        try:
                            if pd.to_numeric(row[col], errors='coerce') == best_value and not pd.isna(best_value):
                                display_df_transposed.at[
                                    idx, col] = f"<span>{row[col]}</span>"
                        except:
                            pass
                elif not numeric_values.empty:
                    best_value = numeric_values.min()
                    for col in row.index[1:]:  # Skip the Parameter column
                        try:
                            if pd.to_numeric(row[col], errors='coerce') == best_value and not pd.isna(best_value):
                                display_df_transposed.at[
                                    idx, col] = f"<span'>{row[col]}</span>"
                        except:
                            pass

            # Group rows by type (info, hyperparameters, metrics, prompts, artifacts)
            info_rows = ['Created At', 'Last Updated', 'Created By']
            hp_rows = [idx for idx in display_df_transposed.index if idx.startswith('HP:')]
            metric_rows = [idx for idx in display_df_transposed.index if idx.startswith('Metric:')]
            prompt_rows = [idx for idx in display_df_transposed.index if idx.startswith('Prompt:')]
            artifact_rows = [idx for idx in display_df_transposed.index
                             if idx not in info_rows and not idx.startswith('HP:')
                             and not idx.startswith('Metric:') and not idx.startswith('Prompt:')
                             and idx != 'Parameter']

            # Create ordered index for better display
            ordered_index = ['Parameter']
            ordered_index.extend([idx for idx in info_rows if idx in display_df_transposed.index])
            ordered_index.extend([idx for idx in hp_rows if idx in display_df_transposed.index])
            ordered_index.extend([idx for idx in metric_rows if idx in display_df_transposed.index])
            ordered_index.extend([idx for idx in prompt_rows if idx in display_df_transposed.index])
            ordered_index.extend([idx for idx in artifact_rows if idx in display_df_transposed.index])

            # Reorder the rows
            display_df_transposed = display_df_transposed.reindex(ordered_index)

            # Create HTML with section headers
            table_html = f"""
            <div class="table-container" style="text-align: left;">
                <table>
                    <thead>
                        <tr>
                            <th>Parameter</th>
                            {' '.join([f'<th>{col}</th>' for col in display_df_transposed.columns[1:]])}
                        </tr>
                    </thead>
                    <tbody>
            """

            # Add information section
            info_section = [idx for idx in info_rows if idx in display_df_transposed.index]
            if info_section:
                table_html += f"""
                    <tr>
                        <td colspan="{len(display_df_transposed.columns)}" style="background-color:#e0e0e0; font-weight:bold;text-align: left;">Run Information</td>
                    </tr>
                """
                for idx in info_section:
                    row = display_df_transposed.loc[idx]
                    table_html += f"""
                        <tr>
                            <td>{row['Parameter']}</td>
                            {' '.join([f'<td>{row[col]}</td>' for col in display_df_transposed.columns[1:]])}
                        </tr>
                    """

            # Add hyperparameters section
            if hp_rows:
                table_html += f"""
                    <tr>
                        <td colspan="{len(display_df_transposed.columns)}" style="background-color:#e0e0e0; font-weight:bold;text-align:left;">Hyperparameters</td>
                    </tr>
                """
                for idx in hp_rows:
                    row = display_df_transposed.loc[idx]
                    table_html += f"""
                        <tr>
                            <td>{row['Parameter'].replace('HP: ', '')}</td>
                            {' '.join([f'<td>{row[col]}</td>' for col in display_df_transposed.columns[1:]])}
                        </tr>
                    """

            # Add metrics section
            if metric_rows:
                table_html += f"""
                    <tr>
                        <td colspan="{len(display_df_transposed.columns)}" style="background-color:#e0e0e0; font-weight:bold;text-align:left;">Metrics</td>
                    </tr>
                """
                for idx in metric_rows:
                    row = display_df_transposed.loc[idx]
                    table_html += f"""
                        <tr>
                            <td>{row['Parameter'].replace('Metric: ', '')}</td>
                            {' '.join([f'<td>{row[col]}</td>' for col in display_df_transposed.columns[1:]])}
                        </tr>
                    """

            # Add prompts section
            if prompt_rows:
                table_html += f"""
                    <tr>
                        <td colspan="{len(display_df_transposed.columns)}" style="background-color:#e0e0e0; font-weight:bold;text-align:left;">Prompts</td>
                    </tr>
                """
                for idx in prompt_rows:
                    row = display_df_transposed.loc[idx]
                    table_html += f"""
                        <tr>
                            <td>{row['Parameter'].replace('Prompt: ', '')}</td>
                            {' '.join([f'<td><div class="prompt-cell">{row[col]}</div></td>' for col in display_df_transposed.columns[1:]])}
                        </tr>
                    """

            # Add artifacts section
            if artifact_rows:
                table_html += f"""
                    <tr>
                        <td colspan="{len(display_df_transposed.columns)}" style="background-color:#e0e0e0; font-weight:bold;text-align:left;">Artifacts</td>
                    </tr>
                """
                for idx in artifact_rows:
                    row = display_df_transposed.loc[idx]
                    table_html += f"""
                        <tr>
                            <td>{row['Parameter']}</td>
                            {' '.join([f'<td>{row[col]}</td>' for col in display_df_transposed.columns[1:]])}
                        </tr>
                    """

            table_html += """
                    </tbody>
                </table>
            </div>
            """

        with self.output_table:
            clear_output()
            display(HTML(self.table_style + table_html))

    def create_metrics_summary(self, df):
        """Create a summary of metrics across runs."""
        metric_cols = [col for col in df.columns if col.startswith('Metric:')]

        if not metric_cols:
            self.metrics_summary.value = ""
            return

        # Create a horizontally scrollable metrics summary
        summary_html = f"<div style='{self.header_style}'>Metrics Summary</div>"
        summary_html += "<div class='metrics-summary-container'>"

        for col in metric_cols:
            metric_name = col.replace('Metric: ', '')
            values = pd.to_numeric(df[col], errors='coerce')

            if values.notna().any():
                min_value = values.min()
                max_value = values.max()

                summary_html += f"""
                <div class='metrics-card'>
                    <div style='font-weight: bold; margin-bottom: 8px;'>{metric_name}</div>
                    <div>Min: {min_value:.4f}</div>
                    <div>Max: <span>{max_value:.4f}</span></div>
                </div>
                """

        summary_html += "</div>"
        self.metrics_summary.value = summary_html

    def update_display(self, selected_experiment):
        """Update the display based on selected experiment."""
        self.current_experiment = selected_experiment
        experiment_data = self.experiments[selected_experiment]

        # Format experiment details as a card
        experiment_html = f"""
        <div style='{self.card_style}'>
            <div style='{self.header_style}'>{experiment_data.get('title', experiment_data.get('name', selected_experiment))}</div>
            <div style='margin-bottom: 12px;'>
                <span style='{self.label_style}'>Description:</span> 
                <span style='{self.value_style}'>{experiment_data.get('description', 'No description available')}</span>
            </div>
            <div style='margin-bottom: 12px;'>
                <span style='{self.label_style}'>Tags:</span> 
                <span style='{self.value_style}'>{self.format_tags(experiment_data.get('tags', []))}</span>
            </div>
            <div>
                <span style='{self.label_style}'>Created by:</span> 
                <span style='{self.value_style}'>{experiment_data.get('created_by', 'Unknown')}</span>
            </div>
        </div>
        """

        self.experiment_card.value = experiment_html

        # Create dataframe from run data
        self.create_dataframe(selected_experiment)

        # Create metrics summary
        self.create_metrics_summary(self.df)

        # Create download buttons
        self.create_download_buttons()

        # Display initial sorted table
        self.sort_table(None)

        # Update status
        num_runs = len(self.experiments[selected_experiment]['runs'])
        self.status_bar.value = f"<div style='padding: 8px; color: #555;'>Displaying {num_runs} runs for experiment '{selected_experiment}'</div>"

    def format_tags(self, tags):
        """Format tags with nice styling."""
        if not tags:
            return "None"

        tag_html = ""
        for tag in tags:
            tag_html += f"<span style='background-color: #e8f4f8; color: #2980b9; padding: 3px 8px; border-radius: 12px; font-size: 0.9em; margin-right: 5px;'>{tag}</span>"
        return tag_html

    def on_experiment_change(self, change):
        """Handle change in experiment selection."""
        self.update_display(change['new'])

    def apply_filter(self, change):
        """Filter the table based on search text."""
        if not self.df is None:
            filter_text = self.filter_text.value.lower()

            if filter_text:
                # Filter across all columns
                filtered_df = self.df.copy()
                mask = False

                for col in filtered_df.columns:
                    mask = mask | filtered_df[col].astype(str).str.lower().str.contains(filter_text, na=False)

                filtered_df = filtered_df[mask]

                # Update status with filter info
                self.status_bar.value = f"<div style='padding: 8px; color: #555;'>Found {len(filtered_df)} runs matching '{filter_text}'</div>"
            else:
                filtered_df = self.df
                self.status_bar.value = f"<div style='padding: 8px; color: #555;'>Displaying all {len(filtered_df)} runs</div>"

            # Apply current sort
            self.display_sorted_table(self.sort_dataframe(filtered_df))

    def sort_dataframe(self, df):
        """Sort DataFrame based on current sort settings."""
        if df.empty:
            return df

        sort_column = self.sort_by_dropdown.value
        ascending = self.sort_order_dropdown.value == 'Ascending'

        if sort_column in df.columns:
            if df[sort_column].dtype in ['float64', 'int64'] or df[sort_column].astype(str).str.replace('.',
                                                                                                        '').str.isdigit().all():
                # Convert to numeric for sorting
                return df.sort_values(by=sort_column,
                                      ascending=ascending,
                                      key=lambda x: pd.to_numeric(x, errors='coerce'))
            else:
                return df.sort_values(by=sort_column, ascending=ascending)
        return df

    def sort_table(self, change):
        """Sort and display the table based on selected criteria."""
        if not self.df is None:
            # Apply current filter first
            self.apply_filter(None)