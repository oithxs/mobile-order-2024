window.onload = function() {
    const dialog = document.querySelector('dialog');

    const deleteAllHistory = document.getElementById('deleteAllHistory');

    deleteAllHistory.addEventListener('click', function() {
        dialog.showModal();
    });

    document.getElementById('yes').addEventListener('click', function() {
        localStorage.setItem("nicknames", "[]");
        alert("削除しました");
        dialog.close();
        document.getElementById('redirectHistoryPage').submit();
    })

    document.getElementById('no').addEventListener('click', function() {
        dialog.close();
    })
}