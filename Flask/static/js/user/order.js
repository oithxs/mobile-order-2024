window.onload = function () {

    // 現在の時刻を取得し入力欄に代入
    const date = new Date();
    rTime = document.getElementById("reservationTime");
    console.log(rTime.value);
    rTime.value = date.getHours().toString() + ":" + date.getMinutes().toString();
};