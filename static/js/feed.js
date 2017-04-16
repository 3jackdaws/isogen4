/**
 * Created by Ian Murphy on 4/14/2017.
 */

var Feed = {
    entries:[],
    container:$('.rss-feed')[0],
    init:function () {
        const numEntries = 20;
        $.get("/api/feed/" + numEntries, function (data) {
            Feed.entries = data.feed.entry;
            // console.log(data);
            Feed.run();
        })
    },
    run:function () {
        var div = document.createElement("div");
        div.className = 'wrap';

        Feed.entries.forEach(function (entry) {
            console.log(entry);
            var date = new Date(entry.updated);
            div.innerHTML += "" +
                "<div class='entry' onclick='location=\""+ entry.link['@href'] +"\"'>" +
                "<span class='author'>" + entry.author.name.toUpperCase() +"</span> " +
                "<span class='date'>ON " + date.toLocaleDateString().toUpperCase() + ": </span>" +
                "<span class='comment'>\"" + entry.title.toUpperCase().trim() + "\"</span></div>" +
                "<span class='dot'> &middot; </span>";
        });
        Feed.container.appendChild(div);
    }

};
