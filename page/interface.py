import streamlit as st

def set_streamlit():
    st.set_page_config(
    page_title = "solvedOR",
    page_icon = "📉",)

    # Checar esse html 
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    hide_streamlit_style = """
    <style>
    .css-1y0tads {padding-top: 0rem;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html = True)
    
    return "initializing..."

def show_results():
    pass
    
def initialize_info():
    pass