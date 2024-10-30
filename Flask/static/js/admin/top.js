function create_html(reservation){
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
            <input type="button" class="delete-button" value="受け取り">
        </td>
        <td>
            ${(reservation.name[0] == "*")?"":
                '<input type="button" class="called-button" value="呼び出し済">'
            }
        </td>
        <td>
            <input type="button" class="edit-button" value="編集">
        </td>
    </tr>
    `;
    return html;
}

const table = document.getElementById("main-table");

function print_table(reservations){
    let table_html = "";
    for(const reservation of reservations){
        table_html += create_html(reservation)
    }
    table.innerHTML = table_html;
}