let seconds = 0;
let interval = 0;
let i = 0;

function stopWatch(){
	seconds++
	document.getElementById("display").innerHTML = seconds/100
}

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

var btn1 = document.getElementById("btn1");
var btn2 = document.getElementById("btn2");
var btn3 = document.getElementById("btn3");

btnchayweb.onclick = function(){
	let diachiip = document.getElementById("diachiip").innerHTML;
    dbRef.child("DangNhap").child("DiaChiIPMotLan").get().then((snapshot) => {
	    if (snapshot.val() == diachiip){
	        dbRef.child("DangNhap").update({
	            "DiaChiIPMotLan" : "Ngắt"
	        });
	        btn1.onclick = function(){
				window.clearInterval(interval);
				i = 0;
				database.ref("/CheDo").update({
					"SoThuTu" : 1
				});
			};

			btn2.onclick = function(){
				window.clearInterval(interval);
				i = 0;
				database.ref("/CheDo").update({
					"SoThuTu" : 2
				});
			};

			btn3.onclick = function(){
				if (i == 0) {
					seconds = 0;
					interval = window.setInterval(stopWatch,10);
					i = 1;
					database.ref("/CheDo").update({
					"SoThuTu" : 3
				});
				};
			};

			database.ref("/HeThongTuoiCayTuDong/TongSoLanTuoiCay").on("value",function(snapshot){
				var tongsolantuoicay = snapshot.val();
				document.getElementById("tsltc").innerHTML = tongsolantuoicay;
			});

			database.ref("/HeThongTuoiCayTuDong/TongSoGiayTuoiCay").on("value",function(snapshot){
				var tongsogiaytuoicay = snapshot.val();
				document.getElementById("tsgtc").innerHTML = tongsogiaytuoicay;
			});

			database.ref("/HeThongTuoiCayTuDong/ThoiDiemTuoiCayCuoiCung").on("value",function(snapshot){
				var thoidiemtuoicaycuoicung = snapshot.val();
				document.getElementById("tdtccc").innerHTML = thoidiemtuoicaycuoicung;
			});

			database.ref("/BamNutTuoiCay/DemThoiGian").on("value",function(snapshot){
				var biendem = snapshot.val();
				document.getElementById("bd").innerHTML = biendem;
			});
	    }
	    else{
	        alert("Vui lòng đăng nhập lại.")
	        window.location.href = 'https://btlamweb.web.app/'
	    }
	});
}