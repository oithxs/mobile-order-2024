function create_html(reservation){
    html = `
    <tr>
        <td>${reservation.name}</td>
        <td>${reservation.number}</td>
        <td>
            <input type="checkbox" class="ketchup" disabled="disabled" ${(reservation.ketchup)?"checked":""}>
        </td>
        <td>
            <input type="checkbox" class="mustard" disabled="disabled" ${(reservation.mustard)?"checked":""}>
        </td>
        <td>${reservation.reservationTime}</td>
        <td>
            <input type="button" class="delete" value="受け取り">
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