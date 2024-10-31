const url = new URL(window.location.href)
const message = url.searchParams.get("message");
const message_type = url.searchParams.get("type");
const message_box = document.getElementById("message");
const message_window = document.getElementById("message-window");

if(message){//メッセージの表示
    message_box.innerText = message;
    message_window.classList.add('active');
    if(message_type=="error")message_window.classList.add("error");
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
                ${(reservation.reservationTime).substr(11,8)}
            </td>
            <td>
                <input type="button" onclick="location.href='/admin/delete/${reservation.id}'" class="delete-button" value="受け取り">
            </td>
            <td>
                <form id="called-form" action="/admin/edit/${reservation.id}" method="post">
                    <input type="hidden" name="name" value="${'*'+reservation.name}">
                    <input type="hidden" name="number" value="${reservation.number}">
                    <input type="hidden" name="ketchup" value="${reservation.ketchup}">
                    <input type="hidden" name="mustard" value="${reservation.mustard}">
                    <input type="hidden" name="reservationTime" value="${reservation.reservationTime}">
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
            <form action="/admin/edit/${reservation.id}" method="post" id="edit-form-${reservation.id}">
                <td>
                    <input form="edit-form-${reservation.id}" type="text" name="name" value="${reservation.name}" class="textbox">
                </td>
                <td>
                    <input form="edit-form-${reservation.id}" type="number" name="number" value="${reservation.number}" max="20" class="textbox">
                </td>
                <td>
                    <input form="edit-form-${reservation.id}" type="checkbox" name="ketchup" class="ketchup" ${(reservation.ketchup)?"checked":""}>
                </td>
                <td>
                    <input form="edit-form-${reservation.id}" type="checkbox" name="mustard" class="mustard" ${(reservation.mustard)?"checked":""}>
                </td>
                <td>
                    <input form="edit-form-${reservation.id}" type="text" name="reservationTime" value="${reservation.reservationTime}" size="8" class="textbox">
                </td>
                <td>
                    <input type="button" class="no-button" value="受け取り">
                </td>
                <td>
                    <input type="button" class="no-button" value="呼び出し">
                </td>
                <td>
                    <input form="edit-form-${reservation.id}" type="submit" class="edit-button" value="完了">
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