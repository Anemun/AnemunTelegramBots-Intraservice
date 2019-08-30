import speech_recognition as sr

def recognize(data):
    result = "не распознано."

    r = sr.Recognizer()
    with sr.AudioFile(data) as source:
        audio = r.record(source)

    
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "indigo-bloom-251313",
  "private_key_id": "1c3aa9a3928ee418c8585e2471448ed73fc3d0e2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCuMy9DVTQrPq0g\nnVU78C14J3MA1PilUyttZBOpJiu9uMCSAcTy9tL8TPsH+AeK/Cr6cxmNpMEgaR8s\nkqn5DBukNB6nDQrKDxrPSVeVSG6P8zyun9F7IRszu0XXPAIYpkJJflUxgdyGcHwu\nrixOQ/0n9Lf10jdR5E4+/5r2PysBjeGUduC72QlPolxJWv0wZL/owJ4evkJBzexx\nn1CI6qPw9OGRXWrZTNfuECFjdhb38bw/VQd8wWYKbWgGhS/UEjCWYDdUfuiA3Zdt\n81U3TU6M1A3tRsjarNoivHr3VX4/hukDEhfXM27e0dgWFSP4xLV8y7kkEDEne9wb\npgyNCTd9AgMBAAECggEAG8zpXwqK/9fJ02mof59N8l4BWYGjiObkCFovVRBVbLq+\naM7FeqzvcPpsGZJ4ybKCvWN/EX7Yn26HXhqt66QGCUeUGL7ZGPQeKDShOJ7NnkWI\nSqoQyWC4MaJSfA4Em6B09bumpvb9lar/9ocvZPIuxaCldyKsV3JjFmS+e0wLdfzF\nj/TtP1F5DgGvUNgF4Tky1yDcOutehJEpzPiKyXlqZr6msD3guUme1ENa2Vr1ERHz\nigU8mbjAPzwldddjawidXXtLGlM6/rqwy56MPL3Wf/sT/LAZxtxA33iAsq40A+9E\nDMSVYItOrWBLTpfAV+Qe7gH31rsg3hXfIBrjSM8VlQKBgQDzFHluIVfwVqkUYmty\nY0WhXnrYlBIWeqBnekVgMVmBn1uqJzgGCSKuqirvCXhGf23XUdrvB2gE6pWkIr/V\naLJV+sjW77ygLrjozp1LFPpIv/wf8bCxNpvdV7wEF4Gt6yr+DUD698c6LxyvrQVO\n1jGWU1HRxROvRkFq/18FdAt8/wKBgQC3dXpF4QDno/9kYTyTm1WaPIrcMBg/p4/b\naf2xVs2eXKLZgDXE+jT6Gg93A+mJlgiRDBpBNnwcwwSpoHCPZpnHtaSH1ak18KLx\nlSU8pYRDdgLWd290/szTrd2Ux7hul2S0jE65B6U0ysFBy5pYx1CZUjtrQggLrWr5\nP92yGRq/gwKBgQDNkgMfoBM+rgtPsewsUMgSMFSz1IV3fT0qRb1mHFYVyS88Nu6q\nLA+op0Cn5tpQxHOgJRmCDEFr5vemV7zkPiaTkANJwnVDAkBeol1jodoIrFQMr9k+\nBXDLP+dBjp+c9cTmFU9e7y0Nh8o6x5g1k+9bshr/zCtZj5DDbDRv6DPPAQKBgHbv\nQzjAOOzzRePWogXzgxh9vWwoBeBmif2uBhkM9DqBRdYJp1Iu/19Qu8vljmZzDNSz\n6uVyJB4lVAWADNj6pCFzodmp64wbmBdUIJLjnw55GDffsDNB6Jomsmr825VespvW\nBkcwLKs/8u/rxgFeHeN4Cytq4Hppj9tMyzXlzpBvAoGBALgIoTpduFTqTsamInHn\ndLryTJDZfKaFIfJriWmfknAzNcqYVSjy6Fi1p6yp5wkYsFaSljJu7PD7VXh+33j/\npZf6TIMI1Y1SW452W6DeWej8KP7TFtjaz0oJTZvs9HppSpVewysHAp3BE27XDjeQ\nZ8wuTBsiLza2MIK9/QjS1exw\n-----END PRIVATE KEY-----\n",
  "client_email": "pyjackintrbot@indigo-bloom-251313.iam.gserviceaccount.com",
  "client_id": "117358009220122889965",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pyjackintrbot%40indigo-bloom-251313.iam.gserviceaccount.com"
}
"""
    try:
        result = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language="ru-RU")
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))

    #result = ""
    return result