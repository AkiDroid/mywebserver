var timeString = function (timestamp) {
    var d = new Date(timestamp * 1000)
    return d.toLocaleString()
}

var weiboTemplate = function (weibo) {
    var w = `
    <div class="weibo-cell" data-id="${weibo.id}">
        ${weibo.content} from ${weibo.username}
        <button class="weibo-delete" data-href="/weibo/delete?id=${weibo.id}">删除</button>
        <button data-href="/weibo/edit?id=${weibo.id}">修改</button>
        <div class="gua-form comment-form"
             data-id="${weibo.id}"
             data-action="/comment/add"
             data-callback=""
             data-method="post">
            <input class="weibo-id" type="hidden" name="weibo_id" value="${weibo.id}">
            <input class="comment-content" name="content">
            <br>
            <button class="comment-add" type="submit">添加评论</button>
        </div>
    </div>
    `
    return w
}

var weiboUpdateFormTemplate = function (weiboCell) {
    var weiboContent = weiboCell.querySelector('.weibo-content')
    var content = weiboContent.querySelector('.content').innerText
    var w = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${content}">
            <button class="weibo-update">更新</button>
        </div>
    `
    return w
}

var weiboContentTemplate = function (weibo) {
    var id = weibo.id
    var wc = `
    <div class="weibo-content">
                <span class="content">${weibo.content}</span>> from ${weibo.username}
                <button class="weibo-delete" data-href="/weibo/delete?id=${id}">删除</button>
                <button class="weibo-edit" data-href="/weibo/edit?id=${id}">修改</button>
            </div>
    `
    return wc
}

var insertWeibo = function (weibo) {
    var weiboCell = weiboTemplate(weibo)
    var weiboList = e('.weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var commentTemplate = function (comment) {
    var c = `
    <div class="comment" data-id=${comment.id}>
                    ${comment.username} : ${comment.content}
                    <button class="comment-delete">删除</button>
                </div>
    `
    return c
}

var insertComment = function (comment, weiboId) {
    var commentCell = commentTemplate(comment)
    var query = '.comment-list-' + weiboId
    var commentList = e(query)
    commentList.insertAdjacentHTML('beforeend',commentCell)
}

var bindEventWeiboDelete = function () {
    var body = document.body
    body.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('weibo-delete')) {
            var weiboCell = self.closest('.weibo-cell')
            var weiboId = weiboCell.dataset.id
            apiWeiboDelete(weiboId, function (r) {
                weiboCell.remove()
            })
        }
    })
}

var bindEventCommentAdd = function () {
    var body = document.body
    body.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('comment-add')) {
            var commentForm = self.closest('.comment-form')
            var weiboId = commentForm.dataset.id
            var content = commentForm.querySelector('.comment-content').value
            var form = {
                weibo_id: weiboId,
                content: content,
            }
            apiCommentAdd(form, function (r) {
                var comment = JSON.parse(r)
                console.log(comment)
                insertComment(comment, weiboId)
            })
        }
    })
}

var bindEventWeiboAdd = function () {
    var add_button = e('#id-button-add')
    add_button.addEventListener('click', function (event) {
        var self = event.target
        var input = e('#id-input-weibo')
        weibo = input.value
        var form = {
            content: weibo,
        }
        apiWeiboAdd(form, function (r) {
            var weibo = JSON.parse(r)
            insertWeibo(weibo)
        })
    })
}

var bindEventWeiboEdit = function () {
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('weibo-edit')) {
            var weiboCell = self.closest('.weibo-cell')
            var weibo_id = weiboCell.dataset.id

            w = weiboUpdateFormTemplate(weiboCell)
            weiboCell.insertAdjacentHTML('afterBegin', w)

            var weiboContent = self.closest('.weibo-content')
            weiboContent.remove()
        }
    })
}

var bindEventWeiboUpdate = function () {
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('weibo-update')) {
            var weiboCell = self.closest('.weibo-cell')
            var input = weiboCell.querySelector('.weibo-update-input')
            var id = weiboCell.dataset.id
            form = {
                id: id,
                content: input.value
            }
            apiWeiboUpdate(form, function (r) {
                var weibo = JSON.parse(r)
                var weibo_content = weiboContentTemplate(weibo)
                weiboCell.insertAdjacentHTML('afterBegin', weibo_content)
                self.parentElement.remove()
            })
        }
    })
}

var bindEventCommentDelete = function () {
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('comment-delete')) {
            var comment = self.closest('.comment')
            var comment_id = comment.dataset.id
            apiCommentDelte(comment_id, function (r) {
                comment.remove()
            })

        }

    })
}

var bindEvents = function () {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventCommentAdd()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentDelete()
}

var main = function () {
    bindEvents()
}

main()

