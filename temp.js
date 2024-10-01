async function sign_up() {
    const url = 'http://127.0.0.1:8000/login';
    const data = {
        username: 'abumi',
        password: 'temp',
    }
    const response = await fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data),
    })
    const rez = await response.json();
    console.log(response.status);
    console.log(rez);
}
async function tasks() {
    const url = 'http://127.0.0.1:8000/createTask';
    const token = '2c1e4f91-d5af-41f8-8801-dbc1d5976d56';
    const data = {
        task: 'Clean the dishes',
    }
    const response = await fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-Token": token},
        body: JSON.stringify(data)
    })
    const rez = await response.json();
    console.log(response.status);
    console.log(rez);
}
async function get() {
    const url = 'http://127.0.0.1:8000/getTasks';
    const token = '6668c89c-d76c-4d39-8dd6-ce0f6dcb30f8';
    const response = await fetch(url, {
        method: "GET",
        headers: {"Content-Type": "application/json", "X-Token": token},
    })
    console.log(response.status);
    if (response.status === 200)  {
        const data = await response.json();
        const dat = data.tasks;
        console.log(dat);
        const rez = dat.map((el) => el.task);
        console.log(rez);
    }  
}
get();