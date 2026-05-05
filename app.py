st.markdown("""
<style>

/* Background with gradient mix */
.stApp {
    background: linear-gradient(135deg, #C71585, #8B0000, #2b2b2b);
    color: white;
}

/* Main title */
h1 {
    color: #ffffff;
    text-align: center;
    font-size: 50px;
    font-weight: 900;
    letter-spacing: 1px;
}

/* Subtext */
p {
    font-size: 18px;
    color: #f5f5f5;
}

/* Labels */
label {
    font-size: 18px !important;
    font-weight: 600;
    color: #ffffff !important;
}

/* Selectbox */
div[data-baseweb="select"] {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 6px;
    font-size: 16px;
}

/* Button */
.stButton > button {
    background: linear-gradient(to right, #8B0000, #C71585);
    color: white;
    border-radius: 14px;
    height: 55px;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(to right, #a30000, #ff1493);
}

/* Subheaders */
h2, h3 {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 10px;
}

/* Movie cards (poster area spacing) */
img {
    border-radius: 12px;
    margin-bottom: 8px;
}

/* Movie title */
strong {
    font-size: 16px;
}

/* Caption */
.stCaption {
    font-size: 14px;
    color: #e0e0e0;
}

/* Add spacing between sections */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Make layout wider */
.main {
    max-width: 1200px;
}

</style>
""", unsafe_allow_html=True)