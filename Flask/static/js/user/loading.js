// ローカルストレージの内容を取り出し、履歴ページに送る
window.onload = function () {
    const nicknamesArray = localStorage.getItem('nicknames');

    const nicknames = document.getElementById('nicknames');
    nicknames.value = nicknamesArray;

    const localstorage = document.getElementById('localStorage')
    localstorage.submit();
};