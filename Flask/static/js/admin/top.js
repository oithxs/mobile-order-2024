const url = new URL(window.location.href)
const data = url.searchParams.get("message");
console.log(data);

document.querySelector('a[href="http://localhost:5000/admin/delete/0"]').addEventListener('click', function(event) {
    event.preventDefault(); // リンクのデフォルトの動作を防ぐ
    const messageWindow = document.getElementById('message-window');
    messageWindow.classList.add('active'); // メッセージを表示
    messageWindow.style.display = 'block'; // メッセージを表示

    // 3秒後にメッセージを非表示にする
    setTimeout(function() {
        messageWindow.classList.remove('active'); // メッセージのクラスを削除
        messageWindow.style.display = 'none'; // メッセージを非表示
    }, 3000);
});
