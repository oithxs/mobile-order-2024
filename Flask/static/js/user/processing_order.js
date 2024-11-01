window.onload = function () {
    // ローカルストレージにニックネームを登録する
    const array = JSON.parse(localStorage.getItem('nicknames'));
    array[array.length] = nickname;
    localStorage.setItem("nicknames", JSON.stringify(array));

    //ニックネームを登録したフラグを付ける
    document.getElementById('isNicknameRegistered').value = "true";

    //ニックネームをflask側に送信する
    document.getElementById('nickname').value = nickname;
    document.getElementById('addToLocalStorage').submit();
}