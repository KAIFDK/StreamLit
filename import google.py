import google.generativeai as genai

genai.configure(api_key="AIzaSyCeAynIIf2iBwD6M_Q-_WMUKcJ1bmz3EJQ")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(input("Enter your question: "))
print(response.text)