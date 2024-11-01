window.onload = function() {

    const dialog = document.querySelector('dialog');
    document.getElementById('deleteAllHistory').addEventListener('click', function() {
        dialog.showModal();
    });

    // 履歴を削除する
    document.getElementById('yes').addEventListener('click', function() {
        localStorage.setItem('nicknames',  '[]');
        document.getElementById('redirectHistoryPage').submit();
        dialog.close();
    });

    // ダイアログを閉じる
    document.getElementById('no').addEventListener('click', function() {
        dialog.close();
    });
};