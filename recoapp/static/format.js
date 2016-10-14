USER_ID = Math.round(Math.random() * 10000) + 140000

function add_listener(){

  $('button').off('click')

  $('button').click(function(){

    var data = {
      user_id: USER_ID,
      movie_id: $(this).parent().parent().attr("data-id"),
      liked: $(this).text() == 'Love' ? 1 : 0
    }
    $.post('/api/rate', data)

    d3.select(this)
      .style("color", "#FFF")
      .style("border-color", "#33C3F0")
      .style("background-color", "#33C3F0")

    d3.select(this)
      .transition()
      .duration(1000)
      .style("color", "#555")
      .style("border-color", "#D1D1D1")
      .style("background-color", "white")
  })
}

function build_table(){

  var options = {
    valueNames: ['title', 'year', { data: ['id'] }],
    page: 6,
    plugins: [
          ListPagination({innerWindow: 3})
        ]
  }
  var movies = new List('input', options);

  movies.remove("year", -1)
  movies.on("updated", add_listener)
  movies.on("searchComplete", add_listener)

  $.get('/api/movies', function(data){
    movies.add(data)
  })
}

function start_polling(user_id){
  recs = $.get('/api/recommend/' + USER_ID, function(data){

  })
}

function start_polling(data){

  function redraw_tables(data){
    top_table.clear()
    bottom_table.clear()

    top_table.add(data.top)
    bottom_table.add(data.bottom)
  }

  function poll(){
    var data = {method: 'raw'}
    $.get('/api/recommend/' + USER_ID, data, function(data){
      redraw_tables(data)
    })
  }

  var options = {
    valueNames: ['title', 'year'],
  }

  var top_table = new List('top', options)
  var bottom_table = new List('bottom', options)

  setInterval(poll, 3000)
}

$(document).ready(function(){

  console.log("Ready as user " + USER_ID)

  build_table();
  start_polling();
})
