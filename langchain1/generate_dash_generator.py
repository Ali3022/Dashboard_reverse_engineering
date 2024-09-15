import os
import sys
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Paths for the Python files
generated_python_file = "generated_dynamic_detailed_dash_app.py"
revised_python_file = "revised_dynamic_detailed_dash_app.py"

# Function to read analysis files
def read_analysis_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

# Read the visual and element analysis from the respective files
visual_analysis = read_analysis_file("visual_analysis.txt")
element_analysis = read_analysis_file("element_analysis.txt")

if not visual_analysis or not element_analysis:
    print("Error: Unable to read analysis files. Ensure both visual_analysis.txt and element_analysis.txt are available.")
    sys.exit(1)

# Initialize OpenAI API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

# Initialize the ChatOpenAI from langchain-openai using GPT-4
llm = ChatOpenAI(api_key=api_key, model_name="gpt-4")

# Create the detailed prompt template for generating the Dash app
prompt_template = PromptTemplate(
    input_variables=["full_analysis"],
    template="""
Based on the following visual and element analysis, generate a comprehensive and highly detailed Python Dash application using Dash Bootstrap Components (dbc) and Flask API for real-time MongoDB data.

{full_analysis}

### Key Requirements:
1. **API Integration**:
   - Use Flask API to pull real-time data from MongoDB.
   - Handle error cases with response validation and fallback mechanisms.

2. **Layout**:
   - Implement a responsive layout using `dbc.Row()` and `dbc.Col()`.
   - Include KPI boxes showing metrics such as total sessions, users, bounce rate, and page views.
     - Each box should have hover effects.
     - Color code: green for positive changes, red for negative changes.
     - Tooltip on hover displaying multiple data points (e.g., percentage change, year-over-year comparisons).

3. **Charts**:
   - Implement responsive interactive charts using Plotly (line, bar, pie charts).
   - Provide interactivity like zoom, hover tooltips, and panning across time-series data.
   - Multiple data series with proper legends, axis labels, and color-coding.

4. **Filter Controls**:
   - Implement filters for date range, services, and traffic sources.
   - Ensure dynamic updates of charts and KPIs based on the selected filters.

5. **Real-Time Updates**:
   - Ensure real-time updates for all KPIs and charts based on MongoDB data.

6. **Tooltips and Hover Effects**:
   - Multi-line tooltips on hover showing detailed statistics.
   - All interactive elements should have hover effects and feedback.

7. **Mobile Responsiveness**:
   - The entire layout should be optimized for both mobile and desktop.

8. **Error Handling**:
   - Show "N/A" when the data is missing or the API fails.
   - Handle large datasets efficiently.

### Example Components:
- `dbc.Row()` for layout.
- `dcc.Graph()` for charts.
- `dbc.Col()` for grid layout.

Make sure the generated code is well-formatted and adheres to Python best practices. ONLY RETURN CODE. There should be no comments, text, or anything but code in your response including the starting "```" and "python```".
"""
)

# Combine the visual and element analyses into a single string
full_analysis = f"Visual Analysis:\n{visual_analysis}\n\nElement Analysis:\n{element_analysis}"

# Format the prompt using the combined analysis
prompt = prompt_template.format(full_analysis=full_analysis)

# Generate the Dash application code
try:
    # Invoke the LLM to generate the Dash app code using a string input
    response = llm.invoke(prompt)

    # Save the generated Python code to a file
    with open(generated_python_file, "w") as file:
        file.write(response.content)

    print(f"Dash application code generated!")

except Exception as e:
    print(f"Error generating Dash application code: {e}")
    sys.exit(1)
