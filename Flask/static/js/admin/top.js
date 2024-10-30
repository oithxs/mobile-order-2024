const url = new URL(window.location.href)
const message = url.searchParams.get("message");
const message_box = document.getElementById("message");
const message_window = document.getElementById("message-window");

if(message){//メッセージの表示
    message_box.innerText = message;
    message_window.classList.add('active');
    setTimeout(()=>{
        message_window.classList.remove('active');
    }, 5000)
}

const table = document.getElementById("main-table");
let global_reservations;

function create_html(reservation){
    let html;
    if(!reservation.edit){
        html = `
        <tr class="${(reservation.name[0] == "*")?"called":""}">
            <td>${reservation.name}</td>
            <td>${reservation.number}</td>
            <td>
                <input type="checkbox" class="ketchup" disabled="disabled" ${(reservation.ketchup)?"checked":""}>
            </td>
            <td>
                <input type="checkbox" class="mustard" disabled="disabled" ${(reservation.mustard)?"checked":""}>
            </td>
            <td>
                ${(reservation.reservationTime)?
                    (reservation.reservationTime).substr(11,8):
                    "現地受け取り"
                }
            </td>
            <td>
                <input type="button" onclick="location.href='/admin/delete/${reservation.id}'" class="delete-button" value="受け取り">
            </td>
            <td>
                <form action="/admin/edit/${reservation.id}" method="post">
                    <hidden name="name">${'*' + reservation.name}</hidden>
                    <hidden name="number">${reservation.number}</hidden>
                    <hidden name="ketchup">${reservation.ketchup}</hidden>
                    <hidden name="mustard">${reservation.mustard}</hidden>
                    <hidden name="reservationTime">${reservation.reservationTime}</hidden>
                    <input type="submit" class="${(reservation.name[0] == "*")?"no-button":"called-button"}" value="呼び出し">
                </form>
            </td>
            <td>
                <input type="button" class="edit-button" value="編集" onclick="edit_set(${reservation.id})">
            </td>
        </tr>
        `;
    }else{//編集時の画面
        html = `
        <tr class="${(reservation.name[0] == "*")?"called":""}">
            <form action="/admin/edit/${reservation.id}" method="post">
                <td>
                    <input type="text" name="name" value="${reservation.name}" class="textbox">
                </td>
                <td>
                    <input type="number" name="number" value="${reservation.number}" max="20" class="textbox">
                </td>
                <td>
                    <input type="checkbox" name="ketchup" class="ketchup" ${(reservation.ketchup)?"checked":""}>
                </td>
                <td>
                    <input type="checkbox" name="mustard" class="mustard" ${(reservation.mustard)?"checked":""}>
                </td>
                <td>
                    <input type="text" name="reservationTime" value="${reservation.reservationTime}" size="8" class="textbox">
                </td>
                <td>
                    <input type="button" class="no-button" value="受け取り">
                </td>
                <td>
                    <input type="button" class="no-button" value="呼び出し">
                </td>
                <td>
                    <input type="submit" class="edit-button" value="完了">
                </td>
            </form>
        </tr>
        `
    }
    return html;
}
function edit_set(id){
    for(const reservation of global_reservations){
        if(reservation.id == id){
            reservation.edit = true;
        }
    }
    print_table();
}
function edit_called(id){

}

function print_table(){
    let table_html = "";
    for(const reservation of global_reservations){
        table_html += create_html(reservation)
    }
    table.innerHTML = table_html;
}