# QR Code Generator using Streamlit

## Imports
import datetime
import json
from segno import helpers
import segno
from unidecode import unidecode
import qrcode
import streamlit as st
from PIL import Image

## Main settings from page
st.set_page_config(layout="centered", page_title="QR Code", page_icon="./img/qr.png")
st.title("QR Code Generator")
st.subheader("Choose the type, fill in your details, and click 'Generate QRCode'.")


footer = """<style>
a:link , a:visited{
color: black;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; color: black; text-align: center;' href="http://www.linkedin.com/in/tranquocnam/" target="_blank">Bell Tran</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

st.markdown(
    "<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>",
    unsafe_allow_html=True,
)

## Sidebar for QR Code Type Selection
qr_types = {"QR Text": "Text" ,"Links/URLs": "Link", "WiFi": "WiFi", "Business Card": "VCard"}
choice = st.sidebar.radio("Select QR Code type:", list(qr_types.keys()))

st.sidebar.subheader("About the app")
st.sidebar.info(
    "Developed by Bell Tran to generate QR Codes for QR Text, business cards, WiFi passwords, or links. Built with Streamlit."
)
st.sidebar.markdown(
    """Find me on [LinkedIn](http://www.linkedin.com/in/tranquocnam/), or [GitHub](https://github.com/Bell1609).""",
    unsafe_allow_html=True,
)

if choice == "Business Card":
    with st.form("VCard"):
        name = st.text_input("Name", "")
        phone = st.text_input("Telephone - Recommended format: +5511999999999", "")
        email = st.text_input('Email - For more than one, use ";" ', "")
        url = st.text_input('URL - For more than one, use ";" ', "")
        org = st.text_input("Company", "")
        title = st.text_input("Title", "")
        birthday = st.date_input(
            "Birth Date - In case of omission, keep the default date",
            None,
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today(),
        )
        border = st.slider(label="Border Size", min_value=1, max_value=5)
        scale = st.slider(label="QR Code Size", min_value=5, max_value=10)
        submitted = st.form_submit_button("Generate QR Code")
        if submitted:
            qr = helpers.make_vcard(
                name=name,
                displayname=name,
                phone=phone,
                email=[i.strip() for i in email.split(";")],
                url=[i.strip() for i in url.split(";")],
                org=org,
                title=title,
                birthday=None if birthday == datetime.date.today() else birthday,
            )
            qr.save("vcard.png", border=border, scale=scale)

elif choice == "WiFi":
    with st.form("WiFi"):
        ssid = st.text_input("Wifi Name", "")
        password = st.text_input("Password", "")
        security = st.radio("Security", ("WPA2 (Standard)", "WPA", "None"))
        border = st.slider(label="Border Size", min_value=1, max_value=5)
        scale = st.slider(label="QR Code Size", min_value=10, max_value=15)
        submitted = st.form_submit_button("Generate QR Code")
        if submitted:
            wifi = helpers.make_wifi(
                ssid=ssid,
                password=password,
                security=security.replace(" (Standard)", ""),
            )
            wifi.save("wifi.png", border=border, scale=scale)

elif choice == "Links/URLs":
    with st.form("Link"):
        url = st.text_input("Links/URLs", "")
        border = st.slider(label="Border Size", min_value=1, max_value=5)
        scale = st.slider(label="QR Code Size", min_value=10, max_value=15)
        submitted = st.form_submit_button("Generate QR Code")
        if submitted:
            link = segno.make(url)
            link.save("link.png", border=border, scale=scale)

elif choice == "QR Text":
    with st.form("Text"):
        col1, col2 = st.columns((2,1))
    
        with col1:
            txt = st.text_area(
            "Type your text you want to convert to QR Code here",
            value="Bell Tran",
            height=250
            )
            st.write(f'You wrote {len(txt)} characters.')

            submitted = st.form_submit_button("Generate QR Code")
            if submitted:
                img = qrcode.make(txt)
                img.save("qr.png")

        with col2:
            if submitted:
                image = Image.open('qr.png')
                st.image(image, caption='Scan with Mobile')
    st.write('---')
    
## Display and Download QR Code after form submission
if submitted:
    if choice == "Business Card":
        with open("vcard.png", "rb") as f:
            bytes_qr = f.read()
            st.image(bytes_qr, caption="Preview QR Code")
            st.download_button(
                "Download QR Code",
                data=bytes_qr,
                file_name="vcard.png",
                mime="image/png",
            )
    elif choice == "WiFi":
        with open("wifi.png", "rb") as f:
            bytes_wifi = f.read()
            st.image(bytes_wifi, caption="Preview QR Code")
            st.download_button(
                "Download QR Code",
                data=bytes_wifi,
                file_name="wifi.png",
                mime="image/png",
            )
    elif choice == "Links/URLs":
        with open("link.png", "rb") as f:
            bytes_link = f.read()
            st.image(bytes_link, caption="Preview QR Code")
            st.download_button(
                "Download QR Code",
                data=bytes_link,
                file_name="link.png",
                mime="image/png",
            )
    elif choice == "QR Text":
        with open("qr.png", "rb") as f:
            bytes_link = f.read()
            st.image(bytes_link, caption="Preview QR Code")
            st.download_button(
                "Download QR Code",
                data=bytes_link,
                file_name="qr.png",
                mime="image/png",
            )
