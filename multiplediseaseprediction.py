import streamlit as st
import streamlit.components.v1 as components  

# Inject CSS into Streamlit
st.markdown(
    """
    <style>
    body,html{
        height: 100%;
        margin: 0;
        background: rgb(44, 47, 59);
        background: -webkit-linear-gradient(to right, rgb(40, 59, 34), rgb(54, 60, 70), rgb(32, 32, 43));
        background: linear-gradient(to right, rgb(38, 51, 61), rgb(50, 55, 65), rgb(33, 33, 78));
    }
    .chat{
        margin-top: auto;
        margin-bottom: auto;
    }
    .card{
        height: 500px;
        border-radius: 15px !important;
        background-color: rgba(0,0,0,0.4) !important;
    }
    .msg_card_body{
        overflow-y: auto;
    }
    .card-header{
        border-radius: 15px 15px 0 0 !important;
        border-bottom: 0 !important;
    }
    .card-footer{
        border-radius: 0 0 15px 15px !important;
        border-top: 0 !important;
    }
    .type_msg{
        background-color: rgba(0,0,0,0.3) !important;
        border:0 !important;
        color:white !important;
        height: 60px !important;
        overflow-y: auto;
    }
    .type_msg:focus{
        box-shadow:none !important;
        outline:0px !important;
    }
    .send_btn{
        border-radius: 0 15px 15px 0 !important;
        background-color: rgba(0,0,0,0.3) !important;
        border:0 !important;
        color: white !important;
        cursor: pointer;
    }
    .msg_cotainer{
        margin-top: auto;
        margin-bottom: auto;
        margin-left: 10px;
        border-radius: 25px;
        background-color: rgb(82, 172, 255);
        padding: 10px;
        position: relative;
    }
    .msg_cotainer_send{
        margin-top: auto;
        margin-bottom: auto;
        margin-right: 10px;
        border-radius: 25px;
        background-color: #58cc71;
        padding: 10px;
        position: relative;
    }
    .msg_time{
        position: absolute;
        left: 0;
        bottom: -15px;
        color: rgba(255,255,255,0.5);
        font-size: 10px;
    }
    .msg_time_send{
        position: absolute;
        right:0;
        bottom: -15px;
        color: rgba(255,255,255,0.5);
        font-size: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define chatbot HTML template
chatbot_html = """
<div class="container-fluid h-100">
    <div class="row justify-content-center h-100">        
        <div class="col-md-8 col-xl-6 chat">
            <div class="card">
                <div class="card-header msg_head">
                    <div class="d-flex bd-highlight">
                        <div class="img_cont">
                            <img src="https://www.prdistribution.com/spirit/uploads/pressreleases/2019/newsreleases/d83341deb75c4c4f6b113f27b1e42cd8-chatbot-florence-already-helps-thousands-of-patients-to-remember-their-medication.png" class="rounded-circle user_img">
                            <span class="online_icon"></span>
                        </div>
                        <div class="user_info">
                            <span>Medical Chatbot</span>
                            <p>Ask me anything!</p>
                        </div>
                    </div>
                </div>
                <div id="messageFormeight" class="card-body msg_card_body"></div>
                <div class="card-footer">
                    <form id="messageArea" class="input-group">
                        <input type="text" id="text" name="msg" placeholder="Type your message..." autocomplete="off" class="form-control type_msg" required/>
                        <div class="input-group-append">
                            <button type="submit" id="send" class="input-group-text send_btn"><i class="fas fa-location-arrow"></i></button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# Display chatbot UI in Streamlit
st.set_page_config(page_title="Medical Chatbot")
st.title("Medical Chatbot 💬")
components.html(chatbot_html, height=600, scrolling=True)
