function search_suggest(keyword) {
    $.ajax({
        url: "/search/suggest",
        type: "POST",
        data: {
            "search-input": keyword
        },
        success: function (data) {
            // console.log(data)
            const suggest_wrap = document.getElementById("suggest_wrap")
            let text = ""
            if (data.status === 1) {
                const house_list = data.data
                for (let i = 0; i < house_list.length; i++) {
                    text += `<li class="suggest_item">
                                <span class="item_title">${house_list[i].title}</span>
                                <span class="item_addr">${house_list[i].city_id}&nbsp;${house_list[i].district_id}</span>
                                <span class="item_price">￥${house_list[i].price}</span>
                             </li>`
                }
                if (keyword.length === 0) {
                    text = ""
                }
                $("#suggest_list").display = "block"
                suggest_wrap.innerHTML = text
            }
        }
    })
}


$(document).ready(function () {
    const search_input = document.getElementById("search-input")
    // 设置锁，true表示锁住输入框，false表示解锁输入框
    var cpLock = false;
    // 中文搜索，监听compositionstart事件，如果触发该事件，就锁住输入框
    $('#search-input').on('compositionstart', function () {
        cpLock = true;
    });

    // 中文搜索，监听compositionend事件，如果触发该事件，就解锁输入框
    $('#search-input').on('compositionend', function () {
        cpLock = false;
        const keyWord = search_input.value;
        search_suggest(keyWord)
    });

    // 英文搜索，监听input事件，用于处理字母搜索
    $('#search-input').on('input', function () {
        if (!cpLock) {
            var keyWord = search_input.value;
            search_suggest(keyWord);
        }
    });
})