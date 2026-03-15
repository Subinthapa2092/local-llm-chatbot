### Importing the necessary libraries and Modulus:: 
import streamlit as st 
import ollama
### Setting up the Page Configuration 
st.set_page_config(page_title ="Local Al Nepal Chatbot",layout = 'centered')
### Setup the title 
st.title("Local AI Nepal Chatbot")
st.caption("Runs On your laptop using ollama Models")
### Siderbar Controls to keep the Model simple for the beginner Level 
with st.sidebar:
    st.header("Application Setting: ")
    # Dropdown of Model Option's 
    ### Drop down to select the model from the list of available models in ollama
    model_name = st.selectbox(
        
        "Choose a model:", 
        options = ["phi3:mini","llama3.1","mistral"],
        index = 0)
    
    temperature = st.slider("Ccreativity (temperature)",0.0,1.0,0.3,0.1)
    max_tokens = st.slider("Max Tokens (response Length)",64,1024,256,64)
    st.markdown("----")
    
    st.subheader("Important :: Pull the Model first in your terminal if you have not pull already")
    st.code(f"Ollama pull {model_name}",language="bash")
    st.write("If you want to pull all the models from your tutorial:")
    
    
    st.code(
        "ollama Pull phi3:mini\n"
        "ollama pull llama3.1:8b\n"
        "ollama pull mistral",
        language = "bash"
    )
    st.markdown("----")
    st.write("Quick test in terminal:")
    st.code("Ollama list",language="bash")
### Storing the chat history in streamlit Session(persiss across reruns)
if "messages" not in st.session_state:
    st.session_state.messages= [
        {"role":"system","content":"you are a helpful Ai Assistant to answer many different questions accurately and precisely"}
    ]
### Display the chat history while skipping the system message or system instruction ::
# for msg in st.session_state.message:
#     if msg["role"] == "system":
#         continue 
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])
if "message" not in st.session_state:
    st.session_state.message = []

for msg in st.session_state.message:
    st.write(msg)
       
## Chat Input 
user_text = st.chat_input("Please Type Your Question here....")
## define the function to get the response from llm 
def generate_response_stream(messages,model,temp,max_tokens):
    """
    Stream tokens from ollama model so the UI feels like chatgpt/copilot
    
    """
    stream = ollama.chat(
        model = model,messages = messages,stream = True,
        options={
            "temperature": temp,
            "num_predict": max_tokens
        }
    )
    for chunk in stream:
        yield chunk["message"]["content"]
if user_text:
    st.session_state.messages.append({"role":"user","content":user_text})
    
    with st.chat_message("user"):
        st.markdown(user_text)
    ### Generate + stream assistant  response 
    with st.chat_message("assistant"):
        try:
            response_text = st.write_stream(
                generate_response_stream(
                    messages= st.session_state.messages,
                    model = model_name,
                    temp = temperature,
                    max_tokens= max_tokens
                    )
            )
        except Exception as e:
            st.error("Cloud not connect to OLLama or rn the selected Model.")
            st.info(
                "Fix Checklist:\n"
                "1) Make Run that OLLama is installed and running\n"
                "2) Run the pull Command shown in the sidebar\n"
                "3) Try: `ollama run phi3:mini`in terminal locally to confirm it work\n"
            )
            st.exception(e)
            response_text = ""
    ### Saving assitants response to conversation history 
    if response_text:
        st.session_state.messages.append({"role":"assistant","content":response_text})
### Clear Chat history button
col1,col2 = st.columns([1,3])
with col1:
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role":"system","content":"you are a helpful Ai Assistant to answer many different questions accurately and precisely"}
        ]
        st.rerun()