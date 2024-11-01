window.onload = function () {

    function formatTime(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    function formatDate(date) {
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        return `${year}/${month}/${day}`;
    }

    // 現在の時刻を取得し数分を足した後入力欄に代入
    const minReservationDate = new Date();
    minReservationDate.setMinutes(minReservationDate.getMinutes() + 15 + 1);

    document.getElementById("reservationTime1").value = formatTime(minReservationDate);

    // フランクフルトの合計金額を求める
    document.getElementById("count").addEventListener("change",function(){
        money = document.getElementById("resultMoney");
        money.innerText = 150 * count.value;
        }
    )

    // 予約時刻が現在時刻+数分より前の時間の場合はじく
    // const dialog = document.querySelector('dialog');
    
    // document.getElementById('orderForm').addEventListener("submit", function (e){
    //     if (document.getElementById('wantToReserve1').checked) {
    //         const canReservationDate = new Date();
    //         const reservationDate = new Date(formatDate(canReservationDate) + " " + document.getElementById('reservationTime1').value);
            
    //         if (reservationDate < canReservationDate.setMinutes(canReservationDate.getMinutes() + 15)) {
    //             document.getElementById('correctTime').textContent = formatTime(canReservationDate);
    //             dialog.showModal();
    //             e.preventDefault();
    //         }
    //     }
    // });

    const dialog = document.querySelector('dialog');
    document.getElementById('yes').addEventListener("click", function() {
        dialog.close();
    });

    function isTimeValidate() {
        if (document.getElementById('wantToReserve1').checked) {
            const canReservationDate = new Date();
            const reservationDate = new Date(formatDate(canReservationDate) + " " + document.getElementById('reservationTime1').value);
            
            if (reservationDate < canReservationDate.setMinutes(canReservationDate.getMinutes() + 15)) {
                document.getElementById('correctTime').textContent = formatTime(canReservationDate);
                return false;
            }
            else {
                return true;
            }
        }
        else {
            return true;
        }
    }

    // 注文確認へフォームを送信する処理
    document.getElementById('goToConfirm').addEventListener('click', function() {
        if (isTimeValidate()) {
            document.getElementById('orderForm').submit();
        }
        else {
            dialog.showModal();
        }
    });

    // マイナスのボタンの処理
    document.getElementById('decrement').addEventListener('click', function() {
        let count = document.getElementById('count');
        if(Number(count.value) > 1) {
            count.value = String(Number(count.value) - 1);
            // 合計金額も変更する
            money = document.getElementById("resultMoney");
            money.innerText = 200 * count.value;
        }
    });

    // プラスのボタンの処理
    document.getElementById('increment').addEventListener('click', function() {
        let count = document.getElementById('count');
        if(Number(count.value) < 15) {
            count.value = String(Number(count.value) + 1);
            // 合計金額も変更する
            money = document.getElementById("resultMoney");
            money.innerText = 200 * count.value;
        }
    });
};

// 受け取り時刻の選択欄の活性・非活性化
function changeDisabled(){
    if(document.getElementById("wantToReserve0").checked){
        document.getElementById("reservationTime0").disabled = false;
        document.getElementById("reservationTime1").disabled = true;
    }else if(document.getElementById("wantToReserve1").checked){
        document.getElementById("reservationTime0").disabled = true;
        document.getElementById("reservationTime1").disabled = false;
    }
}

// ブラウザバックしても強制読み込み
// window.onpageshow = function(event) {
// 	if (event.persisted) {
// 		window.location.reload();
// 	}
// };