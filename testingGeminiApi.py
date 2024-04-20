# # Install the SDK (assuming you haven't already)
# # pip install google-cloud-aiplatform>=1.38

import google.generativeai as genai

# Set your API key (replace with your actual key)
your_api_key = "AIzaSyDUwAn805A5NZY4fUrQSyUOmFDrv5KjtO8"
genai.configure(api_key=your_api_key)
text = "Lockheed Martin Rotary and Mission Systems, Owego, New York, was awarded a $88,380,255 Captains of Industry contract for the overhaul of B-2 digital receiver and legacy defense message system. This contract provides for overhaul, management, and material lay-in. Work will be performed at Owego, New York, and is expected to be completed by April 16, 2034. This contract was a sole source acquisition. No funds are being obligated at time of award. The Air Force Sustainment Center, Tinker Air Force Base, Oklahoma, is the contracting activity (FA8119-24-D-0008). (Awarded April 17, 2024)"

# Select the model (choose 'gemini-pro' for advanced features)
model = genai.GenerativeModel('gemini-pro')

# Provide a prompt for generation
query = "give me json format who is the contractor? what is the location? what is the cost? what is the purpose? WHhen will the work be completed? where will the work be performed? What is the contract number?"

# Generate content
response = model.generate_content(text+query)

# Access the generated text
generated_text = response.text

# Print the generated poem
print(generated_text)

