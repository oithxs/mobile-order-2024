window.onload = function () {

    let paddingTime = function(str) {
        if(str.length == 1){
            str = "0"+ str;
        }
        return str;
    }

    // 現在の時刻を取得し入力欄に代入
    const date = new Date();
    rTime = document.getElementById("reservationTime");
    console.log(rTime.value);
    rTime.value = paddingTime(date.getHours().toString()) + ":" + paddingTime(date.getMinutes().toString());


    let calcSum = function (value) {
        return 150 * value;
    }

    count = document.getElementById("count");

    count.addEventListener("change",function(){
        money = document.getElementById("resultMoney");
        money.innerText = calcSum(count.value);
        }
    )
};

window.onpageshow = function(event) {
	if (event.persisted) {
		window.location.reload();
	}
};