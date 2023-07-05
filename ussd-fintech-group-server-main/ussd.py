from flask import Flask, request
import africastalking
import os


username = ""
api_key = ""
africastalking.initialize(username, api_key)
sms = africastalking.SMS

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])

def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)

    #ussd logic
    if text == "":
        #main menu
        response = "CON Welcome to our USSD Service. Please select an option:\n"
        response += "1. English\n"
        response += "2. Kiswahili\n"
        response += "3. Somali"
    elif text == "1":
        # English menu
        response = "CON Please select an option:\n"
        response += "1. Register\n"
        response += "2. Join Group\n"
        response += "3. My Account\n"
        response += "4. Bank Transaction\n"
        response += "5. Complaint\n"
        response += "6. Go back"
    elif text == "1*1":
        # English -> Register menu
        response = "CON Please select an option:\n"
        response += "1. Enter Name\n"
        response += "2. Enter ID\n"
        response += "3. Go back"
    elif text == "1*2":
        # English -> Join Group menu
        response = "CON Please select an option:\n"
        response += "1. Enter Group ID\n"
        response += "2. Go back"
    elif text == "1*3":
        # English -> My Account menu
        response = "CON Please select an option:\n"
        response += "1. Shares Menu\n"
        response += "2. Savings\n"
        response += "3. Transfer\n"
        response += "4. Payment\n"
        response += "5. Go back"
    elif text == "1*4":
        # English -> Bank Transaction menu
        response = "CON Please select an option:\n"
        response += "1. Apply Loan\n"
        response += "2. Check Balance\n"
        response += "3. Go back"
    elif text == "1*1*1":
        # English -> Register -> Enter Name menu
        response = "CON Enter your full name:"
    elif text == "1*1*2":
        # English -> Register -> Enter ID menu
        response = "CON Enter your ID number:"
    elif text == "1*1*3" or text == "1*2*2" or text == "1*3*5" or text == "1*4*3":
        # English -> Go back menu
        response = "CON Please select an option:\n"
        response += "1. English\n"
        response += "2. Kiswahili\n"
        response += "3. Somali"
    elif text == "2":
        # Kiswahili menu
        response = "CON Tafadhali chagua chaguo:\n"
        response += "1. Jisajili\n"
        response += "2. Jiunge na Kikundi\n"
        response += "3. Akaunti yangu\n"
        response += "4. Hifadhi ya Benki\n"
        response += "5. Malalamiko\n"
        response += "6. Rudi nyuma"
    elif text == "2*1":
        # Kiswahili -> Jisajili menu
        response = "CON Tafadhali chagua chaguo:\n"
        response += "1. Ingiza Jina lako\n"
        response += "2. Ingiza Kitambulisho chako\n"
        response += "3. Rudi nyuma"
    elif text == "2*2":
        # Kiswahili -> Jiunge na Kikundi menu
        response = "CON Tafadhali chagua chaguo:\n"
        response += "1. Ingiza ID ya Kikundi\n"
        response += "2. Rudi nyuma"
    elif text == "2*3":
        # Kiswahili -> Akaunti yangu menu
        response = "CON Tafadhali chagua chaguo:\n"
        response += "1. Menyu ya Hisa\n"
        response += "2. Akiba\n"
        response += "3. Hamisha\n"
        response += "4. Malipo\n"
        response += "5. Rudi nyuma"
    elif text == "2*4":
        # Kiswahili -> Hifadhi ya Benki menu
        response = "CON Tafadhali chagua chaguo:\n"
        response += "1. Omba Mkopo\n"
        response += "2. Angalia Salio\n"
        response += "3. Rudi nyuma"
    elif text == "2*1*1":
        # Kiswahili -> Jisajili -> Ingiza Jina lako menu
        response = "CON Ingiza jina lako kamili:"
    elif text == "2*1*2":
        # Kiswahili -> Jisajili -> Ingiza Kitambulisho chako menu
        response = "CON Ingiza namba yako ya kitambulisho:"
    elif text == "2*1*3" or text == "2*2*2" or text == "2*3*5" or text == "2*4*3":
        response = "CON Karibu kwenye Huduma yetu ya USSD. Tafadhali chagua chaguo:\n"
        response += "1. Kiingereza\n"
        response += "2. Kiswahili\n"
        response += "3. Kisomali"

    elif text == "3":
        # English menu
        response = "CON Fadlan ka dooro xogta:\n"
        response += "1. Diiwaan galinta\n"
        response += "2. Ku dhufo\n"
        response += "3. Akoonkaaga\n"
        response += "4. Hawala\n"
        response += "5. Cabasho\n"
        response += "6. Bukaaga"
    elif text == "3*1":
        # English -> Register menu
        response = "CON Fadlan ka dooro xogta:\n"
        response += "1. Gali magaca\n"
        response += "2. Gali tirada diiwaanka\n"
        response += "3. Bukaaga"
    elif text == "3*2":
        # English -> Join Group menu
        response = "CON Fadlan ka dooro xogta:\n"
        response += "1. Gali ID-ka kooxda\n"
        response += "2. Bukaaga"
    elif text == "3*3":
        # English -> My Account menu
        response = "CON Fadlan ka dooro xogta:\n"
        response += "1. Menyuu lambarka\n"
        response += "2. Xisaabta\n"
        response += "3. Hawala\n"
        response += "4. Bixinta\n"
        response += "5. Bukaaga"
    elif text == "3*4":
        # English -> Bank Transaction menu
        response = "CON Fadlan ka dooro xogta:\n"
        response += "1. Guji dhaqaale\n"
        response += "2. Hubi xisaabta\n"
        response += "3. Bukaaga"
    elif text == "1*1*1":
        # English -> Register -> Enter Name menu
        response = "CON Gali magacaaga oo dhameystiran:"
    elif text == "3*1*2":
        # English -> Register -> Enter ID menu
        response = "CON Gali tiradaaga diiwaanka:"
    elif text == "3*1*3" or text == "3*2*2" or text == "3*3*5" or text == "3*4*3":
        # English -> Go back menu
        response = "CON Fadlan ka dooro xogta:\n"
        response += "1. Ingiriisi\n"
        response += "2. Kiswahili\n"
        response += "3. Somali"

    else:
        response = "END Invalid input. Please try again."


    return response
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))
