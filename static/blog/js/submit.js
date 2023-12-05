window.addEventListener("load" , () => {

    
    const categories    = document.querySelectorAll("[name='category']");
    console.log(categories);
    for (let category of categories){
        console.log(category)
        category.addEventListener("change", (e) => {
            console.log( e.currentTarget.value );
            
            // urlにカテゴリーのidを設定する
            // formを利用しないので今回はgetメソッド
            let url     = `/article_category_option_create/?category=${e.currentTarget.value}`;
            let method  = "get";

            const request = new XMLHttpRequest();
            
            request.open(method,url);

            request.send();

            //成功時の処理
            request.onreadystatechange = () => {
                if( request.readyState === 4 && request.status === 200 ){
                    json    = JSON.parse(request.responseText)

                    console.log(json)

                    if ( !json.error ){
                        let html = '<option value="">カテゴリを選択してください</option>'

                        for ( let article_category of json.article_categories ){
                            html += `<option value="${article_category.id}">${article_category.name}</option>`;
                        }

                        const article_categories    = document.querySelectorAll("#article_category");
                        for ( let article_category of article_categories){
                            article_category.innerHTML = html;
                        }

                    }
                }
            }
            
        });


    }








});