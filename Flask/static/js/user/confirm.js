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

    // 予約時刻が現在時刻+数分より前の時間の場合はじく
    const dialog = document.querySelector('dialog');

    document.getElementById('confirmOrder').addEventListener("submit", function (e){
        const canReservationDate = new Date();
        const reservationDate = new Date(formatDate(canReservationDate) + " " + reservationTime);
        
        if (reservationDate < canReservationDate.setMinutes(canReservationDate.getMinutes() + 15)) {
            document.getElementById('correctTime').textContent = formatTime(canReservationDate);
            dialog.showModal();
            e.preventDefault();
        }
    });

    // 最短の予約可能時刻に変更して送信
    document.getElementById('yes').addEventListener("click", function() {
        const reservationDate = new Date();
        reservationDate.setMinutes(reservationDate.getMinutes() + 15);
        document.getElementById('reservationTime').value = formatTime(reservationDate);
        document.getElementById('confirmOrder').submit();
        dialog.close();
    });

    // ダイアログを閉じる
    document.getElementById('no').addEventListener("click", function() {
        dialog.close();
    });
};