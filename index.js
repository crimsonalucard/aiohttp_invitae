console.log("test");
axios.get('http://0.0.0.0:1337/?name=Brian')
  .then(function (response) {
    console.log(response);
    var div = document.createElement('div');
    var responseText = JSON.stringify(response.data);
    $(div).text(responseText).addClass('content');
    $(".main").append(div);
  })
  .catch(function (error) {
    console.log(error);
  });