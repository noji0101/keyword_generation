function main(extracted_words, edges){
    nodes = extracted_words
    links = edges
    display_words(nodes, links)
}

function display_words(nodes, links){
    width = 1200;
    height = 800;

    selected_words = []

    svg = d3.select("#result")
        .append("svg")
        .attr("width", width)
        .attr("height", height)

    g = svg.append("g");

    // SVG の画像要素
    node = g.selectAll(".node");
    link = g.selectAll(".link");
    label = g.selectAll(".label");

    simulation = d3.forceSimulation( nodes )
        .on("tick", ticked );

    // ドラッグ制御
    drag = d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);

    update(nodes)
}

function add_node() {
    element = document.getElementById('add_word');
    if (element.value != ''){
        word = element.value
        new_id = nodes.length 
        x = 200 + Math.random()*400
        y = 800 - x
        nodes.push({'id':new_id, 'label':word, 'x':x, 'y':y})
        
        update(nodes);
        element.value = ''
    }
}

function update(nodes) {

    // transition
    var t = d3.transition().duration(750);    

    // link の更新 ======>
    link = link.data(links);
    link.exit().remove();
    
    link = link
        .enter()
        .append("line")
        .style('stroke', "#000")
        .style("stroke-width", 1)
        .merge(link);

    // node の更新  ======>

    // 新しく nodes をバインド
    node = node.data(nodes, function( d ) { return d.id; } );

    // バインドした情報に存在しない DOM を削除
    node.exit().transition( t ).attr( "r", 1e-4 ).remove();

    // 新しくバインドした nodes を元に DOM を生成
    node = node.enter()
        .append("ellipse")
        .attr('rx', 40)
        .attr('ry', 20)
        .style('fill', "#fff")
        .style("stroke", "#000")
        .style("stroke-width", 3)
        .call(drag)
        .property("checked", false)
        .on('click', function(){
            // クリックされたら色とis_checkedを変更
            is_checked = !d3.select(this).property("checked");
            d3.select(this).property("checked", is_checked);

            if (is_checked){
                d3.select(this).style("stroke", "#f44");
                d3.select(this).style("stroke-width", 3);
            }else{
                d3.select(this).style("stroke", "#000");
                d3.select(this).style("stroke-width", 3);
            };
            // is_checked=Trueの単語を取り出す
            selected_words = []
            node_elements = d3.selectAll(node)['_groups'][0]['_groups'][0]
            for (idx in node_elements){
                if (node_elements[idx]['checked']){
                    selected_words.push(node_elements[idx].__data__['label'])
                }
            }

            selected_ids = []
            for (idx in node_elements){
                if (node_elements[idx]['checked']){
                    selected_ids.push(node_elements[idx].__data__['id'])
                }
            }
        })
        .merge(node); // 前の DOM とマージする
    
    // label の更新 ======>
    label = label.data(nodes);
    label.exit().remove();
    
    label = label.enter()
        .append('text')
        .attr("text-anchor", "middle")
        .attr("fill", "black")
        .attr("font-size", "11px")
        .text(function(data) { return data.label; })
        .merge(label);

    // forceSimulation 開始
    simulation.nodes(nodes)
    .force("charge", d3.forceManyBody().strength(-300))
    .force("forceX", d3.forceX().strength(.05))
    .force("forceY", d3.forceY().strength(.08))
    .force("center", d3.forceCenter( width/2, height/2 ))
    .force("link", d3.forceLink( links ).distance( 150 ).strength(1.5).iterations(2) )
    .alphaTarget(0.01)
    ;

}

function ticked() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    label.attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y; });
}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}


function reinfer_func(){

    var is_full = true
    console.log(is_full)
    for (idx in [0, 1, 2, 3]){
        if (document.forms[0].elements['words'][idx].value == ''){
            is_full = false
        }
    }

    if (is_full){
        $("#loading").show();
        $("#content").hide();   

        // 選択された単語とそのIDの送信
        var form = document.reget_form
        // form.method = 'POST';
        // form.action = '/send';
        
        for (idx in selected_words){
            // var request1 = document.createElement('input');
            // request1.type = 'hidden'; //入力フォームが表示されないように
            // request1.name = 'words';
            // request1.value = selected_words[idx];
            // form.appendChild(request1);
            // document.body.appendChild(form);

            var request2 = document.createElement('input'); 
            request2.type = 'hidden'; //入力フォームが表示されないように
            request2.name = 'ids';
            request2.value = selected_ids[idx];
            form.appendChild(request2);
            // document.body.appendChild(form);
        }

        form.submit();

        return true
    }else{
        alert('全てのフィールドに入力してください')
        return false
    }


}


function loading1(){
    var is_full = true
    for (idx in [0, 1, 2, 3]){
        if (document.forms[0].elements['words'][idx].value == ''){
            is_full = false
        }
    }
    if (document.forms[0].elements['name'].value == ''){
        is_full = false
    }
    if (is_full){
        $("#loading").show();
        $("#content").hide();   
        return true
    }else{
        alert('全てのフィールドに入力してください')
        return false
    }
}

function loading2(){
    $("#loading").show();
    $("#content").hide();    
}