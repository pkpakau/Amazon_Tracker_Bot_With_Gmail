    import requests
    from bs4 import BeautifulSoup as BS
    from smtplib import SMTP
    import smtplib
    from email.message import EmailMessage
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import os

    pathh = os.getcwd()
    import threading

    plist = open(f"{pathh}/product_list.txt", "a+")
    plist.close()
    
    

    # SMTP Server Details
    SMTP_SERVER = 'smtp.gmail.com'
    PORT = 465
    FROM_EMAIL = Your email in quotes
    PASSWORD = Your password in quotes
    
    TO_EMAIL = ""

    def create_message(url, price, title):
        msg = EmailMessage()
        title = title[:35]
        part1 = MIMEText(title, "plain")
        msg['Subject'] = f'Product Price dropped at {price}'
        
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg.set_content(f"Link of product : {url}")
        return msg
        


    def extract_price(url):
        page = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"})
        soup = BS(page.content, "html.parser")
        title = soup.find(id="title").get_text()
        spans = soup.find_all('span',{'class': 'a-offscreen'})
        lines  = [span.get_text() for span in spans]
        inttext = str(lines[0]).replace(",","")[1:-1]
        amazon_price = float(inttext)
        return amazon_price, title

    def notify(url, price, title):
        print("SMTP Socket Generation")
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)   ## Connect to Gmail SMTP server
        smtp.login(FROM_EMAIL, Your Password in quotes)  ## Login
        smtp.send_message(create_message(url, price, title))
        print("mail sent")
        smtp.close()

    # def notify():
    #     print("SMTP Socket Generation")
    #     server = SMTP(SMTP_SERVER, PORT)
    #     server.starttls()
    #     server.login(FROM_EMAIL, PASSWORD)

    #     subject = 'BUY NOW!!'
    #     body = 'Price has fallen. Go buy it now - ' + URL
    #     msg = f"Subject : {subject}\n\n{body}"

    #     print("Send Mail")
    #     server.sendmail(FROM_EMAIL, TO_EMAIL, msg)
    #     server.quit()


    def checkprices():
        threading.Timer(30, checkprices).start()
        print("Checking Prices of existing products")
        product_list = open(f"{pathh}/product_list.txt", "r")
        for line in product_list.readlines():
            
            listline = line.split(" ")
            extracted_price, title = extract_price(listline[0])
            if( extracted_price <= float(listline[1])):
                notify(listline[0], listline[1], title)

        
    # clear screen
    os.system('cls' if os.name == 'nt' else 'clear')


    print("=====>Welcome to Amazon Price Tracker Bot<=====\n")

    ch = int(input("Enter\n1. To Add New Product\n2. To Check Prices of Already Entered Products\n3. To Quit\n\nYour Choice : \n"))

  

    if(ch == 1):
        URL=""
        URL = input("\nEnter url of product : ")
        AFFORDABLE_PRICE = float(input("Enter price at which you want notifications : "))
        print("\n==> New Product added to list!!!")

        L = [URL, str(AFFORDABLE_PRICE)]
        print(L)
        L = " ".join(L)
        L = L + "\n"
        product_list = open("product_list.txt", "a")

        product_list.writelines(L)
        product_list.close()
    elif(ch == 2):
        print(os.path.getsize(f"{pathh}/product_list.txt"))
        if(os.path.getsize(f"{pathh}/product_list.txt") == 0 ):
            print("\nPlease enter some products to check!!!")
            quit()
        else:
            checkprices()
    else: 
        quit()



