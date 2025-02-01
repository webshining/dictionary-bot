document.addEventListener("DOMContentLoaded", async () => {
    const name = document.querySelector(".dictionary__name");
    const content = document.querySelector(".content");
    const data = await get_dictionary(3);
    name.innerHTML = `<input class="dictionary__name_input" value=${data.name}></input>`;
    data.words.forEach((element) => {
        content.innerHTML += `
            <div class="word__content" key="${element.id}">
                <div class="word__text">
                    ${element.word}<br>—<br>${element.translate}
                </div>
                <div class="word__buttons">
                    <span class="material-symbols-outlined" onclick="delete_word(${data.id}, ${element.id})">
                        delete
                    </span>
                </div>
            </div>
        `;
    });

    let timeout_id;
    const name_input = document.querySelector(".dictionary__name_input");
    name_input.addEventListener("input", (e) => {
        clearTimeout(timeout_id);
        timeout_id = setTimeout(async () => {
            await update_dictionary(data.id, e.target.value);
        }, 1000);
    });
});
