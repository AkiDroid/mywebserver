var timeString = function(timestamp) {
    var d = new Date(timestamp * 1000)
    return d.toLocaleString()
}

var todoUpdateFormTemplate = function() {
    var t = `
        <div class="todo-update-form">
            <input class="todo-update-input">
            <button class="todo-update">更新</button>
        </div>
    `
    return t
}

var todoTemplate = function(todo) {
    var title = todo.title
    var id = todo.id
    var ut = timeString(todo.ut)
    var t = `
        <div class="todo-cell" data-id="${id}">
            <button class="todo-edit" data-id="${id}">编辑</button>
            <button class="todo-delete" data-id="${id}">删除</button>
            <span class='todo-title'>${title}</span>
            <span>${ut}</span>
        </div>
    `
    return t
}

var insertTodo = function(todo) {
    var todoCell = todoTemplate(todo)
    var todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var loadTodos = function() {
    apiTodoAll(function(r) {
        var todos = JSON.parse(r)
        for(var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            insertTodo(todo)
        }
    })
}

var bindEventTodoAdd = function() {
    var b = e('#id-button-add')
    b.addEventListener('click', function(){
        var input = e('#id-input-todo')
        var title = input.value
        var form = {
            title: title,
        }
        apiTodoAdd(form, function(r) {
            var todo = JSON.parse(r)
            insertTodo(todo)
        })
    })
}

var bindEventTodoDelete = function() {
    var todoList = e('.todo-list')
    todoList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('todo-delete')) {
            var todoId = self.dataset.id
            apiTodoDelete(todoId, function(r){
                self.parentElement.remove()
            })
        }
    })
}

var bindEventTodoEdit = function() {
    var todoList = e('.todo-list')
    todoList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('todo-edit')) {
            var t = todoUpdateFormTemplate()
            self.parentElement.insertAdjacentHTML('beforeend', t)
        }
    })
}

var bindEventTodoUpdate = function() {
    var todoList = e('.todo-list')
    todoList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('todo-update')) {
            var todoCell = self.closest('.todo-cell')
            var input = todoCell.querySelector('.todo-update-input')
            var id = todoCell.dataset.id
            var form = {
                id: id,
                title: input.value,
            }
            apiTodoUpdate(form, function(r){
                var updateForm = self.closest('.todo-update-form')
                updateForm.remove()
                var todo = JSON.parse(r)
                var title = todoCell.querySelector('.todo-title')
                title.innerHTML = todo.title
            })
        }
    })
}

var bindEvents = function() {
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    bindEventTodoUpdate()
}

var main = function() {
    bindEvents()
    loadTodos()
}

main()
