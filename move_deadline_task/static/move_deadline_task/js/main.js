const NOTCREATOR = "not creator";

document.addEventListener('DOMContentLoaded', () => {
    const buttons = ['byJS', 'byAdmin', 'forAuth', 'onlyOwn'].map(id => document.getElementById(id));

    BX24.init(() => {
        const response = BX24.placement.info();
        let task_id = response.options.taskId;
        window.BX24_is_loaded = true;

        buttons.forEach(button => {
            button.setAttribute('task_id', task_id);
            button.addEventListener('click', (event) => handleButtonClick(event));
        });
    });
});

function handleButtonClick(event) {
    const button = event.target;
    const task_id = button.getAttribute('task_id');
    const originalColor = button.style.backgroundColor;
    const url = button.getAttribute('url');

    const actionFunction = button.id === 'byJS' ? moveDeadline : fetchRequest;

    button.disabled = true;
    button.style.backgroundColor = 'gray';

    actionFunction(task_id, url)
        .then(result => resultProcess(button, result, originalColor))
        .catch(error => errorProcess(button, error, originalColor));
}

function fetchRequest(task_id, url) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'task_id': task_id
        })
    }).then(response => response.text());
}

function resultProcess(button, result, originalColor) {
    console.log(result);
    if (result.trim() === NOTCREATOR)
        return Promise.reject(NOTCREATOR);
    button.style.backgroundColor = 'green';
    setTimeout(() => {
        button.disabled = false;
        button.style.backgroundColor = originalColor;
    }, 2000);
}

function errorProcess(button, error, originalColor) {
    console.error(error);
    if (error === NOTCREATOR)
        alert('Вы не постановщик задачи');
    button.style.backgroundColor = 'red';
    setTimeout(() => {
        button.disabled = false;
        button.style.backgroundColor = originalColor;
    }, 2000);
}

function moveDeadline(task_id) {
    let taskDeadline = new Promise((resolve, reject) => {
        BX24.callMethod("tasks.task.get", { 'taskId': task_id, 'fields': ["DEADLINE"] }, res => {
            if (res.error()) {
                reject(res.error());
            } else {
                let cur_deadline = res.answer.result.task['deadline'] || dayjs();
                let deadline = dayjs(cur_deadline).add(1, 'day').format('DD.MM.YYYY HH:mm');
                resolve(deadline);
            }
        });
    });
    return taskDeadline
        .then(deadline => updateTaskDeadline(task_id, deadline))
        .then(() => 'Deadline moved successfully')
        .catch(error => Promise.reject(error));

}


function updateTaskDeadline(task_id, deadline) {
    return new Promise((resolve, reject) => {
        BX24.callMethod("tasks.task.update", { 'taskId': task_id, 'fields': { "DEADLINE": deadline.toString() } }, res => {
            res.error() ? reject(res.error()) : resolve();
        });
    });
}



