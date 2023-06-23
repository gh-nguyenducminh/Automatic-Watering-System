#Khai báo các thư viện thời gian, lịch, gpio, firebase, gửi mail.
import time
import datetime
import RPi.GPIO as GPIO
import pyrebase
import yagmail

def main():

    #Cài chế độ khai báo chân gpio theo số pin của Raspberry Pi
    GPIO.setmode(GPIO.BOARD)

    #Khai báo chân pin 29 là chân nhận tín hiệu cảm biến
    GPIO.setup(29,GPIO.IN)

    #Khai báo chân pin 29 là chân xuất tín hiệu rơ-le
    GPIO.setup(40,GPIO.OUT)

    #API kết nối với firebase
    config = {
        "apiKey": "AIzaSyC1MIHLmrka6xWCDbAP1gnPnnjIPep9WQY",
        "authDomain": "fir-cf4d8.firebaseapp.com",
        "databaseURL": "https://fir-cf4d8-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "fir-cf4d8",
        "storageBucket": "fir-cf4d8.appspot.com"}

    #Hàm kết nối với firebase
    firebase = pyrebase.initialize_app(config)

    #Lệnh kết nối với database của firebase
    db = firebase.database()

    #Dùng biến i để đếm số lần tưới
    i = 1

    #Dùng biến batdaudem để đếm thời gian
    batdaudem = 0

    #Lấy dữ liệu từ firebase về
    sltc = db.child("HeThongTuoiCayTuDong").child("TongSoLanTuoiCay").get()
    sgtc = db.child("HeThongTuoiCayTuDong").child("TongSoGiayTuoiCay").get()
    tdcc = db.child("HeThongTuoiCayTuDong").child("ThoiDiemTuoiCayCuoiCung").get()

    #Lấy giá trị của các dữ liệu lấy về từ firebase
    sogiaytuoicay = sgtc.val()
    solantuoicay = sltc.val()
    tdtccc = tdcc.val()

    #Khởi tạo các key trên firebase
    battat = {"SoThuTu": 1}
    db.child("CheDo").set(battat)
    data = {"TongSoGiayTuoiCay":sogiaytuoicay,"ThoiDiemTuoiCayCuoiCung":tdtccc,"TongSoLanTuoiCay":solantuoicay}
    db.child("HeThongTuoiCayTuDong").set(data)
    demtg = {"DemThoiGian":batdaudem}
    db.child("BamNutTuoiCay").set(demtg)

    #Khai báo biến lưu chế độ, mặc định là chế độ chờ
    btht = db.child("CheDo").child("SoThuTu").get()
    
    try:

        while True:
            
            #Trong khi biến lưu chế độ = 1, chuyển sang chế độ chờ
            while btht.val()== 1:
                
                print("Da san sang.")

                GPIO.output(40, GPIO.HIGH)
                btht = db.child("CheDo").child("SoThuTu").get()
                batdaudem = 0

                #Dừng chương trình 0.1s
                time.sleep(.1)
            
            #Trong khi biến lưu chế độ = 2, chuyển sang chế độ tưới cây tự động
            while btht.val() == 2:
                
                print("Tuoi cay tu dong.")

                #Nếu cảm biến không gửi tín hiệu (cảm biến ướt)
                if (GPIO.input(29))==0:

                    #Theo cách lắp đặt rơ-le và nguồn, khi cổng In1 nhận tín hiệu thì công tắc rơ-le không cho nguồn điện chạy qua
                    GPIO.output(40, GPIO.HIGH)

                    #Lấy dữ liệu chế độ trên firebase
                    btht = db.child("CheDo").child("SoThuTu").get()

                    #Đặt biến đếm = 0, đợi đến khi chuyển chế độ 2 thì bắt đầu đếm
                    batdaudem = 0
                    
                    #Đếm số lần tưới mỗi khi cảm biến ướt, đếm xong chuyển biến i về 0
                    if i==1:
                        solantuoicay = solantuoicay + 1
                        i=0

                    #Lệnh cập nhật key số lần tưới cây trên firebase
                    db.child("HeThongTuoiCayTuDong").update({"TongSoLanTuoiCay":solantuoicay})

                #Nếu cảm biến gửi tín hiệu (cảm biến khô)
                elif (GPIO.input(29))==1:

                    #Theo cách lắp đặt rơ-le và nguồn, khi cổng In1 không nhận tín hiệu thì công tắc rơ-le không cho nguồn điện chạy qua
                    GPIO.output(40, GPIO.LOW)

                    #Chuyển biến i về 1 để lúc quay về chế độ 1, số lần tưới sẽ tăng 1 lần
                    if i==0:
                        i=1
                    
                    #Lệnh ấy dữ liệu thời gian từ thư viện datetime
                    tdtccc = datetime.datetime.now()

                    #Lệnh chuyển dữ liệu thời gian thành chuỗi thời gian theo dạng "giờ:phút:giây, ngày/tháng/năm"
                    tdcc = tdtccc.strftime("%H:%M:%S, %d/%m/%Y")

                    #Lệnh cập nhật key số giây tưới cây, thời điểm tưới cây cuối cùng trên firebase
                    db.child("HeThongTuoiCayTuDong").update({"TongSoGiayTuoiCay":sogiaytuoicay,"ThoiDiemTuoiCayCuoiCung":tdcc})

                    #Lệnh cập nhật key thời gian tưới tự động
                    db.child("BamNutTuoiCay").update({"DemThoiGian":batdaudem})

                    #Ras tốn 0.22s để xử lý hàm while đã viết, sau đó chương trình sẽ dừng 0.1s, tổng là 0.32s.
                    sogiaytuoicay = sogiaytuoicay + .32
                    sogiaytuoicay = round(sogiaytuoicay,2)

                    #Ras tốn 0.22s để xử lý hàm while đã viết, sau đó chương trình sẽ dừng 0.1s, tổng là 0.32s.
                    batdaudem = batdaudem + .32
                    batdaudem = round(batdaudem,2)

                    #Nếu chức năng tưới tự động chạy liên tục quá 30s, chương trình sẽ chuyển sang chế độ chờ và gửi mail cho người dùng.
                    if batdaudem > 30:

                        #Chuyển sang chế độ chờ
                        db.child("CheDo").update({"SoThuTu":1})
                        
                        try:

                            #Lấy mail của người dùng trên firebase
                            mailnhan = db.child("DiaChiMail").child("MailNhan").get()

                            #Gửi mail từ một tài khoản gmail đã cho phép ứng dụng bên thứ 3 sử dụng
                            yag = yagmail.SMTP('pion.silently@gmail.com', password ='iampion:)')
                            yag.send(to = mailnhan.val(),subject ='Hệ Thống Tưới Nước Tự Động',contents ='Bơm nước vượt quá 30 giây, đã chuyển sang chế độ chờ do nghi ngờ lỗi cảm biến.')
                            print("Gui mail thanh cong.")

                        except:
                            print("Gui mail that bai.")
                    
                    #Lấy dữ liệu chế độ trên firebase
                    btht = db.child("CheDo").child("SoThuTu").get()

                #Dừng chương trình 0.1s
                time.sleep(.1)
            
            while btht.val()==3:

                print("Khoi dong may bom.")

                #Bật máy bơm thủ công
                GPIO.output(40, GPIO.LOW)

                #Lấy dữ liệu chế độ trên firebase
                btht = db.child("CheDo").child("SoThuTu").get()
                
                #Dừng chương trình 0.1s
                time.sleep(.1)

    finally:

        #Reset tất cả các cổng GPIO đã sử dụng thành các chân nhận tín hiệu
        GPIO.cleanup()

if __name__=="__main__":
    main()