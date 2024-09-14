import base64
import os
import requests
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Function to encode the image into base64 format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to the image (assuming it's in the same folder as this script)
image_path = "dashboard_image1.jpg"

# Encode the image to base64
base64_image = encode_image(image_path)

# Construct the LangChain prompt template for image analysis
prompt_template = PromptTemplate(
    input_variables=["image_base64"],
    template="""
    Your task is to analyze the image provided and describe its contents in two different ways:

    **Part 1: Visual Analysis**
    - Provide a full and detailed analysis of the **visual structure** of the image. Focus on the following aspects:
      1. **Overall Structure and Layout**:
         - Identify and describe the primary sections of the image, such as:
           - Headers
           - KPI boxes
           - Graphs or charts
           - Filters and controls
           - Footers
         - Describe the layout (e.g., rows, columns, grids) and the **spacing between elements**.
         - Specify how each section is aligned (left, right, center), and its relative position to other sections.
         - If applicable, explain how the layout might adjust for different screen sizes (responsiveness).
      2. **Typography and Font Styling**:
         - Describe the font families, weights, sizes, colors, and letter spacing used in the image.
         - Note how the headers, sub-headers, and body text differ in terms of styling and positioning.
         - Include how text is positioned within boxes and charts.
      3. **Color Palette and Backgrounds**:
         - Extract background colors for each section (e.g., headers, KPI boxes, graphs, etc.).
         - Identify gradients, shadows, or background effects like borders or rounded corners.
         - Provide the exact hex codes for all colors, including those used for hover effects.
         - Describe any hover effects (shadows, scaling, or color shifts) on different elements.
      4. **Visual Components (Graphs, KPI boxes, etc.)**:
         - Describe the graphical components present, such as bar charts, line charts, pie charts, etc.
         - For each component, describe its dimensions (width, height), axis labels, legends, and placement within the layout.

    **Part 2: Functional Element Analysis**
    - Provide a breakdown of the **elements in the dashboard** that are functionally important. For each element, describe what kind of data is needed to support it. Focus on:
      1. **KPI Boxes**:
         - Describe the fields required to display the metrics in the KPI boxes. For example:
           - **Sessions**
           - **Page Views**
           - **Users**
           - **Website Visits**
         - Specify the data types for each field (e.g., Integer, Date, String).
         - Include how these metrics may change over time, or how comparisons (e.g., percentage change over the previous period) should be supported.
      2. **Graphs and Charts**:
         - For each chart (e.g., line charts, bar charts, pie charts), explain what data is needed to render the chart.
         - Include fields such as:
           - **Date**: To support time-series data.
           - **Sessions**: Number of sessions over time.
           - **Bounce Rate**: Percentage field for bounce rate.
           - **Traffic Sources**: Categorical field for traffic source (e.g., organic, direct, paid).
         - Describe what axes, legends, and data points are represented in the chart.
      3. **Filters and Controls**:
         - Describe the necessary fields to support dynamic filtering in the dashboard (e.g., by date range, services, posts).
         - For each filter, include the data structure and types required (e.g., String, Date).
         - Explain how the filters should interact with the data (e.g., dropdowns updating the data in real-time).
    """
)

# Use environment variables to store the OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI API via LangChain with the correct model
#llm = ChatOpenAI(api_key=api_key, model_name="gpt-3.5-turbo-16k")
llm = ChatOpenAI(api_key=api_key, model_name="gpt-4")

# Create the LangChain LLM chain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Execute the chain and get the detailed response
response = chain.run({"image_base64": base64_image})

# Print the raw response to inspect its contents
print("LLM Response:\n", response)


# Check that the response contains both Part 1 and Part 2 markers
visual_analysis_start = response.find("**Part 1: Visual Analysis**")
element_analysis_start = response.find("**Part 2: Functional Element Analysis**")

if visual_analysis_start == -1 or element_analysis_start == -1:
    print("Error: The response does not contain the expected analysis markers.")
else:
    # Extract the visual analysis and element analysis from the response
    visual_analysis = response[visual_analysis_start:element_analysis_start].strip()
    element_analysis = response[element_analysis_start:].strip()

    # Output the visual analysis to a text file
    with open("visual_analysis.txt", "w") as f:
        f.write(visual_analysis)

    # Output the element analysis to a text file
    with open("element_analysis.txt", "w") as f:
        f.write(element_analysis)

    print("Image analysis completed. Visual and element analysis saved to separate files.")
