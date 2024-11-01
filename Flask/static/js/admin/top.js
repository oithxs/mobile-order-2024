const form = document.getElementById("delete")

function SendDeleteForm() {
    const formData = new FormData(form)
    const action = form.getAttribute("action")
    const options = {
        method: 'POST',
        body: formData,
    }
    fetch(action, options).then((e) => {
        if(e.status === 200) {
            alert("削除しました")
            return
        }
        alert("削除に失敗しました")
    });
}
//デバッグ用コード=====　勝手に消しといて
setTimeout(()=>{
    window.location.reload()
}, 5000)