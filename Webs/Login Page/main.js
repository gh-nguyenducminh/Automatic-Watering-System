const firebaseConfig = {
    apiKey: "AIzaSyC1MIHLmrka6xWCDbAP1gnPnnjIPep9WQY",
    authDomain: "fir-cf4d8.firebaseapp.com",
    databaseURL: "https://fir-cf4d8-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "fir-cf4d8",
    storageBucket: "fir-cf4d8.appspot.com",
    messagingSenderId: "595286391660",
    appId: "1:595286391660:web:5bb7cca0c3f892e9fad149",
    measurementId: "G-EL2WBK4ZYY"
};

firebase.initializeApp(firebaseConfig);
var database = firebase.database();
const dbRef = firebase.database().ref();
var dangky = document.getElementById("dangky");

dangky.onclick = function(){
        
    var tendk = document.getElementById("tendk").value;
    var mkdk = document.getElementById("mkdk").value;
    var emaildk = document.getElementById("emaildk").value;

    dbRef.child("DangNhap").child(tendk).get().then((snapshot) => {
        if (snapshot.val() == null){
            dbRef.child("DangNhap").child(tendk).update({
                "MatKhau" : mkdk,
                "Email" : emaildk
            });
            alert("Đăng ký thành công, hãy đăng nhập để sử dụng hệ thống.")
        }
        else{
            alert("Tên đăng nhập đã được sử dụng, vui lòng thử lại.");
        }
    });
}

dangnhap.onclick = function(){

    var tendn = document.getElementById("tendn").value;
    var mkdn = document.getElementById("mkdn").value;
    let diachiip = document.getElementById("diachiip").innerHTML;

    dbRef.child("DangNhap").child(tendn).child("MatKhau").get().then((snapshot) => {
        if (snapshot.val() == mkdn){
            dbRef.child("DangNhap").update({
                "DiaChiIPMotLan" : diachiip
            });
            window.location.href = 'https://fir-cf4d8.web.app/'
        }
        else{
            alert("Sai tên đăng nhập hoặc mật khẩu, vui lòng thử lại.")
        }
    });
}